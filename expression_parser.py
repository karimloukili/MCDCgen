import re

def parse_conditions(expression):
    """
    Parses a boolean expression string to find unique condition variables.
    Assumes conditions are valid Python variable names (letters, numbers, underscore).
    Excludes Python keywords 'and', 'or', 'not'.

    Args:
        expression (str): The boolean expression string (e.g., "(A and B) or C").

    Returns:
        list: A sorted list of unique condition names found in the expression.

    Raises:
        ValueError: If no conditions are found in the expression.
    """
    # Find all potential identifiers
    identifiers = re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', expression)
    # Filter out Python keywords
    keywords = {'and', 'or', 'not', 'True', 'False'}
    conditions = sorted(list(set(iden for iden in identifiers if iden not in keywords)))
    if not conditions:
        raise ValueError("No conditions found in the expression.")
    return conditions

if __name__ == '__main__':
    # Example usage/test when run directly
    test_expr = "(Reset or (M1 and M2)) and not Deactivate"
    try:
        conds = parse_conditions(test_expr)
        print(f"Testing expression: {test_expr}")
        print(f"Parsed conditions: {conds}")
    except ValueError as e:
        print(f"Error testing parser: {e}")

    test_expr_2 = "A and B"
    try:
        conds_2 = parse_conditions(test_expr_2)
        print(f"\nTesting expression: {test_expr_2}")
        print(f"Parsed conditions: {conds_2}")
    except ValueError as e:
        print(f"Error testing parser: {e}")

    test_expr_3 = "only_keywords and or not"
    try:
        conds_3 = parse_conditions(test_expr_3)
        print(f"\nTesting expression: {test_expr_3}")
        print(f"Parsed conditions: {conds_3}") # Should raise error or be empty
    except ValueError as e:
        print(f"\nTesting expression: {test_expr_3}")
        print(f"Correctly handled error: {e}")