# from .commandparser import commandparser
import click
import os
from CommandHandler import CommandHandler


@click.group()
# @click.option('--verbose', '-v', is_flag=True, default=False)
def main():
    pass


@main.command()
@click.option('--source', '-src', default=os.getcwd())
@click.option('--destination', '-dst', default=os.getcwd() + '/dst/')
@click.option('--attribute', '-attr', default='album')
@click.option('--auto-overwrite', is_flag=True, default=False)
def sort(**kwargs):
    commandparser('sort', **kwargs)


@main.command()
@click.option('--source', '-src', default=os.getcwd())
@click.option('--destination', '-dst', default=os.getcwd() + '/dst/')
@click.option('--attribute', '-attr', default='album')
@click.option('--auto-overwrite', is_flag=True, default=False)
@click.option('--playlist', '-name')
def playlist(**kwargs):
    commandparser('playlist', **kwargs)


@main.command()
@click.option('--source', '-src', default=os.getcwd())
@click.option('--destination', '-dst', default=os.getcwd())
@click.option('--format', '-fmt')
def format(**kwargs):
    commandparser('format', **kwargs)


def commandparser(mode, **kwargs):
    kwargs['mode'] = mode
    CommandHandler(kwargs)


if __name__ == "__main__":
    main()
