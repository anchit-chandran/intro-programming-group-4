import re

def validate_field_has_input(form_input: str) -> list[str]:
    """Performs basic validation of input. Returns list of errors if any."""
    errors = []
    
    # Empty input
    if not form_input.strip():
        errors.append("Field cannot be blank.")

    return errors


def is_valid_email(email:str)-> bool:
    """Validates email.
    Thanks  https://stackabuse.com/python-validate-email-address-with-regular-expressions-regex/
    """
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    if re.fullmatch(regex, email):
      return True
    else:
      return False