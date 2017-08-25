"""API Routes."""
from flask import Blueprint, jsonify

from ..queries import DatalabData

api = Blueprint('api', __name__)
__version__ = '1.0'

# pylint: disable=wrong-import-position
from . import collection, datalab


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


# TODO: Handle null cases.
@api.route('/datalab/data')
def get_datalab_data():
    """Get the correct slice of datalab data."""
    if not request.args:
        json_obj = DatalabData.get_all_datalab_data()
    elif 'survey' not in request.args or 'indicator' not in request.args \
            or 'characteristicGroup' not in request.args:
        return 'InvalidArgsError: This endpoint requires the following 3 ' \
               'parameters: \n* survey\n* indicator\n* characteristicGroup'
    else:
        survey = request.args.get('survey', None)
        indicator = request.args.get('indicator', None)
        char_grp = request.args.get('characteristicGroup', None)
        json_obj = DatalabData.get_filtered_datalab_data(survey, indicator,
                                                         char_grp)

    return jsonify(json_obj)


@api.route('/datalab/combos')
def get_datalab_combos():
    """Get datalab combos."""
    # TODO: Account for all combinations of request args or lack thereof.
    # TODO: Add logic to sort by arguments. If you have indicator, go to
    # this method.

    if 'survey' not in request.args and 'indicator' not in request.args \
            and 'characteristicGroup' not in request.args:
        return 'InvalidArgsError: This endpoint requires 1-2 of 3 ' \
               'parameters: \n* survey\n* indicator\n* characteristicGroup'

    # return jsonify(DatalabData.related_models_from_single_model_data(
    #     request.args))
    return jsonify(DatalabData.get_combos(request.args))


@api.route('/datalab/init')
def get_datalab_init():
    """Get datalab combos."""
    return jsonify(DatalabData.datalab_init())

@api.route('/datalab')
def get_datalab():
    return get_datalab_resources()

@api.route('/datalab/resources')
def get_datalab_resources():
    """Get datalab routes."""
    resource_endpoints = (
        ('init', 'api.get_datalab_init'),
        ('combos', 'api.get_datalab_combos'),
        ('data', 'api.get_datalab_data')
    )
    return jsonify({
        'resources': [{
            'name': name,
            'resource': url_for(route, _external=True)}
            for name, route in resource_endpoints]
    })
