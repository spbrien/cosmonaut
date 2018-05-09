# -*- coding: utf-8 -*-

"""Main module."""

import os

import magic
import click

import bucketstore

mime = magic.Magic(mime=True)


def get_bucket(name):
    return bucketstore.get(name, create=True)

def get_file_list(_dir):
    path = os.path.expanduser(_dir) if _dir.startswith('~') else _dir
    if os.path.isfile(path):
        return [path]

    return (
        os.path.join(dp, f)
        for dp, dn, filenames
        in os.walk(path)
        for f in filenames
    )


def get_mime_type(f):
    filename, file_extension = os.path.splitext(f)

    if 'js' in file_extension:
        return 'application/javascript'
    if 'css' in file_extension:
        return 'text/css'

    return mime.from_file(f)


def clean_path(root):
    def cleaner(path):
        n = path.replace(root, '')
        return n if not n.startswith('/') else n[1:]
    return cleaner


def get_upload_data(root, single=False):
    cleaner = clean_path(root)
    for i in get_file_list(root):
        yield {
            'path': i,
            'key': cleaner(i) if not single else i,
            'content_type': get_mime_type(i)
        }

def upload(bucket_name):
    bucketstore = get_bucket(bucket_name)

    def uploader(data):
        for i in data:
            with open(i['path'], 'rb') as f:
                value = f.read()
                bucketstore.set(
                    i['key'],
                    value,
                    content_type=i['content_type']
                )
                click.echo(click.style("[-] Uploaded %s" % i['key'], bold=False))

    return uploader

def run(bucket, file_list):
    uploader = upload(bucket)
    for f in file_list:
        data = get_upload_data(f, single=os.path.isfile(f))
        uploader(data)
