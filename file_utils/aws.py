import boto3
from botocore.exceptions import ClientError

from django.conf import settings

from file_utils import consts
from file_utils.base import FileServiceInterface


class AwsFileService(FileServiceInterface):
    def get_file_url(self, filename: str) -> str:
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )
        try:
            response = s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": settings.AWS_STORAGE_BUCKET_NAME, "Key": filename},
                ExpiresIn=consts.AWS_EXPIRATION,
            )
        except ClientError as e:
            return ""

        return response
