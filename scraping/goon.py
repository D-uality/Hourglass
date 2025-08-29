import pymupdf
import json
import requests
from bs4 import BeautifulSoup
from scraping import overwrite

BASE = 'syllabuses'

with open(r'syllabuses\syllabus_pdfs.json', 'r') as f:
    syllabuses = json.load(f)
    for i in syllabuses:
        url = i["url"]
        subject = i["subject"]
        r = requests.get(url)
        path = f"{BASE}\{subject}.pdf"
        with open(path, 'wb') as pdf:
            pdf.write(r.content)
            print(f"{subject} Downloaded")
        overwrite(path)
        print(f"{subject} successfully overwritten.")
