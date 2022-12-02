"""Index server REST API util functions."""
from flask import jsonify
import index


class InvalidUsage(Exception):
    """Basic http exception class."""

    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        """Create exception."""
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        """Make to dict."""
        retval = dict(self.payload or ())
        retval['message'] = self.message
        return retval


@index.app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    """Handle exceptions."""
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
