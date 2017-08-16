"""API Routes."""
from flask import Blueprint, jsonify, request, url_for

from ..models import Country, EnglishString, Survey, Indicator, Data


API = Blueprint('api', __name__)
RESOURCE_INFO = {
    'characteristics': {
        'aliases': {
            'api': {
                'singular': 'characteristic',
                'plural': 'characteristics'
            },
            'db': {
                'singular': 'characteristic',
                'plural': 'characteristics'
            }
        }
    },
    'characteristicGroups': {
        'aliases': {
            'api': {
                'singular': 'characteristicGroup',
                'plural': 'characteristicGroups'
            },
            'db': {
                'singular': 'characteristic_group',
                'plural': 'characteristic_groups'
            }
        }
    },
    'countries': {
        'aliases': {
            'api': {
                'singular': 'country',
                'plural': 'countries'
            },
            'db': {
                'singular': 'country',
                'plural': 'countries'
            }
        }
    },
    'data': {
        'aliases': {
            'api': {
                'singular': 'datum',
                'plural': 'data'
            },
            'db': {
                'singular': 'datum',
                'plural': 'data'
            }
        }
    },
    'indicators': {
        'aliases': {
            'api': {
                'singular': 'indicator',
                'plural': 'indicators'
            },
            'db': {
                'singular': 'indicator',
                'plural': 'indicators'
            }
        }
    },
    'surveys': {
        'aliases': {
            'api': {
                'singular': 'survey',
                'plural': 'surveys'
            },
            'db': {
                'singular': 'survey',
                'plural': 'surveys'
            }
        }
    },
    'texts': {
        'aliases': {
            'api': {
                'singular': 'text',
                'plural': 'texts'
            },
            'db': {
                'singular': 'text',
                'plural': 'texts'
            }
        }
    },
}
# RESOURCES_under_consideration =\
#     [['api_singular', 'api_plural', 'db_singular', 'db_plural'],
#      ['characteristic', 'characteristics', 'characteristic',
#       'characteristics'],
#      ['...', '...', '...', '...']]


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
    return jsonify({
        'resultsSize': len(countries),
        'results': [c.full_json() for c in countries]
    })


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
    # print(request.args)
    surveys = Survey.query.all()
    return jsonify({
        'resultsSize': len(surveys),
        'results': [s.full_json() for s in surveys]
    })


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
    return jsonify({
        'resultsSize': len(indicators),
        'results': [
            i.full_json(endpoint='api.get_indicator') for i in indicators
        ]
    })


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
def get_characteristics():
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


@API.route('/characteristicGroups')
def get_characteristic_groups():
    """Characteristic Groups resource collection GET method.

    Returns:
        json: Collection for resource.
    """
    pass


@API.route('/characteristicGroups/<code>')
def get_characteristic_group(code):
    """Characteristi Groups resource entity GET method.

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
    return jsonify(json_obj = {
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
    return jsonify(json_obj = {
        'resultsSize': len(english_strings),
        'results': [d.to_json() for d in english_strings]
    })


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
    return jsonify({
        resource: {
            'name': resource,
            'resource':
                url_for('api.get_'+info['aliases']['db']['plural'],
                        _external=True)
        }
        for resource, info in RESOURCE_INFO.items()
    })
