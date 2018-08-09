# -*- coding: utf-8 -*-

"""Main module."""

import os
import json

import click

import bucketstore


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

    types = {
        'a': 'application/octet-stream',
        'ai': 'application/postscript',
        'aif': 'audio/x-aiff',
        'aifc': 'audio/x-aiff',
        'aiff': 'audio/x-aiff',
        'au': 'audio/basic',
        'avi': 'video/x-msvideo',
        'bat': 'text/plain',
        'bin': 'application/octet-stream',
        'bmp': 'image/x-ms-bmp',
        'c': 'text/plain',
        'cdf': 'application/x-cdf',
        'csh': 'application/x-csh',
        'css': 'text/css',
        'dll': 'application/octet-stream',
        'doc': 'application/msword',
        'dot': 'application/msword',
        'dvi': 'application/x-dvi',
        'eml': 'message/rfc822',
        'eps': 'application/postscript',
        'etx': 'text/x-setext',
        'exe': 'application/octet-stream',
        'gif': 'image/gif',
        'gtar': 'application/x-gtar',
        'h': 'text/plain',
        'hdf': 'application/x-hdf',
        'htm': 'text/html',
        'html': 'text/html',
        'jpe': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'jpg': 'image/jpeg',
        'js': 'application/x-javascript',
        'json': 'application/json',
        'ksh': 'text/plain',
        'latex': 'application/x-latex',
        'm1v': 'video/mpeg',
        'man': 'application/x-troff-man',
        'me': 'application/x-troff-me',
        'mht': 'message/rfc822',
        'mhtml': 'message/rfc822',
        'mif': 'application/x-mif',
        'mov': 'video/quicktime',
        'movie': 'video/x-sgi-movie',
        'mp2': 'audio/mpeg',
        'mp3': 'audio/mpeg',
        'mp4': 'video/mp4',
        'mpa': 'video/mpeg',
        'mpe': 'video/mpeg',
        'mpeg': 'video/mpeg',
        'mpg': 'video/mpeg',
        'ms': 'application/x-troff-ms',
        'nc': 'application/x-netcdf',
        'nws': 'message/rfc822',
        'o': 'application/octet-stream',
        'obj': 'application/octet-stream',
        'oda': 'application/oda',
        'pbm': 'image/x-portable-bitmap',
        'pdf': 'application/pdf',
        'pfx': 'application/x-pkcs12',
        'pgm': 'image/x-portable-graymap',
        'png': 'image/png',
        'pnm': 'image/x-portable-anymap',
        'pot': 'application/vnd.ms-powerpoint',
        'ppa': 'application/vnd.ms-powerpoint',
        'ppm': 'image/x-portable-pixmap',
        'pps': 'application/vnd.ms-powerpoint',
        'ppt': 'application/vnd.ms-powerpoint',
        'pptx': 'application/vnd.ms-powerpoint',
        'ps': 'application/postscript',
        'pwz': 'application/vnd.ms-powerpoint',
        'py': 'text/x-python',
        'pyc': 'application/x-python-code',
        'pyo': 'application/x-python-code',
        'qt': 'video/quicktime',
        'ra': 'audio/x-pn-realaudio',
        'ram': 'application/x-pn-realaudio',
        'ras': 'image/x-cmu-raster',
        'rdf': 'application/xml',
        'rgb': 'image/x-rgb',
        'roff': 'application/x-troff',
        'rtx': 'text/richtext',
        'sgm': 'text/x-sgml',
        'sgml': 'text/x-sgml',
        'sh': 'application/x-sh',
        'shar': 'application/x-shar',
        'snd': 'audio/basic',
        'so': 'application/octet-stream',
        'src': 'application/x-wais-source',
        'swf': 'application/x-shockwave-flash',
        't': 'application/x-troff',
        'tar': 'application/x-tar',
        'tcl': 'application/x-tcl',
        'tex': 'application/x-tex',
        'texi': 'application/x-texinfo',
        'texinfo': 'application/x-texinfo',
        'tif': 'image/tiff',
        'tiff': 'image/tiff',
        'tr': 'application/x-troff',
        'tsv': 'text/tab-separated-values',
        'txt': 'text/plain',
        'ustar': 'application/x-ustar',
        'vcf': 'text/x-vcard',
        'wav': 'audio/x-wav',
        'wiz': 'application/msword',
        'wsdl': 'application/xml',
        'xbm': 'image/x-xbitmap',
        'xlb': 'application/vnd.ms-excel',
        'xls': 'application/vnd.ms-excel',
        'xlsx': 'application/vnd.ms-excel',
        'xml': 'text/xml',
        'xpdl': 'application/xml',
        'xpm': 'image/x-xpixmap',
        'xsl': 'application/xml',
        'xwd': 'image/x-xwindowdump',
        'zip': 'application/zip'
    }

    return types.get(file_extension, 'text/html')


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


def upload(bucket_name, folder=None):
    bucketstore = get_bucket(bucket_name)

    def uploader(data, tags, meta):
        if tags:
            meta['tags'] = json.dumps(tags.split(','))
        for i in data:
            key = '%s/%s' % (folder, i['key'])
            with open(i['path'], 'rb') as f:
                value = f.read()
                bucketstore.set(
                    key,
                    value,
                    content_type=i['content_type'],
                    metadata=meta
                )
                item = bucketstore.key(key)
                item.make_public()

                click.echo(
                    click.style("[-] Uploaded %s" % key, bold=False)
                )

    return uploader


def run(bucket, file_list, tags=None, metadata=None, folder=None):
    meta = {
        k: json.dumps(v) for k, v in metadata.iteritems()
    } if metadata else {}

    uploader = upload(bucket, folder=folder)
    for f in file_list:
        data = get_upload_data(f, single=os.path.isfile(f))
        uploader(data, tags, meta)
