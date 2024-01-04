# yourapp/codechef_scraper.py
import requests
from bs4 import BeautifulSoup


def get_codechef_stats(username):
    base_url = f'https://www.codechef.com/users/{username}'
    final_url = base_url

    try:
        response = requests.get(final_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'lxml')

        codechef_username = soup.find('h1', class_='h2-style').text.strip()

        rating = soup.find('div', class_='rating-number').text.strip()

        division_section = soup.find('div', class_='rating-number').find_next_sibling('div')
        division = division_section.text.strip() if division_section else 'No division'

        stars_section = soup.find('span', class_='rating')
        stars = stars_section.text.strip() if stars_section else 'No stars'

        problems_solved_section = soup.find('tspan', class_='highcharts-text-outline')
        problems_solved = int(problems_solved_section.text.strip()) if problems_solved_section else 0

        contests_section = soup.find('b')
        contests_participated = int(contests_section.text.strip()) if contests_section else 00

        return {
            'codechef_username': codechef_username,
            'rating': rating,
            'division': division,
            'stars': stars,
            'practice_problems_solved': problems_solved,
            'contests_participated': contests_participated,

        }

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
