import os
import re
import requests
from bs4 import BeautifulSoup


def get_platform(platform_url: str, directory = 'platform') -> None:
    response = requests.get(platform_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    card_div = soup.find('div', { 'class': 'card-body' })
    a_links = [a for a in card_div.find_all('a')]

    for a_link in a_links: 
        img = a_link.find('img')
        src, name = [img['src'], img['alt']]
        path = f"{directory}/{name}"

        if not os.path.exists(path):
            os.makedirs(path)

        filename = re.search(r'/([^/]+)$', src).group(1)
        with open(f"{path}/{filename}", 'wb') as f:
            f.write(requests.get(src).content)
