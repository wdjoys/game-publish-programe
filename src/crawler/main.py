# -*- coding: utf-8 -*-
# @Author: xiaocao
# @Date:   2023-01-07 14:26:05
# @Last Modified by:   xiaocao
# @Last Modified time: 2023-01-08 00:36:52


import time
from typing import List
import aiohttp
import asyncio

from db.db import PublishSource, Servers

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
}


async def get_html(url, headers=HEADERS):
    """获取网页html

    Args:
        url (_type_): _description_
        headers (_type_, optional): _description_. Defaults to HEADERS.

    Returns:
        _type_: _description_
    """

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            return await resp.text()


def resolver(html, publish_source):
    """解析网页html

    Args:
        html (_type_): _description_
        publish_source (_type_, optional): _description_. Defaults to None.

    Returns:
        _type_: _description_
    """
    pass


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


async def collect(publish_source: PublishSource):
    """采集网页信息并存入数据库

    Args:
        publish_source (_type_, optional): _description_. Defaults to None.

    Returns:
        _type_: _description_
    """

    html = await get_html(publish_source.url, headers=HEADERS)
    result = resolver(html, publish_source)
    save_servers(result, publish_source)


async def async_run():

    while True:

        publish_source_list = load_publish_source_config()
        tasks = [asyncio.create_task(collect(publish_source))
                 for publish_source in publish_source_list]
        await asyncio.wait(tasks)
        await asyncio.sleep(5)


def run():
    print("爬虫 Running...")
    asyncio.run(async_run())


if __name__ == "__main__":
    run()
