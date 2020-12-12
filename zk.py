import os
from time import strftime
import importlib.resources
from string import Template
import click
import subprocess
import glob


class Config():
    def __init__(self):
        pass
pass_config = click.make_pass_decorator(Config, ensure=True)


@click.group()
@click.option('--notes-directory', default=os.path.expanduser('~/notes'),
                  help='Directory where notes are stored (default ~/notes)')
@pass_config
def cli(config, notes_directory):
    config.notes_directory = notes_directory


@cli.command()
@click.option('--editor', default='vim', help='Editor used to edit notes.')
@click.option('--identity', '--id', default=strftime('%Y%m%d%H%M%S'), help='Note id')
@click.option('--filetype', default='.md', help="Note filetype extension (default '.md')")
@click.option('--title', default='', help='Note title')
@click.option('--tags', default=[], multiple=True, help='Specify tags')
@click.option('--refs', default=[], multiple=True, help='Specify refs')
@pass_config
def new(config, identity, title, tags, refs, filetype, editor):
    """Create a new zk note."""
    filename = os.path.join(config.notes_directory, identity + filetype)
    with importlib.resources.open_text('templates', 'note-template.md') as f:
        text = Template(f.read()).substitute(
            {'title': title,
             'id': identity,
             'tags': ' '.join(tags),
             'refs': ' '.join(refs),
            })
    new_text = click.edit(text=text, editor=editor, extension=filetype)
    if new_text:
        print(f'writing note to {filename}')
        with open(filename, 'w') as f:
            f.write(new_text)
    else: print('no edits!')

@cli.command()
@click.argument('regex')
@pass_config
# option: whole word
# option: context
def search(config, regex):
    """Search your note directory by regex"""
    grep_result = subprocess.run(
        ['grep', regex] + glob.glob(os.path.join(config.notes_directory, '*.md')),
        capture_output=True)
    click.echo(grep_result.stdout)
    
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