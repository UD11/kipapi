import requests
from bs4 import BeautifulSoup


def get_geeksforgeeks_stats(username):
    base_url = f'https://auth.geeksforgeeks.org/user/{username}/practice/'
    final_url = base_url

    try:
        response = requests.get(final_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'lxml')

        geeksforgeeks_username = soup.find('div', class_='profile_name').text.strip()

        overall_coding_score = float(soup.find('span', class_='score_card_value').text.strip())

        total_problems_solved = int(soup.find('span', class_='score_card_name', text='Total Problem Solved')
                                    .find_next_sibling('span', class_='score_card_value').text.strip())

        easy_section = soup.find('a', href='#easy')
        easy_solved = easy_section.text.split('(')[1].split(')')[0].strip() if easy_section else '0'

        medium_section = soup.find('a', href='#medium')
        medium_solved = medium_section.text.split('(')[1].split(')')[0].strip() if medium_section else '0'

        hard_section = soup.find('a', href='#hard')
        hard_solved = hard_section.text.split('(')[1].split(')')[0].strip() if hard_section else '0'

        return {
            'geeksforgeeks_username': geeksforgeeks_username,
            'total_problems_solved': total_problems_solved,
            'easy_solved': easy_solved,
            'medium_solved': medium_solved,
            'hard_solved': hard_solved,
            'overall_coding_score': overall_coding_score,
        }

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
