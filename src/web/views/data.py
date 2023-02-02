# -*- coding: utf-8 -*-
# @Author: xiaocao
# @Date:   2023-01-11 11:42:43
# @Last Modified by:   xiaocao
# @Last Modified time: 2023-02-02 16:07:10

import datetime
from fastapi import APIRouter

from db.db import ServersAd


router = APIRouter(
    prefix="/data",
    tags=["data"]
)


# 广告内容的全局缓存
CACHE_AD = {
    'expiration_time': datetime.datetime.now(),
    'data': []
}


@router.get('/', )
async def get_ads():

    current_time = datetime.datetime.now()

    global CACHE_AD

    # 判断是否到期
    if CACHE_AD['expiration_time'] < current_time:

        # 今天0点
        today = datetime.datetime(
            current_time.year, current_time.month, current_time.day,)

        # 查出今天0点及以后的广告　根据时间升序排列
        result = ServersAd.select().where(ServersAd.timestamp >
                                          today).order_by(+ServersAd.timestamp)
        # 广告更新到缓存
        CACHE_AD = {
            # 缓存到期时间为当前时间 增加60秒
            'expiration_time': current_time+datetime.timedelta(seconds=60),
            'data': list(result.tuples().iterator())
        }

    # 从缓存返回广告数据
    return CACHE_AD['data']
