# -*- coding: utf-8 -*-

"""Console script for sputnik."""
import sys
import click

from cosmonaut import run


@click.command()
@click.option('-b', '--bucket', help="S3 bucket target for deployment", prompt=True)
@click.argument('dist', nargs=-1)
def main(bucket, dist):
    """Console script for sputnik."""
    click.echo(click.style("[+] Deploying...", bold=True, fg='white'))
    run(bucket, dist)
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
