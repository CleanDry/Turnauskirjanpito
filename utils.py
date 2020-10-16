from app import app

def validate_input(given_input, min_length, max_length):
    valid_input = True
    input_without_spaces = given_input.replace(" ", "")
    if len(given_input) < min_length:
        valid_input = False
    if len(given_input) > max_length:
        valid_input = False
    if not input_without_spaces.isalnum():
        valid_input = False
    return valid_input
