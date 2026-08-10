import re

def validate_input(data):
    if not isinstance(data, str):
        return False, 'Input must be a string.'
    if len(data) < 3:
        return False, 'Input is too short, must be at least 3 characters.'
    if len(data) > 100:
        return False, 'Input is too long, must be 100 characters or less.'
    if not re.match('^[a-zA-Z0-9_ ]+$', data):
        return False, 'Input must contain only alphanumeric characters and underscores.'
    return True, 'Input is valid.'

