"""Routes related to the datalab."""
from flask import jsonify, request

from . import api
from ..response import QuerySetApiResult
from ..queries import DatalabData


@api.route('/datalab/data')
def get_datalab_data():
    """Get the correct slice of datalab data."""
    survey = request.args.get('survey', None)
    indicator = request.args.get('indicator', None)
    char_grp = request.args.get('characteristicGroup', None)
    over_time = request.args.get('overTime', 'false')
    over_time = True if over_time.lower() == 'true' else False
    json_obj = DatalabData.series_query(survey, indicator, char_grp, over_time)
    response_format = request.args.get('format', None)
    return QuerySetApiResult(json_obj, response_format)


@api.route('/datalab/combos')
def get_datalab_combos():
    """Get datalab combos."""
    survey = request.args.get('survey', None)
    survey_list = sorted(survey.split(',')) if survey else []
    indicator = request.args.get('indicator', None)
    char_grp = request.args.get('characteristicGroup', None)
    json_obj = DatalabData.combos_all(survey_list, indicator, char_grp)
    return jsonify(json_obj)


@api.route('/datalab/init')
def get_datalab_init():
    """Get datalab combos."""
    data = DatalabData.datalab_init()
    return jsonify(data)
