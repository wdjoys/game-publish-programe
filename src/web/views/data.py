# -*- coding: utf-8 -*-
# @Author: xiaocao
# @Date:   2023-01-11 11:42:43
# @Last Modified by:   xiaocao
# @Last Modified time: 2023-01-11 15:42:58

import datetime
from fastapi import APIRouter

from db.db import ServersAd


router = APIRouter(
    prefix="/data",
    tags=["data"]
)


@router.get('/', )
async def get_ads():
    current_time = datetime.datetime.now()
    today = datetime.datetime(
        current_time.year, current_time.month, current_time.day,)

    result = ServersAd.select().where(ServersAd.timestamp > today)
    return list(result.tuples().iterator())
