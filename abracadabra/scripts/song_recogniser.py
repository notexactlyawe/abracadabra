import os
import click
from abracadabra import storage, recognise


@click.group()
def cli():
    pass


@click.command(help="Register a song or a directory of songs")
@click.argument("path")
def register(path):
    if os.path.isdir(path):
        recognise.register_directory(path)
    else:
        recognise.register_song(path)


@click.command(help="Recognise a song at a filename or using the microphone")
@click.argument("path", required=False)
@click.option("--listen", is_flag=True, help="Use the microphone to listen for a song")
def recognise_command(path, listen):
    print(f"Args: path - {path}, listen - {listen}")
    if listen:
        result = recognise.listen_to_song()
        click.echo(result)
    else:
        result = recognise.recognise_song(path)
        click.echo(result)


@click.command(help="Initialise the DB, needs to be done before other commands")
def initialise():
    storage.setup_db()
    click.echo("Initialised DB")

cli.add_command(register)
cli.add_command(recognise_command)
cli.add_command(initialise)

if __name__ == "__main__":
    cli()
