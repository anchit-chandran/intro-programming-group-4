def validate_field_has_input(form_input: str) -> list[str]:
    """Performs basic validation of input. Returns list of errors if any."""
    errors = []
    
    # Empty input
    if not form_input.strip():
        errors.append("Field cannot be blank.")

    return errors