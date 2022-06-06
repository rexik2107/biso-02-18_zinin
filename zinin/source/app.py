
import importlib
import os

from aiohttp import web
import aiohttp_cors

from commands import command_list
from middlewares.simple_handler import SimpleHandler
from log import logger


def getsubs(dir):

    dirs = []

    files = []

    for dirname, dirnames, filenames in os.walk(dir):

        dirs.append(dirname)

        for subdirname in dirnames:

            dirs.append(os.path.join(dirname, subdirname))

        for filename in filenames:

            files.append(os.path.join(dirname, filename))

    return dirs, files

def get_files(folder):
    files_list = os.listdir(path=folder)
    for i in files_list.copy():
        if "." in i or "__" in i:
            files_list.remove(i)
    return files_list

def load_modules(file):


    files_list = get_files(f"{file}")
    for i in files_list:
        files = os.listdir(f"{file}/{i}")
        modules = filter(lambda x: x.endswith('.py'), files)
        for m in modules:
            importlib.import_module(f"{file}.{i}." + m[0:-3])
    # for n in modules_ls:
    #     importlib.import_module("commands_ls." + n[0:-3])
    return

# if __name__ == "__main__":
#     #print(os.listdir(path="views"))
#     #print(get_files("views"))
#     load_modules("views")
    #print(getsubs("views"))
    #load_modules("command")


def test():
    load_modules("command")

def get_route(file, app):
    routes = []
    cache = []
    load_modules(f"{file}")

    # hello_resource = cors.add(app.router.add_resource("/hello"))
    # cors.add(hello_resource.add_route("POST", handler_post))
    # cors.add(hello_resource.add_route("PUT", handler_put))
    #
    # # In addition to "http://client.example.org", GET request will be
    # # allowed from "http://other-client.example.org" origin.
    # cors.add(hello_resource.add_route("GET", handler), {
    #     "http://other-client.example.org":
    #         aiohttp_cors.ResourceOptions(),
    # })

    for i in command_list:
        for j in i.definitions:
            for num, rout in enumerate(i.definitions[j][1], start=1):  # for i, data in enumerate(calc_list, start=1):
                #logger.error(f"{rout}     |    {j}")
                if f"{rout}|{j[0]}" in cache:
                    continue
                #if num == 1:
                    #resource = cors.add(app.router.add_resource(f"{j[0]}"))
                #routes.append(cors.add(resource.add_route(rout, i.definitions[j][0])))
                # if f"{rout}|{j[0]}" in cache:
                #     continue
                if rout == "POST":
                    routes.append(web.post(f"{j[0]}", i.definitions[j][0]))
                elif rout == "GET":
                    #logger.error(f"{rout}     |    {j[0]}")
                    #logger.error(f"{j}", i.definitions[j][0])
                    routes.append(web.get(f"{j[0]}", i.definitions[j][0]))
                elif rout == "DELETE":
                    routes.append(web.delete(f"{j[0]}", i.definitions[j][0]))
                cache.append(f"{rout}|{j[0]}")

    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
            #allow_headers=ALLOWED_CORS_HEADERS,
        )
    })
    app.add_routes(routes)
    for route in list(app.router.routes()):
        cors.add(route)
            # web.post(f"{j}", i.definitions[j][0])
            # routes.append([i.definitions[j]])
    #print(routes)
    logger.error(routes)
    return routes

def get_app(file) -> web.Application:

    app = web.Application()

    routes = get_route(file, app)

    # cors = aiohttp_cors.setup(app)
    #
    # resource = cors.add(app.router.add_resource("/hello"))
    # route = cors.add(
    #     resource.add_route("GET", handler), {
    #         "http://client.example.org": aiohttp_cors.ResourceOptions(
    #             allow_credentials=True,
    #             expose_headers="*",
    #             allow_headers="*",
    #         )
    #     })


    #app.add_routes(routes)
    service_handler = SimpleHandler()

    app.middlewares.append(service_handler.middleware)



    return app


# if __name__ == "__main__":
#     routes = [
#         web.post("/bots", bots)
#         #web.post("/api_django/send_sms", send_sms),
#     ]
#
#     app = get_app()

async def run():
    # routes = [
    #         web.post("/bots", bots),
    #         web.post("/bots", bots)
    #         #web.post("/api_django/send_sms", send_sms),
    #     ]
    file = "views"
    app = get_app(file)
    return app

    #web.run_app(app, host="127.0.0.1", port=8000)
