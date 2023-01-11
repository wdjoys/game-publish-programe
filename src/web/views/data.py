# -*- coding: utf-8 -*-
# @Author: xiaocao
# @Date:   2023-01-11 11:42:43
# @Last Modified by:   xiaocao
# @Last Modified time: 2023-01-11 17:44:39

import datetime
from fastapi import APIRouter

from db.db import ServersAd


router = APIRouter(
    prefix="/data",
    tags=["data"]
)


CACHE_AD = {
    'expiration_time': datetime.datetime.now(),
    'data': []
}


@router.get('/', )
async def get_ads():
    current_time = datetime.datetime.now()

    global CACHE_AD

    if CACHE_AD['expiration_time'] < current_time:

        today = datetime.datetime(
            current_time.year, current_time.month, current_time.day,)

        result = ServersAd.select().where(ServersAd.timestamp > today)

        CACHE_AD = {
            'expiration_time': current_time+datetime.timedelta(seconds=60),
            'data': list(result.tuples().iterator())
        }
        print("没走缓存")

    return CACHE_AD['data']
