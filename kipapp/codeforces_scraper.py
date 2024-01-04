# yourapp/codeforces_scraper.py
import requests
from bs4 import BeautifulSoup

def get_codeforces_stats(handle):
    base_url = f'https://codeforces.com/profile/{handle}'
    final_url = base_url

    try:
        response = requests.get(final_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'lxml')

        # Extract Codeforces handle
        # codeforces_handle = soup.find('div', class_='info').find('span', class_='handle').text.strip()

        # Extract Codeforces rating
        rating_section = soup.find('span', class_='user-gray', style='font-weight:bold;')
        rating = rating_section.text.strip() if rating_section else 'No rating'

        # Extract the number of solved problems
        solved_problems_section = soup.find('div', class_='_UserActivityFrame_counterValue')
        solved_problems = int(solved_problems_section.text.split()[0]) if solved_problems_section else 0

        # Extract Codeforces rank
        rank_section = soup.find('span', class_='user-gray')
        rank = rank_section.text.strip() if rank_section else 'No rank'

        # Extract other relevant information based on the Codeforces website structure

        return {
            # 'codeforces_handle': codeforces_handle,
            'rating': rating,
            'solved_problems': solved_problems,
            'rank': rank,
            # Add more fields as needed
        }

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
