"""API Routes."""
from flask import jsonify, request, url_for
# from flask import Blueprint, jsonify, request, url_for

from ..queries import DatalabData
from ..models import Country, EnglishString, Survey, Indicator, Data
from ..api_1_0 import api1 as api2


# api2 = Blueprint('api2', __name__)


@api2.route('/v2/')
def api2_api2_root():
    """Root route.

    Returns:
        func: get_resources() if 'application/json'
        func: get_docs() if 'text/html'
    """
    # TODO: See flask.pocoo.org/snippets/45/
    request_headers = 'application/json'  # default for now
    if request_headers == 'text/html':
        return 'Documentation.'
    return api2_get_resources()


@api2.route('/v2/countries')
def api2_get_countries():
    """Country resource collection GET method.

    Returns:
        json: Collection for resource.
    """
    model = Country
    countries = model.query.all()

    print('\n\n', request.args)  # Testing
    validity, messages = model.validate_query(request.args)
    print(validity)
    print(messages)
    print('\n\n')

    return jsonify({
        'resultsSize': len(countries),
        'results': [c.full_json() for c in countries]
    })


@api2.route('/v2/countries/<code>')
def api2_get_country(code):
    """Country resource entity GET method.

    Args:
        code (str): Identification for resource entity.

    Returns:
        json: Entity of resource.
    """
    lang = request.args.get('_lang')
    country = Country.query.filter_by(country_code=code).first()
    json_obj = country.to_json(lang=lang)
    return jsonify(json_obj)


@api2.route('/v2/surveys')
def api2_get_surveys():
    """Survey resource collection GET method.

    Returns:
        json: Collection for resource.
    """
    # Query by year, country, round
    # print(request.args)
    surveys = Survey.query.all()
    return jsonify({
        'resultsSize': len(surveys),
        'results': [s.full_json() for s in surveys]
    })


@api2.route('/v2/surveys/<code>')
def api2_get_survey(code):
    """Survey resource entity GET method.

    Args:
        code (str): Identification for resource entity.

    Returns:
        json: Entity of resource.
    """
    survey = Survey.query.filter_by(code=code).first()
    json_obj = survey.full_json()
    return jsonify(json_obj)


@api2.route('/v2/indicators')
def api2_get_indicators():
    """Indicator resource collection GET method.

    Returns:
        json: Collection for resource.
    """
    indicators = Indicator.query.all()
    return jsonify({
        'resultsSize': len(indicators),
        'results': [
            i.full_json(endpoint='api2.get_indicator') for i in indicators
        ]
    })


@api2.route('/v2/indicators/<code>')
def api2_get_indicator(code):
    """Indicator resource entity GET method.

    Args:
        code (str): Identification for resource entity.

    Returns:
        json: Entity of resource.
    """
    indicator = Indicator.query.filter_by(code=code).first()
    json_obj = indicator.full_json()
    return jsonify(json_obj)


@api2.route('/v2/data')
def api2_get_data():
    """Data resource collection GET method.

    Returns:
        json: Collection for resource.
    """
    all_data = data_refined_query(request.args)
    # all_data = Data.query.all()
    return jsonify({
        'resultsSize': len(all_data),
        'results': [d.full_json() for d in all_data]
    })


def data_refined_query(args):
    """Data refined query.

    *Args:
        survey (str): If present, filter by survey entities.

    Returns:
        dict: Filtered query data.
    """
    qset = Data.query
    if 'survey' in args:
        qset = qset.filter(Data.survey.has(code=args['survey']))
    results = qset.all()
    return results


@api2.route('/v2/data/<code>')
def api2_get_datum(code):
    """Data resource entity GET method.

    Args:
        code (str): Identification for resource entity.

    Returns:
        json: Entity of resource.
    """
    data = Data.query.filter_by(code=code).first()
    json_obj = data.full_json()
    return jsonify(json_obj)


@api2.route('/v2/texts')
def api2_get_texts():
    """Text resource collection GET method.

    Returns:
        json: Collection for resource.
    """
    english_strings = EnglishString.query.all()
    return jsonify({
        'resultsSize': len(english_strings),
        'results': [d.to_json() for d in english_strings]
    })


@api2.route('/v2/texts/<code>')
def api2_get_text(code):
    """Text resource entity GET method.

    Args:
        code (str): Identification for resource entity.

    Returns:
        json: Entity of resource.
    """
    text = EnglishString.query.filter_by(code=code).first()
    json_obj = text.to_json()
    return jsonify(json_obj)


@api2.route('/v2/characteristicGroups')
def api2_get_characteristic_groups():
    """Characteristic Groups  resource collection GET method.

    Returns:
        json: Collection for resource.
    """
    return 'Characteristic groups'  # TODO


@api2.route('/v2/characteristicGroups/<code>')
def api2_get_characteristic_group(code):
    """Characteristic Groups resource entity GET method.

    Args:
        code (str): Identification for resource entity.

    Returns:
        json: Entity of resource.
    """
    return code


@api2.route('/v2/resources')
def api2_get_resources():
    """API resource route.

    Returns:
        json: List of resources.
    """
    resource_endpoints = (
        ('countries', 'api2.get_surveys'),
        ('surveys', 'api2.get_surveys'),
        ('texts', 'api2.get_texts'),
        ('indicators', 'api2.get_indicators'),
        ('data', 'api2.get_data'),
        ('characteristicGroups', 'api2.get_characteristic_groups')
    )
    json_obj = {
        'resources': [
            {
                'name': name,
                'resource': url_for(route, _external=True)
            }
            for name, route in resource_endpoints
        ]
    }
    return jsonify(json_obj)


# TODO: Handle null cases.
@api2.route('/v2/datalab/data')
def api2_get_datalab_data():
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


@api2.route('/v2/datalab/combos')
def api2_get_datalab_combos():
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


@api2.route('/v2/datalab/init')
def api2_get_datalab_init():
    """Get datalab combos."""
    return jsonify(DatalabData.datalab_init())


@api2.route('/v2/datalab')
def api2_get_datalab():
    """Get datalab routes.."""
    return api2_get_datalab_resources()


@api2.route('/v2/datalab/resources')
def api2_get_datalab_resources():
    """Get datalab routes."""
    resource_endpoints = (
        ('init', 'api2.get_datalab_init'),
        ('combos', 'api2.get_datalab_combos'),
        ('data', 'api2.get_datalab_data')
    )
    return jsonify({
        'resources': [{
            'name': name,
            'resource': url_for(route, _external=True)}
            for name, route in resource_endpoints]
    })
