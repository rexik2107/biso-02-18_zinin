import types
from typing import Any, Callable, Tuple

from aiohttp import web
import ujson
import traceback

from middlewares.exceptions import InputDataValidationError
from middlewares.utils import json_dumps
from log import logger


class SimpleHandler:
    """ Класс для middleware json-обработчиков api-методов.

        Каждый обработчик должен иметь только два аргумента с произвольными
        именами:

        1. В первый будет отправлен оригинальный request.
        2. Во второй - результат request.json().
    """
    def get_error_body(self, request: web.Request, error: Exception) -> dict:
        """ Отдает словарь с телом ответа с ошибкой.

            (Этот метод надо переопределять, если нужен другой формат ответа)
        """
        return {"type": "error", "error_type": str(type(error)), "error_message": str(error)}

    def is_json_service_handler(
        self, request: web.Request, handler: Callable
    ) -> bool:
        """ Проверяет, является ли handler обработчиком сервиса.
        """
        # TODO Возможно, есть решение получше
        return isinstance(handler, types.FunctionType)

    async def run_handler(
        self, request: web.Request, handler: Callable, request_body: Any
    ) -> Any:
        """ Запускает реальный обработчик, и возвращает результат его работы.

            (Этот метод надо переопределять, если необходима дополнительная
            обработка запроса/ответа/исключений)
        """
        #print(11111111111)
        #await handler(request, request_body)
        #print(11111111111)
        return await handler(request, request_body)

    async def get_response_body_and_status(
        self, request: web.Request, handler: Callable, request_body: Any
    ) -> Tuple[Any, int]:
        """ Вызывает метод запуска обработчика и обрабатывает возможные
            ошибки.
            Возвращает объект с телом для ответа и код статуса ответа.
        """
        try:
            response_body = await self.run_handler(
                request, handler, request_body
            )
            status = 200

        except InputDataValidationError as error:
            response_body = self.get_error_body(request, traceback.format_exc())
            #response_body = self.get_error_body(request, error)
            status = 400

        #except Exception as error:
        except Exception as e:
            #print(traceback.format_exc())
            response_body = self.get_error_body(request, traceback.format_exc())
            status = 500

        return response_body, status

    async def get_json_dumps(
        self, request: web.Request, response_body: Any
    ) -> str:
        """ Возвращает json-строку с дампом response_body.
        """
        return ujson.dumps(response_body)

    async def get_response_text_and_status(
        self, request: web.Request, response_body: Any, status: int
    ) -> Tuple[str, int]:
        """ Обрабатывает ошибку дампа объекта python в строку.
            Возвращает json-строку для ответа и код статуса ответа.
        """
        try:
            text = await self.get_json_dumps(request, response_body)

        #except Exception as error:
        except Exception as e:
            # print(traceback.format_exc())
            #response_body = self.get_error_body(request, traceback.format_exc())
            error_body = self.get_error_body(request, traceback.format_exc())
            text = await self.get_json_dumps(request, error_body)
            status = 500

        return text, status

    async def get_request_body(
        self, request: web.Request, handler: Callable
    ) -> Any:

        return await request.json(loads=ujson.loads)

    async def get_request_body_get(
        self, request: web.Request, handler: Callable
    ) -> Any:
        result = {}
        for i in iter(request.rel_url.query):
            result[i] = request.rel_url.query.get(i)
        return result  # await request.json(loads=ujson.loads)

    @web.middleware
    async def middleware(self, request: web.Request, handler: Callable):
        """ middleware для json-сервиса.
        """
        #print(request.text, "|||||", handler)
        if not self.is_json_service_handler(request, handler):
            return await handler(request)

        try:
            logger.error(request.rel_url.query)
            if request.method == "POST":
                request_body = await self.get_request_body(request, handler)
            elif request.method == "GET":
                request_body = await self.get_request_body_get(request, handler)

        except Exception as error:
            print(error)
            response_body = self.get_error_body(request, traceback.format_exc())
            status = 400

        else:
            # Запуск обработчика
            response_body, status = await self.get_response_body_and_status(
                request, handler, request_body
            )

        finally:
            # Самостоятельно делаем дамп объекта python (который находится в
            # response_body) в строку json.
            text, status = await self.get_response_text_and_status(
                request, response_body, status
            )
        #return response_body
        return web.Response(
            text=text, status=status,  content_type="application/json",
        )
