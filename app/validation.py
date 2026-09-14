def is_natural_number(value) -> bool:
    return isinstance(value, (int, float)) and value == int(value) and value >= 0


def is_positive_natural_number(value) -> bool:
    return is_natural_number(value) and value > 0


def bid_is_valid(value, budget) -> bool:
    return is_natural_number(value) and value <= budget
