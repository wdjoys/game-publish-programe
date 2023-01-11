# -*- coding: utf-8 -*-
# @Author: xiaocao
# @Date:   2023-01-07 14:16:19
# @Last Modified by:   xiaocao
# @Last Modified time: 2023-01-11 15:51:26

from fastapi import FastAPI
from web.views.data import router as data_router


app = FastAPI()

app.include_router(data_router)


def run():
    import uvicorn
    uvicorn.run("web.main:app", port=9090)


if __name__ == "__main__":
    run()
