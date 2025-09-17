# chatbot/modules/calculator_module.py
from sympy import sympify, SympifyError, solve
from sympy.parsing.sympy_parser import (parse_expr, standard_transformations,
                                        implicit_multiplication_application)

transformations = (standard_transformations + (implicit_multiplication_application,))

def calculate(text):
    """
    If text contains '=' solve equation, otherwise evaluate expression.
    Example expressions: "2 + 3*4", "integrate x**2" (SymPy supports many ops)
    For safety we use sympy parsing.
    """
    try:
        # clean common words
        expr = text.strip().lower()
        # try equation
        if "=" in expr:
            lhs, rhs = expr.split("=", 1)
            sol = solve(parse_expr(lhs, transformations=transformations) - parse_expr(rhs, transformations=transformations))
            return f"Solution: {sol}"
        else:
            parsed = parse_expr(expr, transformations=transformations)
            val = parsed.evalf()
            return str(val)
    except (SympifyError, Exception) as e:
        return "Sorry, I couldn't parse/solve that expression. Try simpler math (e.g., 2*(3+4))"
