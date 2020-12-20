"""Utilities for dealing with zk notes."""

import os
from os.path import basename
from typing import NamedTuple
from subprocess import run
from importlib.resources import open_text
from string import Template
import click
    

class Config(NamedTuple):
    notes_directory: str
    editor: str
        

def formatted(fields):
    def join_with_spaces(field):
        return ' '.join(field) if type(field) == tuple else field
    return {k: join_with_spaces(v) for k,v in fields.items()}

def fill(template, fields):
    with open_text('templates', template) as f:
        return Template(f.read()).substitute(fields)

def all_notes(ctx):
    nd = ctx.obj.notes_directory
    return (os.path.join(nd, file) for file in os.listdir(nd) if file.endswith('.md'))

def grep_notes(re, ctx):
    return run(['grep', re] + list(all_notes(ctx)), capture_output=True)

def parse_grep(result):
    split_results = str(result.stdout, 'utf-8').split('\n')[:-1]
    return [r.split(':', maxsplit=1) for r in split_results]

def last_note(ctx):
    return sorted(all_notes(ctx), key=os.path.getmtime)[-1]

def title(note_path):
    with open(note_path,'r') as f: return f.readline()[:-1]
        
def complete_note_path(ctx, args, incomplete):
    return [path for path in all_notes(ctx) if incomplete in path]

def get_note(ctx, partial_id):
    notes = complete_note_path(ctx, None, partial_id)
    if len(notes) == 1: return notes[0]
    elif len(notes) == 0: return None
    else:
        for i, path in enumerate(notes):
            click.echo(f'[{i}] {os.path.basename(path)} {title(path)}')
        choice = click.prompt('Which note', prompt_suffix='? ', 
                              type=click.IntRange(min=0, max=len(notes)))
        return notes[choice]

def get_text(filepath):
    with open(filepath) as f: return f.read()

def edit_note(ctx, text, filepath):
    new_text = click.edit(text, editor=ctx.obj.editor, extension='.md')
    if new_text:
        click.echo(f'writing note to {filepath}')
        with open(filepath, 'w') as f: f.write(new_text)
    else: click.echo('no edits!')
