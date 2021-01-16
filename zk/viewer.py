import os
from markdown import markdown
from flask import Flask, render_template

from zk.utils import get_note_html, get_title, get_note_path

def create_app(ctx, test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/all')
    def all_notes():
        return 'This will show all notes'
    
    @app.route('/search')
    def search():
        return 'This will show the search page'
    
    @app.route('/tags')
    def tags():
        return 'This will show a tags page'
    
    @app.route('/graph')
    def graph():
        return 'This will show the graph'
    
    @app.route('/note/<note_id>')
    def view_note(note_id):
        if note_id.endswith('.md'): note_id = note_id[:-3]
        return render_template('note.html', 
                               note_html=get_note_html(ctx, note_id), 
                               title=get_title(get_note_path(ctx, note_id)))

    return app
