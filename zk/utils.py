"""Utilities for dealing with zk notes."""

import os
from os.path import basename
from subprocess import run
from importlib.resources import open_text
import click


def join_with_spaces(field):
    return ' '.join(field) if type(field) == tuple else field

def all_notes(notes_dir):
    return (os.path.join(notes_dir, file) for file in os.listdir(notes_dir) 
            if file.endswith('.md'))

def grep_notes(re, notes_dir):
    return run(['grep', re] + list(all_notes(notes_dir)), capture_output=True)

def parse_grep(result):
    split_results = str(result.stdout, 'utf-8').split('\n')[:-1]
    return [r.split(':', maxsplit=1) for r in split_results]

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