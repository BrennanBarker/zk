"""Command line interface for zk"""

import os, time
from typing import NamedTuple
import click
from zk.utils import *


class Config(NamedTuple):
    notes_directory: str
    editor: str
    

@click.group()
@click.option('--notes-directory', default=os.path.expanduser('~/notes'),
              help='Directory where notes are stored (default ~/notes)')
@click.option('--editor', default='vim', 
              help='Editor used to edit notes.')
@click.pass_context
def cli(ctx, notes_directory, editor): 
    ctx.obj = Config(notes_directory=notes_directory, editor=editor)


@cli.command()
@click.option('--identity', '--id', 
              default=time.strftime('%Y%m%d%H%M%S'), help='Note id')
@click.option('--title', default='', help='Note title')
@click.option('--tag', default=[], multiple=True, help='Specify tags')
@click.option('--ref', default=[], multiple=True, help='Specify refs')
@click.pass_obj
def new(config, **fields):
    """Create a new zk note.""" 
    filename = os.path.join(config.notes_directory, fields['identity'] + '.md')
    formatted_fields = {k: join_with_spaces(v) for k,v in fields.items()}
    with open_text('templates', 'note-template.md') as f:
        text = string.Template(f.read()).substitute(fields)
    edit_note(config, text, filename)

@cli.command()
# option: whole word vs. regex 
# option: context
# pass grep options
@click.argument('regex')
@click.option('--include-path', is_flag=True, default=False)
@click.pass_obj
def search(config, regex, include_path):
    """Search your note directory by regex"""
    grep_result = grep_notes(regex, config.notes_directory)
    for path, match in parse_grep(grep_result):
        location = path if include_path else os.path.basename(path)
        click.echo(f'({location}) {match}')
        
@cli.command()
@click.option('--last', is_flag=True, callback=edit_last_note)
@click.argument('filename')
@click.pass_obj
def edit(config, filename):
    click.edit(filename=filename, editor=config.editor)
    
    
# New note
# Edit
    # Most recently edited note
    # Most recently created note
    # Id (or filename)
# Register friendly name? Titles associated with ids (json)
# Search (keyword)
# Note stats
# Graph
    # Update
    # View
# View as html?