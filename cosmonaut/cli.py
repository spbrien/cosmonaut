# -*- coding: utf-8 -*-

"""Console script for sputnik."""
import sys
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
    '-metadata',
    '--metadata',
    help="JSON metadata to add to uploaded files",
    required=False
)
@click.argument('files', nargs=-1)
def main(bucket, metadata, files):
    """Deploys static assets to S3."""
    click.echo(click.style("[+] Deploying...", bold=True, fg='white'))
    run(bucket, files)
    click.echo(click.style("\n[+] Finished\n", bold=True, fg='white'))
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
