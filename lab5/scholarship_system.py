"""Screen scholarship applicants using merit scores and income criteria."""

import ast
import json
import operator

# Global state
results = {}
MERIT_FORMULA = "gpa * 10 + credits * 2"
INCOME_LIMIT = 800000
CUTOFF = 85


_ARITHMETIC_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
}


def _validate_expression(node):
    """Reject expression nodes outside the supported arithmetic grammar."""
    if isinstance(node, ast.Constant) and type(node.value) in (int, float):
        return
    if isinstance(node, ast.Name) and node.id in {"gpa", "credits"}:
        return
    if isinstance(node, ast.BinOp) and type(node.op) in _ARITHMETIC_OPERATORS:
        _validate_expression(node.left)
        _validate_expression(node.right)
        return
    if isinstance(node, ast.UnaryOp) and isinstance(
        node.op, (ast.UAdd, ast.USub)
    ):
        _validate_expression(node.operand)
        return
    raise ValueError("Unsupported expression in merit formula")


def _evaluate_expression(node, variables):
    """Evaluate one validated arithmetic expression node."""
    if isinstance(node, ast.Constant) and type(node.value) in (int, float):
        return node.value
    if isinstance(node, ast.Name) and node.id in variables:
        return variables[node.id]
    if isinstance(node, ast.BinOp):
        operation = _ARITHMETIC_OPERATORS.get(type(node.op))
        if operation is None:
            raise ValueError("Unsupported operator in merit formula")
        return operation(
            _evaluate_expression(node.left, variables),
            _evaluate_expression(node.right, variables),
        )
    if isinstance(node, ast.UnaryOp) and isinstance(
        node.op, (ast.UAdd, ast.USub)
    ):
        operand = _evaluate_expression(node.operand, variables)
        return operand if isinstance(node.op, ast.UAdd) else -operand
    raise ValueError("Unsupported expression in merit formula")


def _parse_formula(formula):
    """Parse and validate a configured merit formula."""
    try:
        expression = ast.parse(formula, mode="eval")
        _validate_expression(expression.body)
    except (RecursionError, SyntaxError, TypeError) as error:
        message = f"Invalid merit formula {formula!r}: {error}"
        raise ValueError(message) from error
    return expression.body


def _evaluate_formula(formula, gpa, extracurricular_credits):
    """Evaluate a formula for the supplied applicant values."""
    expression = _parse_formula(formula)
    try:
        return _evaluate_expression(
            expression, {"gpa": gpa, "credits": extracurricular_credits}
        )
    except (ArithmeticError, RecursionError, TypeError) as error:
        message = f"Invalid merit formula {formula!r}: {error}"
        raise ValueError(message) from error


def calculate_merit_score(gpa, extracurricular_credits):
    """Calculate an applicant's merit score using the configured formula."""
    return _evaluate_formula(MERIT_FORMULA, gpa, extracurricular_credits)


def evaluate_applicant(student_id, test_scores, logs=None):
    """Record an applicant's score and return their eligibility."""
    if logs is None:
        logs = []
    gpa = test_scores["gpa"]
    extracurricular_credits = test_scores.get("credits", 0)
    income = test_scores.get("income", 0)
    score = calculate_merit_score(gpa, extracurricular_credits)
    eligible = score >= CUTOFF and income < INCOME_LIMIT
    results[student_id] = {"score": score, "eligible": eligible}
    logs.append(f"{student_id} scored {score}")
    return eligible


def change_formula(new_formula):
    """Validate and select a new merit formula."""
    global MERIT_FORMULA
    _evaluate_formula(new_formula, 8.4, 3)
    MERIT_FORMULA = new_formula


def persist_results(file="scholarships.json"):
    """Write applicant results to a UTF-8 JSON file."""
    with open(file, "w", encoding="utf-8") as results_file:
        json.dump(results, results_file)


def load_results(file="scholarships.json"):
    """Load applicant results, reporting file and format errors."""
    try:
        with open(file, encoding="utf-8") as results_file:
            loaded_results = json.load(results_file)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        print(f"Could not load results from {file}: {error}")
        return
    if not isinstance(loaded_results, dict):
        print(f"Could not load results from {file}: expected a JSON object")
        return
    results.clear()
    results.update(loaded_results)


def print_shortlist():
    """Print applicants who meet the scholarship shortlist criteria."""
    print("Shortlisted applicants:")
    for student_id, applicant_result in results.items():
        if applicant_result["eligible"]:
            print(" ", student_id, "score =", applicant_result["score"])


def main():
    """Run the scholarship screener for the sample applicants."""
    evaluate_applicant("U001", {"gpa": 9.1, "credits": 4, "income": 450000})
    evaluate_applicant("U002", {"gpa": 7.2, "credits": 1, "income": 300000})
    evaluate_applicant("U003", {"gpa": 12.5, "credits": -3, "income": -1})
    evaluate_applicant("U004", {"gpa": 6.5})
    formula = input("Merit formula (Enter to keep default): ")
    if formula:
        try:
            change_formula(formula)
        except ValueError as error:
            print(f"Invalid merit formula; keeping default: {error}")
    evaluate_applicant("U005", {"gpa": 8.4, "credits": 3, "income": 600000})
    persist_results()
    load_results()
    print_shortlist()


if __name__ == "__main__":
    main()
