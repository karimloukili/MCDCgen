# --- Import functions from other modules ---
from expression_parser import parse_conditions
from truth_table_generator import generate_truth_table
from mcdc_logic import find_mcdc_pairs, select_mcdc_test_set
from display_utils import display_table
# Note: pandas is imported within display_utils if needed

# ==============================================================================
# Main Analysis Function (using imported components)
# ==============================================================================

def run_mcdc_analysis(expression):
    """
    Performs the complete MCDC analysis for a given expression string
    by calling functions from different modules.

    Args:
        expression (str): The boolean requirement expression.
    """
    print("-" * 60)
    print(f"Analyzing Requirement: {expression}")
    print("-" * 60)

    try:
        # 1. Parse Conditions (from expression_parser.py)
        conditions = parse_conditions(expression)
        print(f"\nIdentified Conditions: {conditions}")

        # 2. Generate Truth Table (from truth_table_generator.py)
        print("\nGenerating Truth Table...")
        truth_table = generate_truth_table(expression, conditions)

        # Proceed only if table generation was successful
        if not truth_table:
            print("\nAnalysis stopped due to issues generating the truth table.")
            print("-" * 60)
            return

        print("\nFull Truth Table (Decision Table):")
        # Use display function (from display_utils.py)
        display_table(truth_table, conditions)
        print("-" * 30)

        # 3. Find MCDC Pairs (from mcdc_logic.py)
        print("\nFinding MCDC Pairs...")
        mcdc_pairs = find_mcdc_pairs(truth_table, conditions)

        if not mcdc_pairs or not any(mcdc_pairs.values()):
            print("\nNo MCDC independence pairs found for any condition.")
            # Check if MCDC is impossible for specific conditions
            achievable_conditions = [c for c in conditions if c in mcdc_pairs and mcdc_pairs[c]]
            if len(achievable_conditions) < len(conditions):
                    print(f"MCDC cannot be achieved for conditions: {[c for c in conditions if c not in achievable_conditions]}")
            print("-" * 60)
            return # Stop if no pairs found or MCDC impossible

        print("\nMCDC Independence Pairs Found (Row Index Pairs):")
        all_conditions_have_pairs = True
        for condition in conditions:
            pairs = mcdc_pairs.get(condition, [])
            if pairs:
                print(f"  Condition '{condition}': {pairs}")
            else:
                # This case indicates MCDC is impossible for this condition
                print(f"  Condition '{condition}': --- No independence pairs found ---")
                all_conditions_have_pairs = False
        print("-" * 30)

        if not all_conditions_have_pairs:
                print("\nCannot select MCDC test set because not all conditions have independence pairs.")
                print("-" * 60)
                return # Stop analysis here

        # 4. Select Minimal MCDC Test Set (from mcdc_logic.py)
        print("\nSelecting Minimal MCDC Test Set...")
        selected_indices, coverage_map = select_mcdc_test_set(mcdc_pairs, conditions, len(truth_table))

        if coverage_map is not None: # Check if selection was successful
            print(f"\nSelected Test Set Indices ({len(selected_indices)} tests): {sorted(list(selected_indices))}")
            print("Coverage Map (Condition: Covering Pair Indices):")
            # Sort map by condition name for consistent output
            for cond in sorted(coverage_map.keys()):
                    print(f"  '{cond}': {coverage_map[cond]}")

            print("\nTruth Table with Selected MCDC Test Cases Highlighted:")
            # Use display function again (from display_utils.py)
            display_table(truth_table, conditions, selected_indices)
        else:
                print("\nFailed to determine a complete MCDC test set from the available pairs.")
                if selected_indices: # Show partial set if selection failed mid-way
                    print(f"Partial set covering some conditions: {sorted(list(selected_indices))}")

    except ValueError as ve:
        # Catch errors specifically from parse_conditions
        print(f"\nInput Error: {ve}")
    except Exception as e:
        # Catch potential errors during the overall process
        print(f"\nAn unexpected error occurred during analysis: {e}")
        import traceback
        traceback.print_exc() # Print detailed traceback for debugging

    print("-" * 60)


# ==============================================================================
# Script Execution (User Interaction)
# ==============================================================================

if __name__ == "__main__":
    print("=============================================")
    print(" MCDC Test Case Generator Tool ")
    print("=============================================")
    print("Enter boolean expressions using Python syntax (and, or, not).")
    print("Example: (A and B) or (C and not D)")

    while True:
        try:
            expression = input("\nEnter requirement expression (or type 'quit' to exit): ")
            if expression.strip().lower() == 'quit':
                break
            if not expression.strip():
                 print("Please enter an expression.")
                 continue

            # Run the analysis for the user-provided expression
            run_mcdc_analysis(expression)

        except EOFError: # Handle Ctrl+D
             print("\nExiting.")
             break
        except KeyboardInterrupt: # Handle Ctrl+C
             print("\nExiting.")
             break

    print("\nTool finished.")