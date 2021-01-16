"""Utilities for dealing with zk notes."""

import os
from subprocess import run
from importlib.resources import open_text
from string import Template
import re
import click
from markdown import markdown

from zk.configuration import *

def formatted(fields):
    def join_with_spaces(field):
        return ' '.join(field) if type(field) == tuple else field
    return {k: join_with_spaces(v) for k,v in fields.items()}

def fill(template, fields):
    with open_text('zk.templates', template) as f:
        return Template(f.read()).substitute(fields)

def all_notes(ctx):
    nd = ctx.obj.notes_directory
    return (os.path.join(nd, file) for file in os.listdir(nd) 
            if file.endswith('.md') and file != 'tags.md')

def grep_notes(re, ctx):
    return run(['grep', re] + list(all_notes(ctx)), capture_output=True)

def parse_grep(result):
    split_results = str(result.stdout, 'utf-8').split('\n')[:-1]
    return [r.split(':', maxsplit=1) for r in split_results]

def last_note(ctx):
    return sorted(all_notes(ctx), key=os.path.getmtime)[-1]

# Note Metadata
def get_id(note):
    return os.path.basename(note)[:-3]

def get_note_path(ctx, note_id):
    return os.path.join(ctx.obj.notes_directory, note_id + '.md')

def get_text(filepath): 
    with open(filepath) as f: return f.read()

def get_note_html(ctx, note_id):
    """TODO: make the markdown safe w/ 3rd party lib like bleach"""
    return markdown(get_text(get_note_path(ctx, note_id)),)
   
def get_title(note):
    with open(note,'r') as f: return f.readline()[2:-1]
    
def get_tags(note):
    return re.findall(r'\#\w\S+', get_text(note))

def get_refs(note):
    return set(re.findall(r'\d{14}', get_text(note))) - {get_id(note)}
        
def complete_note(ctx, args, incomplete):
    return [path for path in all_notes(ctx) if incomplete in path]

def get_note(ctx, partial_id):
    notes = complete_note(ctx, None, partial_id)
    if len(notes) == 1: return notes[0]
    elif len(notes) == 0: return None
    else:
        for i, path in enumerate(notes):
            click.echo(f'[{i}] {os.path.basename(path)} {get_title(path)}')
        choice = click.prompt('Which note', prompt_suffix='? ', 
                              type=click.IntRange(min=0, max=len(notes)))
        return notes[choice]


def edit_note(ctx, text, filepath):
    new_text = click.edit(text, editor=ctx.obj.editor, extension='.md')
    if new_text:
        click.echo(f'writing note to {filepath}')
        with open(filepath, 'w') as f: f.write(new_text)
    else: click.echo('no edits!')

        
def build_tag_index(ctx):
    tags_by_note = {note: get_tags(note) for note in all_notes(ctx)}
    all_tags = set(sum(tags_by_note.values(), []))
    tag_index = {tag: [] for tag in all_tags}
    for tag, notes in tag_index.items():
        for note, tags in tags_by_note.items():
            if tag in tags: notes.append(note)
    return dict(sorted(tag_index.items(), key=lambda i: len(i[1]), reverse=True))
   
    
def build_tags_page(ctx):
    tags_page = os.path.join(ctx.obj.notes_directory, 'tags.md')
    tag_index = build_tag_index(ctx)
    with open(tags_page, 'w') as f:
        for tag, notes in tag_index.items():
            f.write(f'## {tag}\n')
            for note in notes:
                f.write(f'{get_link(ctx, note)} {get_title(note)}\n\n')
                

def get_link(ctx, note):
    """Given a path to a (markdown) note, return a markdown-formatted link to the corresponding html file"""
    return f'[{get_id(note)}]({get_html_path(ctx, note)})'


def edgelist(ctx):
    return {get_id(note): get_refs(note) for note in all_notes(ctx)}
    
# Edgelist
# get_refs
# build edgelist
    # {note: get_refs(note) for note in all_notes}
    