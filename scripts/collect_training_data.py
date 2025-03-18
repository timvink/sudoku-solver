"""
Example usage:

$> uv run scripts/collect_training_data.py
$> uv run scripts/collect_training_data.py --date YYYY-MM-DD

Run this in a loop for the last 7 days:

```bash
for i in {0..6}; do
  date=$(date -d "-$i day" +%Y-%m-%d)
  uv run scripts/collect_training_data.py --date $date
done
```

"""
import os
import logging
from requests.compat import urljoin
import argparse

# Configure logging based on environment variable
logging.basicConfig(
    level=os.environ.get('LOGLEVEL', 'INFO').upper(),
    format='%(asctime)s - %(name)s - %(livename)s - %(message)s'
)

from datetime import datetime, timedelta
import json

import requests
from bs4 import BeautifulSoup

def fetch_sudoku_details(url):
    # Step 1: Fetch the webpage content
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Step 2: Extract the URL of the SVG image from the <img> tag with class "puzzle"
    img_tag = soup.find('img', class_='puzzle')
    if img_tag is None:
        raise ValueError("No image tag with class 'puzzle' found on the page.")
    
    svg_url = str(img_tag['src']) # type: ignore
    if not svg_url.startswith('http'):
        # If the URL is relative, make it absolute
        svg_url = urljoin(url, svg_url)
    
    # Step 3: Fetch the SVG content
    svg_response = requests.get(svg_url)
    svg_soup = BeautifulSoup(svg_response.content, 'xml')
    
    # Step 4: Parse the SVG content to extract the Sudoku board
    sudoku_board = parse_sudoku_svg(svg_soup)
    
    # Step 5: Extract the list of strategies from the techniques section
    techniques_div = soup.find('div', class_='techniquelist')
    strategies = []
    if techniques_div:
        strategies = [a.get_text().strip() for a in techniques_div.find_all('a')] # type: ignore
    
    return {
        'url': url,
        'strategies': strategies,
        'puzzle': sudoku_board
    }

def parse_sudoku_svg(soup):
    # Initialize an empty 9x9 Sudoku board
    board = [[0 for _ in range(9)] for _ in range(9)]
    
    # Find all text elements which contain the numbers
    text_elements = soup.find_all('text')
    
    for text in text_elements:
        x = float(text['x'])
        y = float(text['y'])
        value = text.get_text().strip()
        
        if value.isdigit():
            value = int(value)
        else:
            value = 0  # Treat non-digits as empty cells
        
        # Determine the row and column based on x and y coordinates
        col = int((x - 8) / 111)
        row = int((y - 8) / 111)
        
        if 0 <= row < 9 and 0 <= col < 9:
            board[row][col] = value
    
    return board



def collect_sudoku_data(days=10):
    base_url = "https://www.sudokuoftheday.com/dailypuzzles/"
    levels = ['beginner', 'easy', 'medium', 'tricky', 'fiendish', 'diabolical']
    collected_data = []

    for i in range(days):
        date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
        for level in levels:
            url = f"{base_url}{date}/{level}"
            try:
                data = fetch_sudoku_details(url)
                collected_data.append(data)
            except Exception as e:
                logging.error(f"Error fetching data for {date} {level}: {e}")
        import time
        print(f'collected {date}')
        time.sleep(1)
    
    return collected_data

def save_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def read_from_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def main():
    parser = argparse.ArgumentParser(description='Collect Sudoku training data for a specific date.')
    parser.add_argument('--date', type=str, help='Date in YYYY-MM-DD format. Defaults to today if not specified.')
    args = parser.parse_args()

    # Determine the date to collect data for
    if args.date:
        try:
            date = datetime.strptime(args.date, '%Y-%m-%d')
        except ValueError:
            raise ValueError('Date must be in YYYY-MM-DD format.')
    else:
        date = datetime.now()

    # Collect data for the specified date
    data = collect_sudoku_data_for_date(date)
    filename = f'tests/fixtures/sudoku_data-{date.strftime("%Y-%m-%d")}.json'
    save_to_json(data, filename)

    print(f'Data collected and saved to {filename}')

def collect_sudoku_data_for_date(date):
    base_url = "https://www.sudokuoftheday.com/dailypuzzles/"
    levels = ['beginner', 'easy', 'medium', 'tricky', 'fiendish', 'diabolical']
    collected_data = []

    date_str = date.strftime('%Y-%m-%d')
    for level in levels:
        url = f"{base_url}{date_str}/{level}"
        try:
            data = fetch_sudoku_details(url)
            collected_data.append(data)
        except Exception as e:
            logging.error(f"Error fetching data for {date_str} {level}: {e}")

    return collected_data

if __name__ == "__main__":
    main()
