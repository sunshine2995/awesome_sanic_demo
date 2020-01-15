# -*- coding:utf-8 -*-

import shutil
from io import BytesIO

import oss2 as oss2

access_key_id = ""
access_key_secret = ""
endpoint = ""
bucket_name = ""


def upload_file(server_file_path, data, data_type, **other_headers):
    """
        上传文件到OSS
        参数：
            server_file_path：上传路径
            data：要上传的文件数据
            data_type：MIME类型
            other_headers：其他头部信息
    """
    bucket = __get_bucket(bucket_name)

    headers = (
        dict({"Content-Type": data_type}, **other_headers)
        if data_type
        else other_headers
    )

    result = bucket.put_object(server_file_path, data, headers=headers)

    return result.status == 200


def download_file(server_file_path):
    """
        下载OSS文件
        参数：
            server_file_path：下载路径
    """
    bucket = __get_bucket(bucket_name)
    remote_stream = bucket.get_object(server_file_path)
    buf = BytesIO()
    shutil.copyfileobj(remote_stream, buf)

    return buf.getvalue()


def upload_local_files(server_file_path: str, local_file_path: str) -> bool:
    """
        上传本地文件到OSS
        参数：
            server_file_path：上传路径
            local_file_path：本地路径
    """
    bucket = __get_bucket(bucket_name)
    result = bucket.put_object_from_file(server_file_path, local_file_path)
    return result.status == 200


def download_local_files(server_file_path, local_file_path):
    """
        OSS下载到本地文件
        参数：
            server_file_path：oss路径
            local_file_path：本地路径
    """
    bucket = __get_bucket(bucket_name)
    result = bucket.get_object_to_file(server_file_path, local_file_path)
    return result.status == 200


def __get_bucket(b_name):
    auth = oss2.Auth(access_key_id, access_key_secret)
    return oss2.Bucket(auth, endpoint, b_name)
