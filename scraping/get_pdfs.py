import json
import requests
from bs4 import BeautifulSoup

PATH = r'C:\Users\victo\OneDrive\Desktop\comp_programming\data_science\scraping\cie_subjects.json'
BASE_URL = r'https://www.cambridgeinternational.org'

try:
  with open(PATH, 'r') as f: 
    print("File loaded successfully")
    subjects = json.load(f)
except FileNotFoundError:
    print("File not found")
except json.JSONDecodeError:
    print("json could not be decoded")

syllabus_pdfs = []

for subject in subjects:

  # Clean data so subjects can be looked up/indexed via their 4 digit subject code
  url = subject["url"]
  subject["name"] = url.split('-')[-1]
  subject["name"] = subject["name"].replace("/", "")
  
  # Start scraping
  response = requests.get(subject["url"])
  soup = BeautifulSoup(response.content, "html.parser")

  for link in soup.find_all('a'):
    href = link.get('href')
    if href and "syllabus.pdf" in href:

      # Find the syllabus for 2025
      href_split = href.split('-')
      year = []
      for i in href_split:
        try:
            year.append(int(i))
        except:
            pass
      if (len(year) >= 2 and 2025 in range(year[0], year[1] + 1)) or (2025 in year):
        PDF_URL = BASE_URL + href
        print(f"Code: {subject["name"]}\n{PDF_URL}")
        syllabus_pdfs.append({
            "subject": subject["name"],
            "url": PDF_URL
        })

with open(r'scraping\syllabus_pdfs.json', 'w') as f:
    json.dump(syllabus_pdfs, f, indent=2)