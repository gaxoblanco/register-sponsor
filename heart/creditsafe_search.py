import requests
from bs4 import BeautifulSoup
import time
import json


def get_company_info(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        h1 = soup.find('h1')
        return h1.text.strip() if h1 else 'N/A'
    except requests.exceptions.RequestException as e:
        print(f'Error fetching {url}: {e}')
        return 'N/A'


def get_information(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Search the div who have x-show="industry"
        div = soup.find('div', {'x-show': 'industry'})
        industry = div.text.strip() if div else 'N/A'

        # Search the img for the logo
        img = soup.find('img', class_='w-75 m-auto cursor-pointer',
                        alt='Klik hier voor het volledige kredietrapport')
        img_src = img['src'] if img else 'N/A'  # type: ignore

        return {
            'industry': industry,
            'logo_url': img_src
        }
    except requests.exceptions.RequestException as e:
        print(f'Error fetching {url}: {e}')
        return {
            'industry': 'N/A',
            'logo_url': 'N/A'
        }


def scrape_creditsafe(kvk_number):
    url = f"https://www.creditsafe.com/business-index/nl-nl/search?searchQuery=&number={kvk_number}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')  # type: ignore
        view_company_button = soup.select_one('a[href*="company/id"]')
        if view_company_button:
            company_url = view_company_button['href']
            if not company_url.startswith('https://'):  # type: ignore
                company_url = 'https://www.creditsafe.com' + company_url  # type: ignore
            company_info = get_company_info(company_url)
            print(f"Company URL: {company_info}")
            information = get_information(company_url)
            print(f"Company Img: {information['logo_url']}")
            return {
                'kvk_number': kvk_number,
                'company_url': company_url,
                'company_name': company_info,
                'industry': information['industry'],
                'logo_url': information['logo_url']
            }
        else:
            return {
                'kvk_number': kvk_number,
                'error': f'Error fetching {url}'
            }
    except requests.exceptions.RequestException as e:
        print(f'Error fetching {url}: {e}')
        return {
            'kvk_number': kvk_number,
            'error': f'Error fetching {url}: {str(e)}'
        }


def update_json(result):
    with open('sponsors.json', 'r+') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            data = []

        # Find and update the existing entry or append a new one
        updated = False
        for entry in data:
            if entry.get('id') == result['kvk_number']:
                entry.update(result)
                updated = True
                break

        if not updated:
            data.append(result)

        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()


def main():
    with open('sponsors.json', 'r') as file:
        sponsors = json.load(file)

    for i, sponsor in enumerate(sponsors, 1):
        kvk_number = sponsor.get('id')

        # Skip if this entry have company_url
        if sponsor.get('logo_url'):
            print(
                f"Skipping {i}/{len(sponsors)}: {kvk_number} already has company_url")
            continue

        if kvk_number:
            print(f"Processing {i}/{len(sponsors)}: KvK number {kvk_number}")
            result = scrape_creditsafe(kvk_number)
            update_json(result)
            # time.sleep(2)  # Add a 2-second delay between requests
        else:
            print(f"Missing KvK number for sponsor: {sponsor}")


if __name__ == "__main__":
    main()
