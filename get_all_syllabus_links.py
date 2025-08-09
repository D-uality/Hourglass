import requests
from bs4 import BeautifulSoup
import json


ALL_SUBJECTS_URL = r"https://www.cambridgeinternational.org/programmes-and-qualifications/cambridge-advanced/cambridge-international-as-and-a-levels/subjects/"
BASE_URL = r'https://www.cambridgeinternational.org'


# def scrape(url):

response = requests.get(ALL_SUBJECTS_URL)
soup = BeautifulSoup(response.content, 'html.parser')
subjects = []

for link in soup.find_all('a'):
    href = link.get('href')
    if href and '/programmes-and-qualifications/cambridge-international-as-and-a-level' in href:
        SUBJECT_URL = BASE_URL + href
        subjects.append({
            'name': link.get_text(strip=True),
            'url': SUBJECT_URL
        })

with open('cie_subjects.json', 'w') as f:
    json.dump(subjects, f, indent=2)
# SUBJECT_URL = BASE_URL + href
# subject_response = requests.get(SUBJECT_URL)
# subject_soup = BeautifulSoup(subject_response.content, 'html.parser')
