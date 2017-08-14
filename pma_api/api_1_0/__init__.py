"""API Routes."""
from flask import Blueprint, jsonify, request, url_for

from ..models import Country, EnglishString, Survey, Indicator, Data


API = Blueprint('api', __name__)


@API.route('/')
def say_hello():
    """API Root.

    Returns:
        json: List of resources.
    """
    return get_resources()


@API.route('/countries')
def get_countries():
    """Country resource collection GET method.

    Returns:
        json: Collection for resource.
    """
    countries = Country.query.all()
    json_obj = {
        'resultsSize': len(countries),
        'results': [c.url_for() for c in countries]
    }
    return jsonify(json_obj)


@API.route('/countries/<code>')
def get_country(code):
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


@API.route('/surveys')
def get_surveys():
    """Survey resource collection GET method.

    Returns:
        json: Collection for resource.
    """
    # Query by year, country, round
    print(request.args)
    surveys = Survey.query.all()
    json_obj = {
        'resultsSize': len(surveys),
        'results': [s.full_json() for s in surveys]
    }
    return jsonify(json_obj)


@API.route('/surveys/<code>')
def get_survey(code):
    """Survey resource entity GET method.

    Args:
        code (str): Identification for resource entity.

    Returns:
        json: Entity of resource.
    """
    survey = Survey.query.filter_by(code=code).first()
    json_obj = survey.full_json()
    return jsonify(json_obj)


@API.route('/indicators')
def get_indicators():
    """Indicator resource collection GET method.

    Returns:
        json: Collection for resource.
    """
    indicators = Indicator.query.all()
    json_obj = {
        'resultsSize': len(indicators),
        'results': [
            i.full_json(endpoint='api.get_indicator') for i in indicators
        ]
    }
    return jsonify(json_obj)


@API.route('/indicators/<code>')
def get_indicator(code):
    """Indicator resource entity GET method.

    Args:
        code (str): Identification for resource entity.

    Returns:
        json: Entity of resource.
    """
    indicator = Indicator.query.filter_by(code=code).first()
    json_obj = indicator.full_json()
    return jsonify(json_obj)


@API.route('/characteristics')
def get_characterstics():
    """Characteristics resource collection GET method.

    Returns:
        json: Collection for resource.
    """
    pass


@API.route('/characteristics/<code>')
def get_characteristic(code):
    """Characteristic resource entity GET method.

    Args:
        code (str): Identification for resource entity.

    Returns:
        json: Entity of resource.
    """
    pass


@API.route('/data')
def get_data():
    """Data resource collection GET method.

    Returns:
        json: Collection for resource.
    """
    all_data = data_refined_query(request.args)
    # all_data = Data.query.all()
    json_obj = {
        'resultsSize': len(all_data),
        'results': [
            d.full_json() for d in all_data
        ]
    }
    return jsonify(json_obj)


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


@API.route('/data/<uuid>')
def get_datum(uuid):
    """Data resource entity GET method.

    Args:
        uuid (str): Identification for resource entity.

    Returns:
        json: Entity of resource.
    """
    data = Data.query.filter_by(code=uuid).first()
    json_obj = data.full_json()
    return jsonify(json_obj)


@API.route('/texts')
def get_texts():
    """Text resource collection GET method.

    Returns:
        json: Collection for resource.
    """
    english_strings = EnglishString.query.all()
    json_obj = {
        'resultsSize': len(english_strings),
        'results': [eng.url_for() for eng in english_strings]
    }


@API.route('/texts/<uuid>')
def get_text(uuid):
    """Text resource entity GET method.

    Args:
        uuid (str): Identification for resource entity.

    Returns:
        json: Entity of resource.
    """
    text = EnglishString.query.filter_by(uuid=uuid).first()
    json_obj = text.to_json()
    return jsonify(json_obj)


@API.route('/resources')
def get_resources():
    """API resource route..

    Returns:
        json: List of resources.
    """
    json_obj = {
        'resources': [{
            'name': 'countries',
            'resource': url_for('api.get_surveys', _external=True)
        }, {
            'name': 'surveys',
            'resource': url_for('api.get_countries', _external=True)
        }, {
            'name': 'texts',
            'resource': url_for('api.get_texts', _external=True)
        }]
    }
    return jsonify(json_obj)
