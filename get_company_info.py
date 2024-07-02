import requests


def get_company_info(company_name):
    API_KEY = "AIzaSyDgygjZC4w1Mik2Lj4w6X4ir6fxaSD0Q9s"
    url = f'https://kgsearch.googleapis.com/v1/entities:search'
    params = {
        'query': company_name,
        'key': API_KEY,
        'limit': 1,
        'indent': True,
    }

    response = requests.get(url, params=params)
    data = response.json()

    if 'itemListElement' in data and len(data['itemListElement']) > 0:
        element = data['itemListElement'][0]['result']
        description = element.get('description', 'No description available')
        detailed_description = element.get('detailedDescription', {}).get(
            'articleBody', 'No detailed description available')
        return description, detailed_description
    else:
        return None, None


company_name = "NVIDIA"
description, detailed_description = get_company_info(company_name)

print(f"Description: {description}")
print(f"Detailed Description: {detailed_description}")
