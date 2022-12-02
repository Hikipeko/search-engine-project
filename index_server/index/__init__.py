"""Index package initializer."""
import os
import flask

app = flask.Flask(__name__)  # pylint: disable=invalid-name

# Load segment from the file specified by the env var INDEX_PATH.
# If the environment variable is not set, default to inverted_index_1.txt.
app.config["INDEX_PATH"] = os.getenv("INDEX_PATH", "inverted_index_1.txt")

import index.api  # noqa: E402  pylint: disable=wrong-import-position

# Load inverted index, stopwords, and pagerank into memory
index.api.load_index()
