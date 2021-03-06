import os
from markdown import markdown
from flask import Flask, Blueprint, render_template

from zk.utils import (get_note_html, get_title, get_note_path, get_id, 
                      all_notes, build_tag_index)


notes_bp = Blueprint('note', __name__)

@notes_bp.route('/')
def notes_index(ctx):
    return render_template('all.html', 
                           notes=all_notes(ctx),
                           get_id=get_id,
                           get_title=get_title,
                           page_title='All notes',
                          )

@notes_bp.route('/<note_id>')
def view_note(ctx, note_id):
    if note_id.endswith('.md'): note_id = note_id[:-3]
    return render_template('note.html', 
                           note_html=get_note_html(ctx, note_id), 
                           page_title=get_title(get_note_path(ctx, note_id))
                          )


def create_app(ctx, test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY='dev',)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    app.register_blueprint(notes_bp)
    
    app.add_url_rule('/', endpoint='notes_index')
    
    
    @app.route('/search')
    def search():
        return 'This will show the search page'
    
    @app.route('/tag/<tag_name>')
    def tag(tag_name):
        if tag_name == 'all-tags':
            tag_index = build_tag_index(ctx)
        return render_template('tags.html',
                               tag_index=tag_index,
                               get_id=get_id,
                               get_title=get_title,
                               page_title='All tags'
                              )
    
    @app.route('/graph')
    def graph():
        return 'This will show the graph'
    
    
    return app
