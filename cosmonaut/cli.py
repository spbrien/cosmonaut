# -*- coding: utf-8 -*-

"""Console script for sputnik."""
import sys
import click

from cosmonaut import run


@click.command()
@click.option('-b', '--bucket', help="S3 bucket target for deployment", prompt=True)
@click.argument('dist', nargs=-1)
def main(bucket, dist):
    """Console script for cosmonaut."""
    click.echo(click.style("\n[+] Deploying...\n", bold=True, fg='white'))
    run(bucket, dist)
    click.echo(click.style("\n[+] Finished\n", bold=True, fg='white'))
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
