import os
import click
import abracadabra.storage as storage
import abracadabra.recognise as recog


@click.group()
def cli():
    pass


@click.command(help="Register a song or a directory of songs")
@click.argument("path")
def register(path):
    if os.path.isdir(path):
        recog.register_directory(path)
    else:
        recog.register_song(path)


@click.command(help="Recognise a song at a filename or using the microphone")
@click.argument("path", required=False)
@click.option("--listen", is_flag=True,
              help="Use the microphone to listen for a song")
def recognise(path, listen):
    if listen:
        result = recog.listen_to_song()
        click.echo(result)
    else:
        result = recog.recognise_song(path)
        click.echo(result)


@click.command(
    help="Initialise the DB, needs to be done before other commands")
def initialise():
    storage.setup_db()
    click.echo("Initialised DB")


cli.add_command(register)
cli.add_command(recognise)
cli.add_command(initialise)

if __name__ == "__main__":
    cli()
