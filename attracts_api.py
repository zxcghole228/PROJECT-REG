import flask
from flask import jsonify
from data import db_session
from data.attarcts import Attractions


blueprint = flask.Blueprint(
    'attract_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/attract')
def get_attaracts():
    db_sess = db_session.create_session()
    attracts = db_sess.query(Attractions).all()
    return jsonify(
        {
            'news':
                [item.to_dict(only=('title', 'number', 'region', 'addres', 'categories', 'types', 'Unesko', 'Rare_obj'))
                 for item in attracts]
        }
    )