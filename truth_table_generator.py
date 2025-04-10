import itertools

def generate_truth_table(expression, conditions):
    """
    Generates the full truth table (decision table) for a given expression.

    Args:
        expression (str): The boolean expression string.
        conditions (list): A list of condition names.

    Returns:
        list: A list of dictionaries, where each dictionary represents a row
              in the truth table. Keys are condition names and 'Decision'.
              Returns None if eval fails or expression is invalid.
    """
    n_conditions = len(conditions)
    table = []
    # Generate all possible combinations of True/False for the conditions
    for values in itertools.product([False, True], repeat=n_conditions):
        row = dict(zip(conditions, values))
        try:
            # Evaluate the expression with the current condition values
            # WARNING: eval() can be dangerous if the expression is untrusted.
            # Here, we assume the expression is valid boolean logic.
            decision = eval(expression, {}, row) # Provide row as local namespace
            row['Decision'] = bool(decision) # Ensure decision is boolean
            table.append(row)
        except SyntaxError as se:
             print(f"\nExpression Syntax Error: {se}")
             print("Please provide a valid Python boolean expression.")
             return None
        except NameError as ne:
             print(f"\nName Error: {ne}. Ensure all conditions are correctly identified.")
             print(f"Identified conditions were: {conditions}")
             return None
        except Exception as e:
            print(f"\nError evaluating expression for row {row}: {e}")
            return None
    return table

if __name__ == '__main__':
    # Example usage/test when run directly
    from expression_parser import parse_conditions # Need parser for testing
    test_expr = "(A and B) or C"
    try:
        conds = parse_conditions(test_expr)
        print(f"Testing expression: {test_expr}")
        print(f"Conditions: {conds}")
        table = generate_truth_table(test_expr, conds)
        if table:
            print("Generated Truth Table:")
            for i, row in enumerate(table):
                print(f"{i}: {row}")
        else:
            print("Failed to generate table.")

    except ValueError as e:
        print(f"Error during testing: {e}")

    test_expr_invalid = "A and B or (C and not D" # Missing parenthesis
    try:
        conds_invalid = parse_conditions(test_expr_invalid)
        print(f"\nTesting invalid expression: {test_expr_invalid}")
        print(f"Conditions: {conds_invalid}")
        table_invalid = generate_truth_table(test_expr_invalid, conds_invalid)
        if not table_invalid:
            print("Correctly handled invalid expression.")
    except ValueError as e:
         print(f"Error parsing invalid expression: {e}") # Parser might succeed here
    except Exception as e:
         print(f"Caught other error: {e}")