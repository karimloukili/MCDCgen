# MCDC Test Case Generator

This Python tool helps generate a minimal set of test cases satisfying the Modified Condition/Decision Coverage (MCDC) criteria for a given boolean requirement expression. MCDC is a code coverage criterion often required by safety-critical standards like DO-178C/ED-12C in avionics.

## Features

* **Parses Conditions:** Identifies independent boolean conditions within a requirement expression.
* **Generates Truth Table:** Creates the full decision table showing the outcome for all possible condition combinations.
* **Finds MCDC Pairs:** Identifies pairs of test cases demonstrating the independent effect of each condition on the decision outcome.
* **Selects Minimal Test Set:** Uses a greedy algorithm to select a near-minimal set of test cases satisfying MCDC for all conditions.
* **Displays Results:** Presents the truth table, MCDC pairs, and the final selected test set (using `pandas` for nice formatting if installed).
* **Interactive:** Prompts the user to enter requirement expressions repeatedly until 'quit' is entered.
* **Modular:** Core logic is separated into distinct `.py` files:
    * `expression_parser.py`: Handles parsing conditions.
    * `truth_table_generator.py`: Handles truth table creation and expression evaluation.
    * `mcdc_logic.py`: Contains logic for finding MCDC pairs and selecting the test set.
    * `display_utils.py`: Handles formatting and printing the output tables.
    * `main.py`: The main executable script that orchestrates the process and handles user interaction.

## Requirements

* Python 3.x
* All `.py` files (`main.py`, `expression_parser.py`, `truth_table_generator.py`, `mcdc_logic.py`, `display_utils.py`) must be in the same directory.
* `pandas` (Optional, for nicely formatted table output with highlighting):
    ```bash
    pip install pandas
    ```
    (If pandas is not installed, the script will fall back to basic text-based table output).

## How to Use

1.  Ensure all the Python files (`main.py`, `expression_parser.py`, etc.) are in the same directory.
2.  Run the main script from your terminal:
    ```bash
    python main.py
    ```
3.  The script will prompt you to enter a requirement expression.
4.  Type your boolean expression using Python syntax (e.g., `(A and B) or (C and not D)`) and press Enter.
5.  The script will perform the MCDC analysis and display the results.
6.  It will then prompt you for another expression.
7.  Type 'quit' (case-insensitive) and press Enter to exit the tool.

## Limitations & Considerations

* **`eval()` Usage:** The script uses Python's `eval()`. **Do not run this script with arbitrary, untrusted input strings.** Assume the input represents known requirement logic.
* **Minimal Set:** The greedy algorithm provides a valid MCDC set, often minimal, but not guaranteed to be the absolute smallest in all cases.
* **Coupled Conditions:** Assumes conditions are independent. Does not explicitly handle "don't care" scenarios unless modeled in the input logic.

