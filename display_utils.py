try:
    # Attempt to import pandas
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    # Set flag to False and pd to None if import fails
    PANDAS_AVAILABLE = False
    pd = None # Ensure pd is defined even if import fails


def display_table(table, conditions, selected_indices=None):
    """
    Displays the truth table using pandas for nice formatting if available,
    otherwise uses basic text formatting.

    Args:
        table (list): List of dictionaries representing the truth table.
        conditions (list): List of condition names.
        selected_indices (set, optional): Set of row indices to highlight. Defaults to None.
    """
    if not table:
        print("Cannot display empty table.")
        return

    if PANDAS_AVAILABLE:
        # Use pandas if it was successfully imported
        try:
            df = pd.DataFrame(table, columns=conditions + ['Decision'])
            df.index.name = "Index" # Add index column name

            if selected_indices is not None and selected_indices:
                # Highlight selected rows - create a style function
                def highlight_rows(row):
                    # Check if the row index (row.name) is in the set
                    color = 'background-color: yellow' if row.name in selected_indices else ''
                    return [color] * len(row)

                # Apply styling (requires pandas and jinja2 potentially)
                if hasattr(df, 'style') and hasattr(df.style, 'apply'):
                     # Use subset=None to apply to all columns
                     styled_df = df.style.apply(highlight_rows, axis=1, subset=None)
                     print("\n" + styled_df.to_string()) # Use to_string() for better console output
                else:
                     # Fallback if styling methods aren't fully available
                     print("\nPandas styling methods not available. Printing plain DataFrame.")
                     print(df)
                     print(f"\nSelected Row Indices for MCDC: {sorted(list(selected_indices))}")
            else:
                # Print without highlighting if no indices selected or selection is empty
                print("\n" + df.to_string())

        except Exception as e:
            print(f"\nError using pandas for display: {e}. Falling back to text.")
            _display_text_table(table, conditions, selected_indices) # Call fallback

    else:
        # Fallback if pandas is not installed
        print("\nPandas library not found. Displaying basic text table format.")
        _display_text_table(table, conditions, selected_indices)


def _display_text_table(table, conditions, selected_indices=None):
    """Internal function for basic text table display."""
    header = ['Index'] + conditions + ['Decision']
    # Calculate column widths based on header and data content (simple approach)
    col_widths = [len(h) for h in header]
    for i, row in enumerate(table):
         col_widths[0] = max(col_widths[0], len(str(i)))
         for idx, cond in enumerate(conditions):
              col_widths[idx+1] = max(col_widths[idx+1], len(str(row.get(cond, 'N/A'))))
         col_widths[-1] = max(col_widths[-1], len(str(row.get('Decision', 'N/A'))))

    # Add padding
    col_widths = [w + 2 for w in col_widths]

    # Print header
    print("".join(f"{h:<{col_widths[idx]}}" for idx, h in enumerate(header)))
    print("-" * sum(col_widths)) # Separator line

    # Print rows
    for i, row in enumerate(table):
        row_data = [i] + [row.get(cond, 'N/A') for cond in conditions] + [row.get('Decision', 'N/A')]
        row_str = "".join(f"{str(d):<{col_widths[idx]}}" for idx, d in enumerate(row_data))
        highlight = " *" if selected_indices is not None and i in selected_indices else ""
        print(f"{row_str}{highlight}")

    if selected_indices is not None and selected_indices:
         print(f"\nSelected Row Indices for MCDC: {sorted(list(selected_indices))}")


if __name__ == '__main__':
     # Example usage/test when run directly
     test_table = [
        {'A': False, 'B': False, 'Decision': False},
        {'A': False, 'B': True, 'Decision': True},
        {'A': True, 'B': False, 'Decision': False},
        {'A': True, 'B': True, 'Decision': True}
     ]
     test_conditions = ['A', 'B']
     test_selected = {1, 2}

     print("Testing display_table (Pandas if available, else text):")
     display_table(test_table, test_conditions, test_selected)

     print("\nTesting display_table without selection:")
     display_table(test_table, test_conditions)

     print("\nTesting display_table with empty selection:")
     display_table(test_table, test_conditions, set())
