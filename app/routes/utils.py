"""

"""
from flask import current_app, request, jsonify
from flask_api import status
from functools import wraps


# ---------- Decorators ---------- #
def request_wrapper(orig_func):
    @wraps(orig_func)
    def wrapper(*args, **kwargs):
        current_app.logger.info(f'{request.method} - {request.url} ({request.is_secure})')
        try:
            return orig_func(*args, **kwargs)
        except Exception as error:
            error_msg = f'{type(error).__name__}: {error}'
            current_app.logger.error(f'{error_msg}')
            current_app.logger.exception(error)

            if '404' in error_msg:
                return {'error': error_msg}, status.HTTP_404_NOT_FOUND
            else:
                return {'error': error_msg}, status.HTTP_500_INTERNAL_SERVER_ERROR

    return wrapper


def request_auth_wrapper(orig_func):
    @wraps(orig_func)
    def wrapper(*args, **kwargs):
        current_app.logger.info(f'{request.method} - {request.url} ({request.is_secure})')
        auth_token = request.headers.get('X-Auth-Token', None)
        if auth_token == 'XYZ':
            return orig_func(*args, **kwargs)
        else:
            current_app.logger.error('Unauthorized')
            return jsonify({'error': 'Unauthorized'}), status.HTTP_401_UNAUTHORIZED

    return wrapper


#  ---------- Helpers ---------- #
def create_payload_check(payload, fields=None):
    for field in fields:
        if field not in payload or not payload[field]:
            return jsonify({'error': f'{field} field is required and needs content.'}), status.HTTP_400_BAD_REQUEST


def check_payload(payload, fields=None, allow_optional_fields=False, skip_null_check=False, skip_type_check=False):
    """ Test request.get_json() keys

    Example:

        payload = request.get_json()
        fields = [
            ('key', str)
        ]

    :param payload:
    :param fields:
    :param allow_optional_fields:
    :param skip_null_check:
    :param skip_type_check:
    :return:
    """
    for field, data_type in fields:
        # Null check
        if not skip_null_check:
            if field not in payload or not payload[field]:
                return jsonify({'error': f'{field} field is required and needs content.'}), status.HTTP_400_BAD_REQUEST
        else:
            if field not in payload:
                return jsonify({'error': f'{field} field is required.'}), status.HTTP_400_BAD_REQUEST
        # Data type check
        if not skip_type_check:
            if data_type and not isinstance(payload[field], data_type):
                return jsonify({'error': f'{field} field has to be of type {data_type}'}), status.HTTP_400_BAD_REQUEST

    if not allow_optional_fields:
        for k in payload.keys():
            if k not in [f[0] for f in fields]:
                return jsonify({'error': f'Extraneous field {k}'}), status.HTTP_400_BAD_REQUEST


def replace_payload_check(payload, fields=None):
    update_dict = dict()
    if 'patch' in payload:
        for patch in payload['patch']:
            if 'op' in patch and patch['op'] == 'replace':
                if 'path' in patch and 'value' in patch and any([field == patch['path'] for field in fields]):
                    update_dict[patch['path'].replace('/', '')] = patch['value']
    return update_dict


def replace_payload_check2(payload, fields=None):
    update_dict = dict()
    extraneous_fields = []

    if 'patch' in payload:
        for patch in payload['patch']:
            if 'op' in patch and patch['op'] == 'replace':
                if 'path' in patch and 'value' in patch and any([field == patch['path'] for field in fields]):
                    update_dict[patch['path'].replace('/', '')] = patch['value']
                elif 'path' in patch and 'value' in patch and not any([field == patch['path'] for field in fields]):
                    extraneous_fields.append(patch['path'])

    return update_dict, extraneous_fields
