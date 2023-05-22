import requests
from bs4 import BeautifulSoup

from database import insert_record

init_url = 'https://djinni.co/jobs/?all-keywords=Data+Analyst&any-of-keywords=&exclude-keywords=&keywords=Data+Analyst'


def get_vacancy(li) -> tuple:
    href = 'https://djinni.co' + li.find('a', class_='profile').get('href')
    title = li.find('a', class_='profile').find('span').text
    company_name = \
        li.find('div', class_='mt-2'). \
            find('div', class_='list-jobs__details'). \
            find('div', class_='list-jobs__details__info'). \
            find('a').text.strip()

    current_vacancy = (title, company_name, href)
    return current_vacancy


def get_vacancy_list() -> list:
    result_list = []

    request = requests.get(init_url)
    src = request.text
    soup = BeautifulSoup(src, 'lxml')

    pages = int(soup.find(
        'ul', 'pagination'
    ).find_all('li', class_='page-item')[-2].find('a').text)

    list_jobs_current_page = soup.find('ul', class_='list-jobs').find_all('li')

    for li in list_jobs_current_page:
        current_vacancy = get_vacancy(li)

        if insert_record(current_vacancy[0], current_vacancy[1], current_vacancy[2]):
            result_list.append(current_vacancy)
        else:
            continue

    for page in range(2, pages + 1):
        request = requests.get(
            f'https://djinni.co/jobs/?all-keywords=Data+Analyst&any-of-keywords=&exclude-keywords=&keywords=Data+Analyst&page={page}'
        )
        src = request.text
        soup = BeautifulSoup(src, 'lxml')

        list_jobs_current_page = soup.find('ul', class_='list-jobs').find_all('li')

        for li in list_jobs_current_page:
            current_vacancy = get_vacancy(li)

            if insert_record(current_vacancy[0], current_vacancy[1], current_vacancy[2]):
                result_list.append(current_vacancy)
            else:
                continue

    return result_list




