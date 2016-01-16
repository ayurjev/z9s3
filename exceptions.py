
""" Исключения """


class BaseServiceException(Exception):
    """ Базовый класс исключений """
    code = 0


class UploadFailed(BaseServiceException):
    """ Загрузка не удалась """
    code = 1


class S3ConfigurationException(BaseServiceException):
    """ Не хватает переменных окружения """
    code = 2