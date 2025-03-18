#!/usr/bin/env python3
import sys
import urllib.parse

def parse_sg(s):
    """
    Parse the sudoku encoding string from the 'sg' parameter.
    Each cell is encoded by either:
      - A digit (1-9) for a solved cell
      - A set of digits in parentheses for a cell with pencil marks
    The 'W' prefix is just for styling and can be ignored.
    Returns a list of 81 integers (with 0 for empty cells).
    """
    tokens = []
    i = 0
    
    while i < len(s):
        # Skip any whitespace or W characters
        if s[i].isspace() or s[i] == 'W':
            i += 1
            continue
            
        # If we see a digit, that's a solved cell
        if s[i].isdigit():
            tokens.append(int(s[i]))
            i += 1
            continue
            
        # If we see an opening parenthesis, skip until closing parenthesis
        if s[i] == '(':
            tokens.append(0)  # Empty cell with pencil marks
            while i < len(s) and s[i] != ')':
                i += 1
            if i < len(s):
                i += 1  # Skip the closing parenthesis
            continue
            
        # Skip any other characters
        i += 1
            
    # Ensure exactly 81 cells
    return tokens[:81] if len(tokens) >= 81 else tokens + [0] * (81 - len(tokens))

def main():
    url = "https://www.sudokuoftheday.com/image.svg?sg=9(68)(24)(24)5173(68)1(46)73982(46)55(348)(234)(24)76(48)9181(69)72435(69)2(34)(349)165(489)(48)7(46)75983(46)12(46)21537(4689)(468)(4689)75864912339(46)81257(46)"

    # Parse URL to get query parameters
    parsed_url = urllib.parse.urlparse(url)
    query_params = urllib.parse.parse_qs(parsed_url.query)
    if 'sg' not in query_params:
        print("No sudoku parameter 'sg' found in the URL.")
        sys.exit(1)
    sg = query_params['sg'][0]

    tokens = parse_sg(sg)
    if len(tokens) != 81:
        print("Warning: Expected 81 cells, but parsed", len(tokens))
    
    # Convert the flat list into a 9x9 grid.
    grid = [tokens[i*9:(i+1)*9] for i in range(9)]
    print("[")
    for row in grid:
        print("\t", row, ",")
    print("]")
if __name__ == "__main__":
    main()
