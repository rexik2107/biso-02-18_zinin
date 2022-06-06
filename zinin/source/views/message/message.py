
from aiohttp import web


from settings import *


from commands import Command
from log import logger

cmd = Command()


@cmd('/sendMessage', methods=["POST", "OPTIONS"])
#@cross_origin()
async def send_message(request: web.Request, data: dict):
    db_mongo.send_message(data["name"], data["message"])

    return {
            "type": "ok",
        }