import asyncio
import urllib.parse

import base64
import io
import os


import aioboto3
from dotenv import load_dotenv

load_dotenv()

ACCESS_KEY = os.getenv("AWS_KEY")
ACCESS_SECRET = os.getenv("AWS_SECRET")
session = aioboto3.Session(
    aws_access_key_id=ACCESS_KEY, aws_secret_access_key=ACCESS_SECRET
)


async def download_file_by_uri(uri: str) -> str:
    # Parse the URI to extract bucket and object key
    parsed_uri = urllib.parse.urlparse(uri)
    bucket_name = parsed_uri.netloc
    object_key = parsed_uri.path.lstrip("/")

    async with session.resource("s3") as s3:
        bucket = await s3.Bucket(bucket_name)
        try:
            file = io.BytesIO()
            await bucket.download_fileobj(object_key, file)
            print("File successfully downloaded")
            file.seek(0)
            base64_str = base64.b64encode(file.read()).decode("utf-8")
            return base64_str
        except Exception as e:
            print("AWS File not found")


if __name__ == "__main__":
    uri = "s3://resources-image-ai/653a8b6943ce4bc1f6985d5b_3.png"
    asyncio.run(download_file_by_uri(uri))
