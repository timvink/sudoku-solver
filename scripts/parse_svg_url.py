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
    url = "https://www.sudokuoftheday.com/image.svg?sg=934W(127)W6W(27)(178)5(18)(17)(15)6W(178)W(578)W4923(127)(125)8W9W(357)W(357)(17)468(129)(1239)W5W4W6(13)(19)76(49)(379)W(278)W1W(278)(348)(89)55(14)(17)W3W9W(78)(148)6236(59)4(58)127(89)47(29)6(238)(2389)5(18)(189)(12)8(1259)(27)(257)(2579)634"

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
