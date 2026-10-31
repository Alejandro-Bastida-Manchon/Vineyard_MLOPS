import os

import boto3
from botocore.config import Config

BUCKET = os.environ.get("S3_BUCKET", "vineyard-data")


def get_s3():
    return boto3.client(
        "s3",
        endpoint_url=os.environ["S3_ENDPOINT_URL"],
        region_name="us-east-1",
        config=Config(s3={"addressing_style": "path"}),
    )


def list_keys(prefix: str) -> list[str]:
    """Lista las claves (rutas) de todos los objetos bajo un prefijo."""
    keys = []
    paginator = get_s3().get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=BUCKET, Prefix=prefix):
        keys += [o["Key"] for o in page.get("Contents", []) if not o["Key"].endswith("/")]
    return keys