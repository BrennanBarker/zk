import os, subprocess, glob, time, string
from collections import namedtuple
from typing import NamedTuple
from importlib.resources import open_text
import click
from zk.utils import *

print(ard)


def filled_template(fields):
    with open_text('templates', 'note-template.md') as f: 
        return string.Template(f.read()).substitute(fields)

def join_with_spaces(field):
    return ' '.join(field) if type(field) == tuple else field

def all_notes(notes_dir):
    return (os.path.join(notes_dir, file) for file in os.listdir(notes_dir) 
            if file.endswith('.md'))

def grep_notes(regex, notes_dir):
    results = subprocess.run(['grep', regex] + list(all_notes(notes_dir)),
                             capture_output=True)
    return str(results.stdout, 'utf-8').split('\n')[:-1]

def split_grep(grep_result, directory):
        without_dir = grep_result.replace(directory, '')
        return (without_dir[1:18], without_dir[19:])

def last_note(notes_dir):
    return sorted(all_notes(notes_dir), key=os.path.getmtime)[-1]

def edit_note(config, text, filepath):
    new_text = click.edit(text, editor=config.editor, extension='.md')
    if new_text:
        click.echo(f'writing note to {filepath}')
        with open(filepath, 'w') as f: f.write(new_text)
    else: click.echo('no edits!')

def edit_last_note(ctx, param, value):
    config = ctx.obj
    filepath = last_note(config.notes_directory)
    with open(filepath) as f: 
        text = f.read()
    edit_note(config, text, filepath)
    ctx.exit()


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
    text = filled_template({k: join_with_spaces(v) for k,v in fields.items()})
    edit_note(config, text, filename)

@cli.command()
# option: whole word vs. regex
# option: context
@click.argument('regex')
@click.pass_obj
def search(config, regex):
    """Search your note directory by regex"""
    for result in grep_notes(regex, config.notes_directory):
        file, match = split_grep(result, config.notes_directory)
        click.echo(f'{file}: {match}')
        
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