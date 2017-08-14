from flask import Blueprint, jsonify, request, url_for

from ..models import Country, EnglishString, Survey, Indicator, Data


api = Blueprint('api', __name__)
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


@api.route('/')
def say_hello():
    return '<h1>HELLO FLASK</h1>'


@api.route('/countries')
def get_countries():
    countries = Country.query.all()
    json_obj = {
        'resultsSize': len(countries),
        'results': [c.url_for() for c in countries]
    }
    return jsonify(json_obj)


@api.route('/countries/<code>')
def get_country(code):
    lang = request.args.get('_lang')
    country = Country.query.filter_by(country_code=code).first()
    json_obj = country.to_json(lang=lang)
    return jsonify(json_obj)


@api.route('/surveys')
def get_surveys():
    # Query by year, country, round
    print(request.args)
    surveys = Survey.query.all()
    json_obj = {
        'resultsSize': len(surveys),
        'results': [s.full_json() for s in surveys]
    }
    return jsonify(json_obj)


@api.route('/surveys/<code>')
def get_survey(code):
    survey = Survey.query.filter_by(code=code).first()
    json_obj = survey.full_json()
    return jsonify(json_obj)


@api.route('/indicators')
def get_indicators():
    indicators = Indicator.query.all()
    json_obj = {
        'resultsSize': len(indicators),
        'results': [
            i.full_json(endpoint='api.get_indicator') for i in indicators
        ]
    }
    return jsonify(json_obj)


@api.route('/indicators/<code>')
def get_indicator(code):
    indicator = Indicator.query.filter_by(code=code).first()
    json_obj = indicator.full_json()
    return jsonify(json_obj)


@api.route('/characteristics')
def get_characteristics():
    pass


@api.route('/characteristics/<code>')
def get_characteristic(code):
    pass


@api.route('/characteristicGroups')
def get_characteristic_groups():
    """Characteristic Groups resource collection GET method.

    Returns:
        json: Collection for resource.
    """
    pass


@api.route('/characteristicGroups/<code>')
def get_characteristic_group(code):
    """Characteristi Groups resource entity GET method.

    Args:
        code (str): Identification for resource entity.

    Returns:
        json: Entity of resource.
    """
    pass


@api.route('/data')
def get_data():
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
    qset = Data.query
    if 'survey' in args:
        qset = qset.filter(Data.survey.has(code=args['survey']))
    results = qset.all()
    return results

@api.route('/data/<uuid>')
def get_datum(uuid):
    data = Data.query.filter_by(code=uuid).first()
    json_obj = data.full_json()
    return jsonify(json_obj)


@api.route('/texts')
def get_texts():
    english_strings = EnglishString.query.all()
    json_obj = {
        'resultsSize': len(english_strings),
        'results': [eng.url_for() for eng in english_strings]
    }


@api.route('/texts/<uuid>')
def get_text(uuid):
    text = EnglishString.query.filter_by(uuid=uuid).first()
    json_obj = text.to_json()
    return jsonify(json_obj)


@api.route('/resources')
def get_resources():
    return jsonify({
        resource: {
            'name': resource,
            'resource':
                url_for('api.get_'+info['aliases']['db']['plural'],
                        _external=True)
        }
        for resource, info in RESOURCE_INFO.items()
    })
