#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import os

from io import StringIO

import boto3
import paramiko
import sys
from base64 import b64decode

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    kms_client = boto3.client('kms')
    ssh_username = \
        kms_client.decrypt(CiphertextBlob=b64decode(os.environ['SSH_USERNAME'
                           ]))['Plaintext']
    ssh_host = \
        kms_client.decrypt(CiphertextBlob=b64decode(os.environ['SSH_HOST'
                           ]))['Plaintext']
    ssh_dir = \
        kms_client.decrypt(CiphertextBlob=b64decode(os.environ['SSH_DIR'
                           ]))['Plaintext']
    ssh_port = \
        int(kms_client.decrypt(CiphertextBlob=b64decode(os.environ.get('SSH_PORT'
            , 22)))['Plaintext'])
    ssh_password = \
        kms_client.decrypt(CiphertextBlob=b64decode(os.environ.get('SSH_PASSWORD'
                           )))['Plaintext']

    pkey = None

    (sftp, transport) = connect_to_SFTP(hostname=ssh_host,
            port=ssh_port, username=ssh_username,
            password=ssh_password, pkey=pkey)
    s3 = boto3.client('s3')
    if ssh_dir:
        try:
            sftp.chdir(ssh_dir)
        except Exception:
            logger.error('Could not change the directory')
            raise
        else:
            logger.info('successfully changed directory')

    with transport:
        for record in event['Records']:
            uploaded = record['s3']
            filename = uploaded['object']['key'].split('/')[-1]

            try:
                transfer_file(s3_client=s3, bucket=uploaded['bucket'
                              ]['name'], key=uploaded['object']['key'],
                              sftp_client=sftp, sftp_dest=filename)
            except Exception:
                logger.error('Could not upload file to SFTP')
                raise
            else:

                logger.info('S3 file  uploaded to SFTP successfully')


def connect_to_SFTP(
    hostname,
    port,
    username,
    password,
    pkey,
    ):
    transport = paramiko.Transport((hostname, port))
    transport.connect(username=username, password=password, pkey=pkey)
    sftp = paramiko.SFTPClient.from_transport(transport)

    return (sftp, transport)


def transfer_file(
    s3_client,
    bucket,
    key,
    sftp_client,
    sftp_dest,
    ):
    """
    Download file from S3 and upload to SFTP
    """

    with sftp_client.file(sftp_dest, 'w') as sftp_file:

        try:
            s3_client.download_fileobj(Bucket=bucket, Key=key,
                    Fileobj=sftp_file)
        except Exception:
            logger.error('Could not Download file from S3 and upload to SFTP'
                         )
            raise
        else:

            logger.info('Download file from S3 and upload to SFTP successfully'
                        )
