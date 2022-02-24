"""

"""
from flask import Blueprint, jsonify, request, current_app
from flask_api import status
from app.models.main_db import TableA, TableASchema, db
from .utils import request_wrapper, create_payload_check, replace_payload_check


main_db_bp = Blueprint(
    'main_db_bp',
    __name__,
    template_folder='routes'
)


# Create
@main_db_bp.route('/api/1/tablea', methods=['POST'])
@request_wrapper
def create_tablea_record():
    """ Create record

    Example:
        r = requests.post(
            'http://127.0.0.1:5000/api/1/tablea',
            json={
                'name': "test',
                'data': {'x': 5}
            }
        )
        print(r.status_code)
        print(r.json())

    :return:
    """
    if request.method == 'POST':
        data = request.get_json()

        current_app.logger.info('Create tablea record')

        payload_check = create_payload_check(data, fields=['name', 'data'])
        if payload_check:
            return payload_check

        # Check name entry
        if not isinstance(data['name'], str):
            return jsonify({'error': 'name must be a str'}), status.HTTP_400_BAD_REQUEST

        # Check data entry
        if not isinstance(data['name'], dict):
            return jsonify({'error': 'data must be an object'}), status.HTTP_400_BAD_REQUEST

        record = TableA(
            name=data['name'],
            data=data['data']
        )
        db.session.add(record)
        db.session.commit()

        return jsonify({'id': record.id}), status.HTTP_201_CREATED


# Update
@main_db_bp.route('/api/1/tablea/<tid>', methods=['POST'])
@request_wrapper
def update_tablea_record(tid):
    """ Update a record.

    Example:
        r = requests.post(
            'http://127.0.0.1:5000/api/1/tablea/1',
            json={
                'patch': [
                    {
                        'op': 'replace',
                        'path': '/name',
                        'value': 'test2'
                    },
                    {
                        'op': 'replace',
                        'path': '/data',
                        'value': {'x': 6}
                    },
                ]
            }
        )
        print(r.status_code)
        print(r.json())

    :param tid:
    :return:
    """
    if request.method == 'POST':
        # Check if the record exists
        record = db.session.query(TableA).filter_by(
            id=tid
        ).with_entities(
            TableA.name,
            TableA.data
        ).first_or_404()

        current_name = record[0]
        current_data = record[1]

        # Update record
        data = request.get_json()

        update = replace_payload_check(data, ['/name', '/data'])
        if not update:
            return jsonify({'error': 'Invalid patch operation!'}), status.HTTP_400_BAD_REQUEST
        else:
            new_name = update.get('name', None)
            new_data = update.get('data', None)

            # Detect a change
            if new_name and new_name == current_name:
                return jsonify({'error': 'No change detected in the name field'}), status.HTTP_400_BAD_REQUEST

            if new_data and new_data == current_data:
                return jsonify({'error': 'No change detected in the data field'}), status.HTTP_400_BAD_REQUEST

            # Check name entry
            if new_name:
                if not isinstance(new_name, str):
                    return jsonify({'error': 'name must be a str'}), status.HTTP_400_BAD_REQUEST

            # Check data entry
            if new_data:
                if not isinstance(new_data, dict):
                    return jsonify({'error': 'data must be an object'}), status.HTTP_400_BAD_REQUEST

            # Update
            db.session.query(TableA).filter_by(
                id=tid
            ).update(
                update
            )
            db.session.commit()

            return jsonify({'id': tid}), status.HTTP_200_OK


# Delete
@main_db_bp.route('/api/1/tablea/<tid>', methods=['DELETE'])
@request_wrapper
def delete_tablea_record(tid):
    """ Delete a record.

    Example:
        r = requests.delete(
            'http://127.0.0.1:5000/api/1/tablea/1'
        )
        print(r.status_code)
        print(r.json())

    :param tid:
    :return:
    """
    if request.method == 'DELETE':
        # Check if the record exists
        db.session.query(TableA).filter_by(
            id=tid
        ).first_or_404()

        # Delete record
        db.session.query(TableA).filter_by(
            id=tid
        ).delete()
        db.session.commit()

        return jsonify({'id': tid}), status.HTTP_200_OK


# Get
@main_db_bp.route('/api/1/tablea/<tid>', methods=['GET'])
@request_wrapper
def get_tablea_record(tid):
    """ Get a record.

    Example:
        r = requests.get(
            'http://127.0.0.1:5000/api/1/tablea/1'
        )
        print(r.status_code)
        print(r.json())

    :param tid:
    :return:
    """
    if request.method == 'GET':

        schema = TableASchema()
        record = db.session.query(TableA).filter_by(
            id=tid
        ).first_or_404()

        result = schema.dump(record)

        return jsonify({'id': result}), status.HTTP_200_OK


# Search records by name
@main_db_bp.route('/api/1/tablea/collection/search_by_name/<name>', methods=['GET'])
@request_wrapper
def get_tablea_records_by_name(name):
    """ Get a record by name/partial name.

    Example:
        r = requests.get(
            'http://127.0.0.1:5000/api/1/collection/search_by_name/test'
        )
        print(r.status_code)
        print(r.json())

    :param name:
    :return:
    """
    if request.method == 'GET':

        schema = TableASchema(many=True, only=['id', 'name'])
        records = db.session.query(TableA).filter_by(
            is_active=True
        ).filter(
            TableA.name.ilike('%{name}%'.format(name=name))
        ).order_by(
            TableA.id
        ).all()

        result = schema.dump(records)

        return jsonify({'records': records}), status.HTTP_200_OK


# Get All
@main_db_bp.route('/api/1/tablea', methods=['GET'])
@request_wrapper
def get_tablea_records():
    """ Get all records.

    Example:
        r = requests.get(
            'http://127.0.0.1:5000/api/1/tablea'
        )
        print(r.status_code)
        print(r.json())

    :return:
    """
    if request.method == 'GET':

        schema = TableASchema(many=True, only=['id', 'name'])
        records = db.session.query(TableA).order_by(
            TableA.id
        ).all()

        result = schema.dump(records)

        return jsonify({'records': result}), status.HTTP_200_OK
