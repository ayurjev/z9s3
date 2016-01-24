""" Модели """

import os
import boto3
import random
from io import BytesIO
from datetime import datetime
from exceptions import *


AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_DEFAULT_REGION = os.environ.get("AWS_DEFAULT_REGION")
S3BUCKET = os.environ.get("S3BUCKET")
S3CONTENTTYPE = os.environ.get("S3CONTENTTYPE")
S3BUCKETURL = os.environ.get("S3BUCKETURL")
CFBUCKETURL = os.environ.get("CFBUCKETURL")


if not AWS_ACCESS_KEY_ID:
    raise S3ConfigurationException("AWS_SECRET_ACCESS_KEY env variable is not defined")

if not AWS_SECRET_ACCESS_KEY:
    raise S3ConfigurationException("AWS_SECRET_ACCESS_KEY env variable is not defined")

if not AWS_DEFAULT_REGION:
    raise S3ConfigurationException("AWS_DEFAULT_REGION env variable is not defined")

if not S3BUCKET:
    raise S3ConfigurationException("S3BUCKET env variable is not defined")

if not S3BUCKETURL:
    raise S3ConfigurationException("S3BUCKETURL env variable is not defined")

if not S3CONTENTTYPE:
    raise S3ConfigurationException("S3CONTENTTYPE env variable is not defined")

if not S3BUCKETURL.endswith("/"):
    S3BUCKETURL += "/"

if CFBUCKETURL and not CFBUCKETURL.endswith("/"):
    CFBUCKETURL += "/"


class S3Uploader(object):
    """ Класс для работы с S3 """
    def __init__(self):
        self.s3 = boto3.resource('s3')

    def upload(self, file_obj: BytesIO):
        """ Выполняет загрузку файла в сгенерированный самостоятельно ключ
        :param file_obj:
        :return:
        """
        key = "%s%s.jpg" % (datetime.now().strftime("%Y%m%d%H%M%S%f"), random.randint(1,10000))
        return self.upload_with_key(key, file_obj)

    def upload_with_key(self, key: str, file_obj: BytesIO):
        """
        Выполняет загрузку файла в указанный ключ
        :param key:
        :param file_obj:
        :return:
        """
        try:
            self.s3.Bucket(S3BUCKET).put_object(Key=key, Body=file_obj, ContentType=S3CONTENTTYPE)
            return key, "%s%s" % (CFBUCKETURL or S3BUCKETURL, key)
        except Exception as err:
            raise UploadFailed(str(err))

    def delete(self, key: str):
        """
        Выполняет удаление файла по указанному ключу
        :param key:
        :return:
        """
        # noinspection PyBroadException
        try:
            obj = self.s3.Object(bucket_name=S3BUCKET, key=key)
            if obj:
                obj.delete()
                return True
        except Exception:
            pass
        return False