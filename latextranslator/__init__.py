"""A LaTeX to TXT file translator."""
import click
from .main import translate

__version__ = "0.1.1"

@click.command()
@click.argument('file_name')
@click.version_option(__version__)
def cli(file_name):
	translate(file_name)
	click.echo("Traducido correctamente")
