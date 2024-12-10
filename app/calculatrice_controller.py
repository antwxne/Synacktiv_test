class InvalidExpression(RuntimeError):
    pass


def valid_expression(expr: str) -> bool:
    valid_chars: str = "1234567890()+*/- "
    return all(map(lambda c: c in valid_chars, expr))


def calculatrice_controller(expr: str) -> int:
    if not valid_expression(expr):
        raise InvalidExpression
    return eval(expr)
