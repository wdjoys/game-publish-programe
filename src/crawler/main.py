# -*- coding: utf-8 -*-
# @Author: xiaocao
# @Date:   2023-01-07 14:26:05
# @Last Modified by:   xiaocao
# @Last Modified time: 2023-01-11 23:55:18


import functools
from peewee import Model
import re
import time
import datetime
from typing import List
import aiohttp
import asyncio

from peewee import chunked, fn
from db.db import PublishSource, ServerTag, ServersAd, ServersAdCount, Tags, DATABASE
from asyncio.coroutines import iscoroutine


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
}


def print_run_time(func):
    """计算函数执行耗时

    Args:
        func (_type_): _description_

    Returns:
        _type_: _description_
    """
    def wrapper(*args, **kw):
        local_time = time.time()
        result = func(*args, **kw)
        print(
            f'Function [{func.__name__}] run time is {time.time() - local_time}')
        return result

    return wrapper


# 异步计算时间函数
def async_print_run_time(func):

    @functools.wraps(func)
    async def wrapper(*args, **kw):
        local_time = time.time()
        result = await func(*args, **kw)
        print(
            f'Function [{func.__name__}] run time is {time.time() - local_time}')
        return result

    return wrapper


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

    for record in search_result:
        timestamp = time_format(
            current_time, record[publish_source.located_time], publish_source)

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


def time_format(current_time: datetime.datetime, time_string: str, publish_source: PublishSource):
    """格式化时间

    Args:
        time_string (_type_): _description_
        time_reg_exp (_type_, optional): _description_. Defaults to None.

    Returns:
        _type_: _description_
    """

    r = re.compile(publish_source.time_reg_exp)

    if result := r.search(time_string):
        month = int(result[1]) if result[1] else current_time.month
        day = int(result[2]) if result[1] else current_time.day
        hour = int(result[3]) if result[3] else 23
        minute = int(result[4]) if result[4] else 0 if result[3] else 59

        return datetime.datetime(current_time.year, month, day, hour, minute)
    else:
        raise ValueError


@print_run_time
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


@print_run_time
def remove_duplicates_for_db(records_db: List[ServersAd], records_crawler, publish_source):
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
    id_count = ({"source": publish_source.id, "game": id, "count": count_dict[tag]}
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
    result = DATABASE.execute_sql(sql).fetchone()
    return result[10]-1


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


@print_run_time
def load_publish_source_config() -> List[PublishSource]:
    """加载采集配置文件

    Returns:
        _type_: _description_
    """

    return PublishSource.select().where(PublishSource.active == True)


@print_run_time
def save_crawled_data(server, server_count, publish_source, ads_tags, current_time):
    """保存抓取的数据

    Args:
        server (_type_): _description_
        server_count (_type_): _description_
        publish_source (_type_): _description_
        current_time (_type_): _description_
    """

    with DATABASE.atomic():
        # 更新爬虫最后运行时间
        publish_source.last_run_time = current_time
        publish_source.save()

        # 保存广告数据
        for batch in chunked(server, 500):
            ServersAd.insert_many(batch).execute()

        # 保存广告数量数据
        for batch in chunked(server_count, 500):
            ServersAdCount.insert_many(batch).execute()

        # 保存广告tags数据
        for batch in chunked(ads_tags, 500):
            ServerTag.insert_many(batch).execute()


def make_tags_ex(server_ads):

    tags: List[Tags] = Tags.select()

    tags_re_compile_dict = {tag.id: re.compile(tag.reg_exp) for tag in tags}

    for server_ad in server_ads:
        server_ad_text = server_ad["name"]+server_ad["ip"] + \
            server_ad["route"]+server_ad["description"]+server_ad["service"]
        for id, compile in tags_re_compile_dict.items():
            if compile.search(server_ad_text):
                yield {"server_id": server_ad['id'], "tag_id": id}


@async_print_run_time
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
        records_db, crawler_data, publish_source)

    ads_tags = make_tags_ex(server_ad)

    save_crawled_data(server_ad, server_ad_count,
                      publish_source, ads_tags, current_time)


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
    #
    c = re.compile(r'(?:今日|(?:(\d)+月)?(?:(\d+)日/))(?:(\d+):)?(\d+)?')

    sss = ["""今日22:30""", '01月13日/18:30', '01月11日/通宵推荐']

    for s in sss:
        res = c.search(s)
        print(res.groups())
