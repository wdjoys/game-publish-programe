# -*- coding: utf-8 -*-
# @Author: xiaocao
# @Date:   2023-01-07 14:16:19
# @Last Modified by:   xiaocao
# @Last Modified time: 2023-01-07 14:27:41

from fastapi import FastAPI

app = FastAPI()


def run():
    import uvicorn
    uvicorn.run("web.main:app", port=7000)


if __name__ == "__main__":
    run()
