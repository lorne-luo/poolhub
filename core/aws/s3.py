from datetime import datetime

import boto3
import logging

from botocore.exceptions import ClientError
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)

s3_client = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                         aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)


class AWSS3URLs(object):
    """generate presigned url for aws s3"""
    https = (not settings.DEBUG)

    @classmethod
    def get_url(cls, relative_path, expires_in=3600, http_method='GET'):
        try:
            url = s3_client.generate_presigned_url(ClientMethod='get_object',
                                                   Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                                                           'Key': relative_path},
                                                   ExpiresIn=expires_in,
                                                   HttpMethod=http_method)
            return url
        except ClientError as e:
            logging.error(e)
            return None

    @classmethod
    def upload_url(cls, object_name='', fields=None, conditions=None, expiration=3600):
        fields = fields or {}
        expired_at = timezone.now() + relativedelta(seconds=expiration - 120)
        expired_at = datetime.timestamp(expired_at)

        try:
            response = s3_client.generate_presigned_post(settings.AWS_STORAGE_BUCKET_NAME,
                                                         object_name,
                                                         Fields=fields,
                                                         Conditions=conditions,
                                                         ExpiresIn=expiration)

            response['expired_at'] = expired_at
            return response
        except ClientError as e:
            logging.error(e)
            return None
