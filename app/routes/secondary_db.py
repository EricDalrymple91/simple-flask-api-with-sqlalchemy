"""

"""
from flask import Blueprint, jsonify, request, current_app
from flask_api import status
from app.models.secondary_db import TableB, db
from .utils import request_wrapper, create_payload_check

secondary_db_bp = Blueprint(
    'secondary_db_bp',
    __name__,
    template_folder='routes'
)


# Create
@secondary_db_bp.route('/api/1/tableb', methods=['POST'])
@request_wrapper
def create_tablea_record():
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
            return jsonify({'error': 'name must be an object'}), status.HTTP_400_BAD_REQUEST

        # Check is_operational entry
        if 'is_operational' in data:
            if not isinstance(data['is_operational'], bool):
                return jsonify({'error': 'is_operational must be a bool'}), status.HTTP_400_BAD_REQUEST

        record = TableB(
            name=data['name'],
            data=data['data'],
            is_operational=data.get('is_operational', None)
        )
        db.session.add(record)
        db.session.commit()

        return jsonify({'id': record.id}), status.HTTP_201_CREATED
