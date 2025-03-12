"""
Example usage:

uv run scripts/collect_training_data.py

# training data as JSON
collected_data = collect_sudoku_data(days=7)
save_to_json(collected_data, 'sudoku_data-2024-06-05-to-2024-06-14.json')

# single url parsing
url = "https://www.sudokuoftheday.com/dailypuzzles/2024-06-14/beginner"
sudoku_details = fetch_sudoku_details(url)
sudoku_details
"""
import os
import logging

# Configure logging based on environment variable
logging.basicConfig(
    level=os.environ.get('LOGLEVEL', 'INFO').upper(),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
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
    
    svg_url = img_tag['src']
    if not svg_url.startswith('http'):
        # If the URL is relative, make it absolute
        svg_url = requests.compat.urljoin(url, svg_url)
    
    # Step 3: Fetch the SVG content
    svg_response = requests.get(svg_url)
    svg_soup = BeautifulSoup(svg_response.content, 'xml')
    
    # Step 4: Parse the SVG content to extract the Sudoku board
    sudoku_board = parse_sudoku_svg(svg_soup)
    
    # Step 5: Extract the list of strategies from the techniques section
    techniques_div = soup.find('div', class_='techniquelist')
    strategies = []
    if techniques_div:
        strategies = [a.get_text().strip() for a in techniques_div.find_all('a')]
    
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


if __name__ == "__main__":
    # you can't go back more than 9 days, because the site only has data for the past 9 days
    data = collect_sudoku_data(days=6)
    today = datetime.now().strftime('%Y-%m-%d')
    ten_days_ago = (datetime.now() - timedelta(days=9)).strftime('%Y-%m-%d')
    save_to_json(data, f'tests/fixtures/sudoku_data-{ten_days_ago}-to-{today}.json')
