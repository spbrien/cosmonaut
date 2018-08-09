# -*- coding: utf-8 -*-

"""Console script for sputnik."""
import sys
import json
import click

from cosmonaut import run


@click.command()
@click.option(
    '-b',
    '--bucket',
    help="S3 bucket target for deployment",
    prompt=True
)
@click.option(
    '-f',
    '--folder',
    help="S3 bucket folder for deployment",
    prompt=True
)
@click.option(
    '-t',
    '--tags',
    help="Comma-separated list of tags to add to uploaded files",
    required=False
)
@click.option(
    '-m',
    '--metadata',
    help="JSON metadata to add to uploaded files",
    required=False
)
@click.argument('files', nargs=-1)
def main(bucket, folder, tags, metadata, files):
    """Deploys static assets to S3."""
    click.echo(click.style("[+] Deploying...", bold=True, fg='white'))
    meta = json.loads(metadata) if metadata else None
    run(bucket, files, tags=tags, metadata=meta, folder=folder)
    click.echo(click.style("\n[+] Finished\n", bold=True, fg='white'))
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
