"""Command line interface for zk"""

import os, time, webbrowser
import click
from zk.utils import *
from zk.viewer import create_app


@click.group()
@click.option('--notes-directory', default=os.path.expanduser('~/notes'),
              help='Directory where notes are stored (default ~/notes)')
@click.option('--html-directory', default=os.path.expanduser('~/notes/html'),
              help='Directory of html mirror of notes (default ~/notes/html)')
@click.option('--editor', default='vim', 
              help='Editor used to edit notes.')
@click.pass_context
def cli(ctx, notes_directory, html_directory, editor): 
    ctx.obj = Config(notes_directory=notes_directory, 
                     html_directory=html_directory,
                     editor=editor)


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
    for note in all_notes(ctx): click.echo(f'({note}) {get_title(note)}')
        
@cli.command()
@click.option('--open-browser', '-l', is_flag=True)
@click.option('--host', '-h', default=None)
@click.option('--port', '-p', default=None)
@click.pass_context
def view(ctx, open_browser, host, port):
    viewer = create_app(ctx)
    viewer.run(host=host, port=port)
    if open_browser:
        webbrowser.open(f'{host}:{port}')

@cli.command()
@click.pass_context
def build(ctx):
    """(Re)build an html mirror of the note archive."""
    click.echo('Building html archive...')
    build_html_notes(ctx)
    click.echo('Done.')

# Note stats
# Graph
    # Update
    # View
# View as html?
    # Update automatically?
    # Autobuild top-level index
    # Autogenerate tag indexes
    