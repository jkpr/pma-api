"""API Routes."""
from flask import Blueprint, jsonify, request, url_for

from .. import queries
from ..models import Country, EnglishString, Survey, Indicator, Data


api = Blueprint('api', __name__)


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
    # TODO: See flask.pocoo.org/snippets/45/
    request_headers = 'application/json'  # default for now
    if request_headers == 'text/html':
        return 'Documentation.'
    return get_resources()


@api.route('/countries')
def get_countries():
    """Country resource collection GET method.

    Returns:
        json: Collection for resource.
    """
    # validity, messages = model.validate_query(request.args)  # TODO: Finish.
    # print('\n\n', validity, messages, '\n\n')  # Testing

    return full_json_collection(Country)


@api.route('/countries/<code>')
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


@api.route('/surveys')
def get_surveys():
    """Survey resource collection GET method.

    Returns:
        json: Collection for resource.
    """
    # Query by year, country, round
    return full_json_collection(Survey)


@api.route('/surveys/<code>')
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


@api.route('/indicators')
def get_indicators():
    """Indicator resource collection GET method.

    Returns:
        json: Collection for resource.
    """
    return full_json_collection(Indicator)


@api.route('/indicators/<code>')
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


@api.route('/data')
def get_data():
    """Data resource collection GET method.

    Returns:
        json: Collection for resource.
    """
    refined_all_data = data_refined_query(request.args)
    return full_json_collection(refined_all_data, prequeried=True)


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


@api.route('/data/<uuid>')
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


@api.route('/texts')
def get_texts():
    """Text resource collection GET method.

    Returns:
        json: Collection for resource.
    """
    return full_json_collection(EnglishString)


@api.route('/texts/<uuid>')
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


@api.route('/characteristicGroups')
def get_characteristic_groups():
    """Characteristic Groups  resource collection GET method.

    Returns:
        json: Collection for resource.
    """
    return 'Characteristic groups'  # TODO


@api.route('/characteristicGroups/<code>')
def get_characteristic_group(code):
    """Characteristic Groups resource entity GET method.

    Args:
        code (str): Identification for resource entity.

    Returns:
        json: Entity of resource.
    """
    return code


@api.route('/resources')
def get_resources():
    """API resource route.

    Returns:
        json: List of resources.
    """
    resource_endpoints = (
        ('countries', 'api.get_surveys'),
        ('surveys', 'api.get_surveys'),
        ('texts', 'api.get_texts'),
        ('indicators', 'api.get_indicators'),
        ('data', 'api.get_data'),
        ('characteristicGroups', 'api.get_characteristic_groups')
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


@api.route('/datalab/data')
def get_datalab_data():
    """Get the correct slice of datalab data."""
    survey = request.args.get('survey', None)
    indicator = request.args.get('indicator', None)
    char_grp = request.args.get('characteristicGroup', None)
    json_obj = queries.get_datalab_data(survey, indicator, char_grp)
    return jsonify(json_obj)
