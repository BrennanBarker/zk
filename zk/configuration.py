import click
from typing import NamedTuple
from os.path import expanduser

class Config(NamedTuple):
    notes_directory: str
    html_directory: str
    editor: str
        
test_ctx = click.Context(click.Command)
test_ctx.obj = Config(notes_directory=expanduser('~/notes'),
                      html_directory=expanduser('~/notes/html'),
                      editor='vim')