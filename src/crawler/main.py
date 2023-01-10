# -*- coding: utf-8 -*-
# @Author: xiaocao
# @Date:   2023-01-07 14:26:05
# @Last Modified by:   xiaocao
# @Last Modified time: 2023-01-10 23:14:40


from peewee import Model
import re
import time
import datetime
from typing import List
import aiohttp
import asyncio

from peewee import chunked, fn
from db.db import PublishSource, ServersAd, ServersAdCount, database

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
}


async def get_html(url, headers=HEADERS, charset=None):
    """获取网页html

    Args:
        url (_type_): _description_
        headers (_type_, optional): _description_. Defaults to HEADERS.

    Returns:
        _type_: _description_
    """

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            return await resp.text(encoding=charset, errors='ignore')


def resolver(html, publish_source: PublishSource, current_time):
    """解析网页html，返回广告记录 的字典 迭代器

    Args:
        html (_type_): _description_
        publish_source (_type_, optional): _description_. Defaults to None.

    Returns:
        _type_: _description_
    """

    r = re.compile(rf'{publish_source.record_reg_exp}')
    search_result = r.findall(html)

    year = time.gmtime()[0]

    for record in search_result:
        timestamp = time_format(
            year, record[publish_source.located_time], publish_source)

        # 过滤已经过时的广告记录
        if current_time < timestamp:
            yield {
                'timestamp': timestamp,
                'url': record[publish_source.located_url],
                'name': record[publish_source.located_name],
                "ip": record[publish_source.located_ip],
                "route": record[publish_source.located_route],
                "description": record[publish_source.located_description],
                "service": record[publish_source.located_service],
            }


def time_format(year: int, time_string: str, publish_source: PublishSource):
    """格式化时间

    Args:
        time_string (_type_): _description_
        time_reg_exp (_type_, optional): _description_. Defaults to None.

    Returns:
        _type_: _description_
    """

    r = re.compile(publish_source.time_reg_exp)

    if result := r.search(time_string):
        month = int(result[1])
        day = int(result[2])
        hour = int(result[3]) if result[3] else 23
        minute = int(result[4]) if result[4] else 0 if result[3] else 59

        return datetime.datetime(year, month, day, hour, minute)
    else:
        raise ValueError


def get_records_from_db(datetime):
    """查询尚未到展示时间的广告

    Args:
        datetime (_type_): _description_

    Returns:
        _type_: _description_
    """
    result = ServersAd.select(ServersAd.url, ServersAd.timestamp).where(
        ServersAd.timestamp > datetime)

    return result


def remove_duplicates_for_db(records_db: List[ServersAd], records_crawler):
    """ 1.与数据库对比，去除数据库内已经存在的记录
        2.去除爬取的重复广告，并标记广告重复次数
        3.构造数据id

    Args:
        records_db (_type_): _description_

    Returns:
        _type_: _description_
    """

    # 基于url 与 时间 构造数据库内的广告标识
    tags_db = [
        f"{record.url}-{datetime.datetime.timestamp(record.timestamp)}" for record in records_db]

    count_dict = {}
    id_count_dict = {}

    removed_duplicates_records = []

    server_id = get_primary_key_num(ServersAd)
    for record in records_crawler:
        tag = f"{record['url']}-{datetime.datetime.timestamp(record['timestamp'])}"

        if tag not in tags_db:

            if tag in count_dict:
                count_dict[tag] += 1
            else:
                count_dict[tag] = 1

                server_id += 1
                record['id'] = server_id

                id_count_dict[server_id] = tag
                removed_duplicates_records.append(record)
    id_count = ({"source": 1, "game": id, "count": count_dict[tag]}
                for id, tag in id_count_dict.items())
    return removed_duplicates_records, id_count  # 去重的广告记录，广告


def get_primary_key_num(model: Model):
    """获取模型的当前id 主键 最大值

    Args:
        model (Model): _description_

    Returns:
        _type_: _description_
    """
    sql = f"SHOW TABLE STATUS where name='{model._meta.table_name}'"
    result = database.execute_sql(sql).fetchone()
    return result[10]


def marks_counters_for_record(records):
    """标记广告条数

    Args:
        source (_type_): _description_

    Returns:
        _type_: _description_
    """

    count_dict = {}
    removed_duplicates_records = []

    for record in records:
        if item := f"{record['url']}-{record['timestamp']}" in count_dict:
            count_dict[item] += 1
        else:
            count_dict[item] = 1
            removed_duplicates_records.append(record)

    return removed_duplicates_records, count_dict  # 去重的广告记录，广告


def load_publish_source_config() -> List[PublishSource]:
    """加载采集配置文件

    Returns:
        _type_: _description_
    """

    return PublishSource.select().where(PublishSource.active == True)


def save_crawled_data(server, server_count, publish_source, current_time):
    """保存抓取的数据

    Args:
        server (_type_): _description_
        server_count (_type_): _description_
        publish_source (_type_): _description_
        current_time (_type_): _description_
    """

    with database.atomic():
        # 更新爬虫最后运行时间
        publish_source.last_run_time = current_time
        publish_source.save()

        # 保存广告数据
        for batch in chunked(server, 500):
            ServersAd.insert_many(batch).execute()

        # 保存广告数量数据
        for batch in chunked(server_count, 500):
            ServersAdCount.insert_many(batch).execute()


async def collect(publish_source: PublishSource):
    """采集网页信息并存入数据库

    Args:
        publish_source (_type_, optional): _description_. Defaults to None.

    Returns:
        _type_: _description_
    """

    html = await get_html(publish_source.url, headers=HEADERS, charset=publish_source.charset)

    current_time = datetime.datetime.now()

    crawler_data = resolver(html, publish_source, current_time)

    records_db = get_records_from_db(datetime=current_time)

    server_ad, server_ad_count = remove_duplicates_for_db(
        records_db, crawler_data)

    save_crawled_data(server_ad, server_ad_count, publish_source, current_time)


async def async_run():

    while True:

        publish_source_list = load_publish_source_config()
        tasks = [asyncio.create_task(collect(publish_source), name=f'任务-{publish_source.id}')
                 for publish_source in publish_source_list]

        tasks and await asyncio.wait(tasks)
        await asyncio.sleep(60)


def run():
    print("爬虫 Running...")
    asyncio.run(async_run())


if __name__ == "__main__":
    import re
    c = re.compile("(\d)+月(\d+)日.(?:(\d+)点)?(?:(\d+)分)?")

    res = c.search("1月10日/17点开放")
    print(res.groups())
