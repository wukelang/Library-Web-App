"""Initialize Flask app."""

from flask import Flask, render_template
from pathlib import Path    # Gets file names for book + author data

from library.adapters.jsondatareader import BooksJSONReader


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    # TODO: we need to move this code into a repository - Luke
    data_path = Path('library') / 'adapters' / 'data'
    books_file = str(Path(data_path) / "comic_books_excerpt.json")
    author_file = str(Path(data_path) / "book_authors_excerpt.json")

    reader = BooksJSONReader(books_file, author_file)
    reader.read_json_files()
    books_db = reader.dataset_of_books

    with app.app_context():
        # Register blueprints.
        from .home import home
        app.register_blueprint(home.home_blueprint)

        from .browse import browse
        app.register_blueprint(browse.browse_blueprint)

        # TODO: Authentication implementation
        # from .authentication import authentication
        # app.register_blueprint(authentication.authentication_blueprint)


    return app