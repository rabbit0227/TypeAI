from django.core.exceptions import ValidationError
import re

def validate_card_number(val):
    if not val.isdigit() or len(val) < 13 or len(val) > 19:
        raise ValidationError("Card number must be between 13 and 19 digits")
    
def validate_expiry(val):
    if not re.match(r'^(0[1-9]|1[0-2])/\d{2}$', val):
        raise ValidationError("Expiry must be in MM/YY format")

def validate_cvv(val):
    if not val.isdigit() or len(val) < 3 or len(val) > 4:
        raise ValidationError("Improper CVV must be either 3 or 4 digits long")