# -*- coding: utf-8 -*-
# @Author: xiaocao
# @Date:   2023-01-07 14:16:19
# @Last Modified by:   xiaocao
# @Last Modified time: 2023-01-17 10:18:47

from fastapi import FastAPI
from web.views.data import router as data_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(data_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],

    allow_methods=["*"],
    allow_headers=["*"],
)


def run():
    import uvicorn
    uvicorn.run("web.main:app", host="0.0.0.0", port=9090)


if __name__ == "__main__":
    run()
