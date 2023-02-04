# -*- coding: utf-8 -*-
# @Author: xiaocao
# @Date:   2023-01-11 11:42:43
# @Last Modified by:   xiaocao
# @Last Modified time: 2023-02-04 14:40:20

import datetime
from fastapi import APIRouter

from db.db import ServerTag, ServersAd, ServersAdCount, Tags, PublishSource
from peewee import fn, Case, JOIN

router = APIRouter(prefix="/data", tags=["data"])

# 广告内容的全局缓存
CACHE_AD = {"expiration_time": datetime.datetime.now(), "data": []}


def get_ads(startTime: datetime.datetime, endTime: datetime.datetime = None):
    if not endTime:
        endTime = startTime + datetime.timedelta(days=7)

    # 查询出采集源配置
    source_configs = list(
        PublishSource().select(PublishSource.id, PublishSource.name).dicts()
    )

    # 动态构造字段
    case_list = [
        fn.MAX(
            Case(
                None,
                ((ServersAdCount.source == source_config["id"], ServersAdCount.count),),
                0,
            )
        ).alias(source_config["name"])
        for source_config in source_configs
    ]

    # 分割函数
    def convert_ids(s):
        return [int(i) for i in (s or "").split(",") if i]

    # tags 字段
    tags = (
        fn.GROUP_CONCAT(ServerTag.tag_id.distinct())
        .python_value(convert_ids)
        .alias("tags")
    )

    result = (
        ServersAd()
        .select(
            ServersAd.name,
            ServersAd.route,
            ServersAd.ip,
            ServersAd.timestamp,
            ServersAd.description,
            ServersAd.service,
            ServersAd.url,
            *case_list,
            tags
        )
        .join(
            ServersAdCount,
            on=(ServersAdCount.game == ServersAd.id),
            join_type=JOIN.LEFT_OUTER,
        )
        .join(
            ServerTag,
            on=(ServerTag.server_id == ServersAd.id),
            join_type=JOIN.LEFT_OUTER,
        )
        .where(ServersAd.id.between(35183, 83899))
        .group_by(ServersAdCount.game, ServerTag.server_id)
    )

    for server in result:
        yield [
            [
                server.name,
                server.ip,
                server.timestamp,
                server.route,
                server.description,
                server.service,
                server.url,
            ],
            {
                source_config["name"]: getattr(server, source_config["name"])
                for source_config in source_configs
            },
            server.tags,
        ]


@router.get(
    "/ad/",
)
async def ad():
    """获取今天0点及以后得开区数据

    Returns:
        _type_: _description_
    """

    current_time = datetime.datetime.now()

    global CACHE_AD

    # 判断是否到期
    if CACHE_AD["expiration_time"] < current_time:
        # 今天0点
        today = datetime.datetime(
            current_time.year,
            current_time.month,
            current_time.day,
        )

        # 查出今天0点及以后的广告　根据时间升序排列
        result = get_ads(today)
        # 广告更新到缓存
        CACHE_AD = {
            # 缓存到期时间为当前时间 增加60秒
            "expiration_time": current_time + datetime.timedelta(seconds=60),
            "data": list(result),
        }

    # 从缓存返回广告数据
    return CACHE_AD["data"]


@router.get(
    "/tag/",
)
async def tag():
    """获取服务器的tags配置

    Returns:
        _type_: _description_
    """
    result = Tags.select()
    return list(result.dicts())


@router.get(
    "/source/",
)
async def source():
    """获取采集源配置

    Returns:
        _type_: _description_
    """
    result = PublishSource.select(PublishSource.id, PublishSource.name)
    return list(result.dicts())


if __name__ == "__main__":
    pass
