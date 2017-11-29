from django.core.exceptions import ValidationError

def validate_quantity(value):
    if not value < 5:
        raise ValidationError("Valor superior ao estoque.")