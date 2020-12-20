"""Command line interface for zk"""

import os, time
import click
from zk.utils import *


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
@click.pass_context
def new(ctx, **fields):
    """Create a new zk note.""" 
    filename = os.path.join(ctx.obj.notes_directory, fields['identity'] + '.md')
    text = fill('note-template.md', formatted(fields))
    edit_note(ctx, text, filename)

@cli.command()
# option: whole word vs. regex 
# option: context
# pass grep options
@click.argument('regex')
@click.option('--include-path', is_flag=True, default=False)
@click.pass_context
def search(ctx, regex, include_path):
    """Search your note directory by regex"""
    grep_result = grep_notes(regex, ctx)
    for path, match in parse_grep(grep_result):
        location = path if include_path else os.path.basename(path)
        click.echo(f'({location}) {match}')
    

@cli.command()
@click.option('--last', '-l', is_flag=True)
@click.argument('partial_id', required=False, default='')
@click.pass_context
def edit(ctx, partial_id, last):
    note = last_note(ctx) if last else get_note(ctx, partial_id)
    if note: edit_note(ctx, get_text(note), note)
    else: click.echo(f'No notes containing "{partial_id}"')


@cli.command()
@click.pass_context
def ls(ctx):
    for note in all_notes(ctx): click.echo(f'({note}) {title(note)}')
    

# Note stats
# Graph
    # Update
    # View
# View as html?