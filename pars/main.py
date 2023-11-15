from bs4 import BeautifulSoup
import requests
import time
import json


HOST = 'https://www.google.com/search?q=dollar+to+som&rlz=1C5CHFA_enKG1065KG1069&oq=dollar+&gs_lcrp=EgZjaHJvbWUqBwgAEAAYgAQyBwgAEAAYgAQyBggBEEUYOTIPCAIQABgKGIMBGLEDGIAEMgcIAxAAGIAEMgcIBBAAGIAEMgcIBRAAGIAEMgcIBhAAGIAEMg8IBxAAGAoYgwEYsQMYgAQyBwgIEAAYgAQyBwgJEAAYgATSAQgyNDAwajFqNKgCALACAA&sourceid=chrome&ie=UTF-8'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'}


def check_currency():
    full_page = requests.get(HOST, headers=headers)

    soup = BeautifulSoup(full_page.content, 'html.parser')

    convert = soup.find_all("span", {'class': 'DFlfde SwHCTb', 'data-precision': 2})[0].text
    time.sleep(10)
    return convert


def write_to_json(data):
    with open('dollar.json', 'w') as dollar:
        json.dump(f'Dollar currency: {data}', dollar)


def main():
    data = check_currency()
    write_to_json(data)


if __name__ == '__main__':
    main()