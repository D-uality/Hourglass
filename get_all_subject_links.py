"""
Creates json file with links to the official CAIE websites for every AS & A level subject.
"""

import requests
from bs4 import BeautifulSoup
import json


ALL_SUBJECTS_URL = r"https://www.cambridgeinternational.org/programmes-and-qualifications/cambridge-advanced/cambridge-international-as-and-a-levels/subjects/"
BASE_URL = r'https://www.cambridgeinternational.org'

response = requests.get(ALL_SUBJECTS_URL)
soup = BeautifulSoup(response.content, 'html.parser')
subjects = []

for link in soup.find_all('a'):
    href = link.get('href')
    if href and '/programmes-and-qualifications/cambridge-international-as-and-a-level' in href:
        SUBJECT_URL = BASE_URL + href

        # Use dictionary for json file
        subjects.append({
            'name': link.get_text(strip=True),
            'url': SUBJECT_URL
        })

with open('cie_subjects.json', 'w') as f:
    json.dump(subjects, f, indent=2)
