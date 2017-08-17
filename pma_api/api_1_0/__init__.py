"""API Routes."""
from flask import Blueprint, jsonify

from ..queries import DatalabData

api = Blueprint('api', __name__)
__version__ = '1.0'

# pylint: disable=wrong-import-position
from . import collection, datalab


def full_json_collection(model, prequeried=False):
    """Return collection in full JSON format.

    Args:
        model (class): SqlAlchemy model class.
        prequeried (bool): If model has already been queried.

    returns:
        json: Jsonified response.
    """
    collection = model if prequeried else model.query.all()
    return jsonify({
        'resultsSize': len(collection),
        'results': [record.full_json() for record in collection]
    })


@api.route('/')
def root():
    """Root route.

    Returns:
        func: get_resources() if 'application/json'
        func: get_docs() if 'text/html'
    """
    # TODO: (jef/jkp 2017-08-29) Investigate mimetypes in accept headers.
    # See: flask.pocoo.org/snippets/45/ Needs: Nothing?
    request_headers = 'application/json'  # default for now
    if request_headers == 'text/html':
        return 'Documentation.'
    return collection.get_resources()


@api.route('/version')
def show_version():
    """Show API version."""
    response = {
        'version': __version__
    }
    return jsonify(response)
