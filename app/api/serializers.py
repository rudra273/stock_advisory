from decimal import Decimal

def clean_decimal_nan(value):
    if isinstance(value, Decimal):
        if value.is_nan() or value.is_infinite():
            return None
    return value

def clean_orm_row(row):
    return {k: clean_decimal_nan(v) for k, v in row.__dict__.items() if not k.startswith("_")}
