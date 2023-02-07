# -*- coding: utf-8 -*-
# @Author: xiaocao
# @Date:   2023-01-07 14:16:19
# @Last Modified by:   xiaocao
# @Last Modified time: 2023-02-07 11:26:41

from fastapi import FastAPI
from web.views.data import router as data_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

app = FastAPI()

app.include_router(data_router)

# 开启Gzip压缩 level=2
app.add_middleware(GZipMiddleware, minimum_size=1000, compresslevel=3)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def run():
    import uvicorn

    uvicorn.run("web.main:app", host="0.0.0.0", port=9090)


if __name__ == "__main__":
    run()
