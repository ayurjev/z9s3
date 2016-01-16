""" Контроллеры сервиса """

import json
import base64
from io import BytesIO
from envi import Controller as EnviController, Request
from exceptions import BaseServiceException
from models import S3Uploader

uploader = S3Uploader()


def error_format(func):
    """ Декоратор для обработки любых исключений возникающих при работе сервиса
    :param func:
    """
    def wrapper(*args, **kwargs):
        """ wrapper
        :param args:
        :param kwargs:
        """
        try:
            return func(*args, **kwargs)
        except BaseServiceException as e:
            return json.dumps({"error": {"code": e.code}})
    return wrapper


class Controller(EnviController):
    """ Контроллер """

    @classmethod
    @error_format
    def upload(cls, request: Request, **kwargs):
        """ Метод для загрузки файла с любым ключом
        :param request:
        :param kwargs:
        :return:
        """
        if request.get_file("file"):
            file_name, file_body = request.get_file("file")
            file_obj = BytesIO(file_body)
        else:
            file_obj = BytesIO(base64.b64decode(request.get("base64").replace(" ", "+").encode()))
        key, url = uploader.upload(file_obj)
        return {"key": key, "url": url}

    @classmethod
    @error_format
    def upload_with_key(cls, request: Request, **kwargs):
        """ Метод для загрузки файла с указанным ключом
        :param request:
        :param kwargs:
        :return:
        """
        key = request.get("key")
        if request.get_file("file"):
            file_name, file_body = request.get_file("file")
            file_obj = BytesIO(file_body)
        else:
            file_obj = BytesIO(base64.b64decode(request.get("base64").replace(" ", "+").encode()))
        key, url = uploader.upload_with_key(key, file_obj)
        return {"key": key, "url": url}

    @classmethod
    @error_format
    def delete(cls, request: Request, **kwargs):
        """ Метод для удаления файла с указанным ключом
        :param request:
        :param kwargs:
        :return:
        """
        key = request.get("key")
        return uploader.delete(key)