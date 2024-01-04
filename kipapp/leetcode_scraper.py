import requests
from bs4 import BeautifulSoup

def get_leetcode_stats(username):
    base_url = 'https://leetcode.com/'
    final_url = base_url + username

    try:
        response = requests.get(final_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'lxml')

        leetcode_username = soup.find('div', class_='text-label-3 dark:text-dark-label-3 text-xs').text
        candidate_name = soup.find('div', class_='text-label-1 dark:text-dark-label-1 break-all text-base font-semibold').text
        questions_done = int(soup.find('div', class_='text-[24px] font-medium text-label-1 dark:text-dark-label-1').text)
        easy_solved = int(soup.find_all('span', class_='mr-[5px] text-base font-medium leading-[20px] text-label-1 dark:text-dark-label-1')[0].text)
        medium_solved = int(soup.find_all('span', class_='mr-[5px] text-base font-medium leading-[20px] text-label-1 dark:text-dark-label-1')[1].text)
        hard_solved = int(soup.find_all('span', class_='mr-[5px] text-base font-medium leading-[20px] text-label-1 dark:text-dark-label-1')[2].text)
        contest_rating = soup.find('div', class_='text-label-1 dark:text-dark-label-1 flex items-center text-2xl').text
        total_active_days = int(soup.find_all('span', class_='font-medium text-label-2 dark:text-dark-label-2')[3].text)

        return {
            'leetcode_username': leetcode_username,
            'candidate_name': candidate_name,
            'questions_done': questions_done,
            'easy_solved': easy_solved,
            'medium_solved': medium_solved,
            'hard_solved': hard_solved,
            'contest_rating': contest_rating,
            'total_active_days': total_active_days,
        }

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
