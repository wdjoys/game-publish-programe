# -*- coding: utf-8 -*-
# @Author: xiaocao
# @Date:   2023-01-07 14:26:05
# @Last Modified by:   xiaocao
# @Last Modified time: 2023-01-08 23:32:01


import re
import time
import datetime
from typing import List
import aiohttp
import asyncio

from peewee import chunked
from db.db import PublishSource, Servers, database

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


def resolver(html, publish_source: PublishSource):
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
        yield {
            'timestamp': time_format(year, record[publish_source.located_time], publish_source),
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
        hour = int(result[3])
        minute = int(result[4]) if result[4] else 0

        return datetime.datetime(year, month, day, hour, minute)
    else:
        raise ValueError


def remove_duplicates_for_db(source):
    """与数据库对比，去除数据库内已经存在的记录

    Args:
        source (_type_): _description_

    Returns:
        _type_: _description_
    """

    return list(set(source))


def marks_counters_for_record(source):
    """标记广告条数

    Args:
        source (_type_): _description_

    Returns:
        _type_: _description_
    """

    for record in source:
        sorted()


def load_publish_source_config() -> List[PublishSource]:
    """加载采集配置文件

    Returns:
        _type_: _description_
    """

    return PublishSource.select().where(PublishSource.active == True)


def save_servers(servers, publish_source):
    """保存servers

    Args:
        servers (_type_): _description_
        publish_source (_type_, optional): _description_. Defaults to None.

    Returns:
        _type_: _description_
    """

    publish_source.last_run_time = time.time()
    publish_source.save()
    print("存入数据库", publish_source)

    with database.atomic():

        for batch in chunked(servers, 100):
            Servers.insert_many(batch).execute()


async def collect(publish_source: PublishSource):
    """采集网页信息并存入数据库

    Args:
        publish_source (_type_, optional): _description_. Defaults to None.

    Returns:
        _type_: _description_
    """

    html = await get_html(publish_source.url, headers=HEADERS, charset=publish_source.charset)
    result = resolver(html, publish_source)
    save_servers(result, publish_source)


async def async_run():

    while True:

        publish_source_list = load_publish_source_config()
        tasks = [asyncio.create_task(collect(publish_source), name=f'任务-{publish_source.id}')
                 for publish_source in publish_source_list]

        tasks and await asyncio.wait(tasks)
        await asyncio.sleep(10)


def run():
    print("爬虫 Running...")
    asyncio.run(async_run())


if __name__ == "__main__":
    import time
    print(time.gmtime()
          )
