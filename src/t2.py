# -*- coding: utf-8 -*-
# @Author: xiaocao
# @Date:   2023-01-12 15:31:11
# @Last Modified by:   xiaocao
# @Last Modified time: 2023-01-12 16:42:47


# the result string and convert the values to python ints.


from db.db import ServersAdCount, ServersAd
if __name__ == "__main__":

    from peewee import fn

    def convert_ids(s): return [int(i) for i in (s or '').split(',') if i]

    ids = (fn
           .GROUP_CONCAT(ServersAdCount.source)
           .python_value(convert_ids))

    result = ServersAdCount.select(ServersAd.id.alias("ssss"), ServersAd.url, ServersAd.timestamp, ids.alias(
        "ids")).join(ServersAd, on=(ServersAdCount.game == ServersAd.id)).group_by(ServersAdCount.game).where(
        ServersAd.timestamp > 0)

    for user in result:
        print(user.serversad.timestamp, user.ids,
              user.serversad.url, user.ssss)
