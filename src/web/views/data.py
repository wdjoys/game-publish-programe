# -*- coding: utf-8 -*-
# @Author: xiaocao
# @Date:   2023-01-11 11:42:43
# @Last Modified by:   xiaocao
# @Last Modified time: 2023-01-12 10:42:39

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


Test = [
    [
        16594,
        "不卖装备●全部靠打●公平起步●长久服",
        "保底●回А褚磺",
        "１８５雷霆③合①",
        "雷霆③合①",
        "免费合成终极",
        "2023-01-12T23:59:00",
        "http://www.0818pk.com"
    ],
]


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

    return CACHE_AD['data']


@router.get('/1', )
async def get_ads():

    return CACHE_AD['data']


@router.get('/2', )
async def get_ads():

    return Test


@router.get('/3', )
async def get_ads():

    current_time = datetime.datetime.now()

    today = datetime.datetime(
        current_time.year, current_time.month, current_time.day,)

    result = ServersAd.select().where(ServersAd.timestamp > today)

    return list(result.tuples().iterator())
