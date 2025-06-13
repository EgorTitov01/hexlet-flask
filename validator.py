import re


def validate(user_data):
    errors = []
    if user_data.get('name') is not None:
        if not user_data['name']:
            errors.append('Fullfill your name')

        if not user_data['name'].isalpha():
            errors.append('Name should only consist of letters without whitespaces')

    if not user_data['email']:
        errors.append('Fullfill your email')

    email_pattern = re.compile(r".+@.+\.[a-z]+")
    if not email_pattern.fullmatch(user_data['email'].lower()):
        errors.append('Wrong email format')

    return errors