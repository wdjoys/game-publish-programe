# -*- coding: utf-8 -*-
# @Author: xiaocao
# @Date:   2023-01-07 18:11:15
# @Last Modified by:   xiaocao
# @Last Modified time: 2023-02-03 17:58:05
from peewee import *
from setting import DATABASE


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = DATABASE


class PublishSource(BaseModel):
    active = IntegerField()
    charset = CharField()
    last_run_time = DateTimeField()
    located_description = IntegerField()
    located_ip = IntegerField()
    located_name = IntegerField()
    located_route = IntegerField()
    located_service = IntegerField()
    located_time = IntegerField()
    located_time_d = IntegerField()
    located_time_h = IntegerField()
    located_time_min = IntegerField()
    located_time_month = IntegerField()
    located_url = IntegerField()
    record_reg_exp = CharField()
    time_reg_exp = CharField()
    url = CharField()
    name = CharField()

    class Meta:
        table_name = 'publish_source'


class ServerTag(BaseModel):
    server_id = IntegerField()
    tag_id = IntegerField()

    class Meta:
        table_name = 'server_tag'
        primary_key = False


class ServersAd(BaseModel):
    description = CharField(null=True)
    ip = CharField(null=True)
    name = CharField(null=True)
    route = CharField(null=True)
    service = CharField(null=True)
    timestamp = DateTimeField(null=True)
    url = CharField(null=True)

    class Meta:
        table_name = 'servers_ad'


class ServersAdCount(BaseModel):
    count = IntegerField(null=True)
    game = IntegerField(null=True)
    source = IntegerField(null=True)

    class Meta:
        table_name = 'servers_ad_count'
        primary_key = False


class Tags(BaseModel):
    name = CharField(null=True)
    reg_exp = CharField(null=True)

    class Meta:
        table_name = 'tags'


if __name__ == "__main__":

    from peewee import fn

    def convert_ids(s): return [int(i) for i in (s or '').split(',') if i]

    ids = (fn
           .GROUP_CONCAT(ServersAdCount.source)
           .python_value(convert_ids))

    result = ServersAdCount.select(ServersAd.id, ServersAd.url, ServersAd.timestamp, ids.alias(
        "ids")).join(ServersAd, on=(ServersAdCount.game == ServersAd.id)).group_by(ServersAdCount.game).where(
        ServersAd.id.between(83815, 83865))

    for g in result:
        print(g.serversad.id, g.ids)
