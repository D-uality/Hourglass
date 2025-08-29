import pymupdf
import json
import requests
from bs4 import BeautifulSoup

def get_all_subject_links():
    ALL_SUBJECTS_URL = r"https://www.cambridgeinternational.org/programmes-and-qualifications/cambridge-advanced/cambridge-international-as-and-a-levels/subjects/"
    BASE_URL = r'https://www.cambridgeinternational.org'

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



def get_pdfs(yr: int):
    PATH = r'syllabuses\cie_subjects_dummy.json'
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
                
                if (len(year) >= 2 and yr in range(year[0], year[1] + 1)) or (yr in year):
                    PDF_URL = BASE_URL + href
                    print(f"Code: {subject['name']}\n{PDF_URL}")
                    syllabus_pdfs.append({
                        "subject": subject["name"],
                        "url": PDF_URL
                    })

    with open(r'syllabuses\syllabus_pdfs.json', 'w') as f:
        json.dump(syllabus_pdfs, f, indent=2)

def parse_syllabus(pdf_file):
    """
    Returns range of page numbers in syllabus containing the subject content.
    """
    pages = None
    doc = pymupdf.open(pdf_file)
    toc = doc.get_toc() # gets all bookmarks

    start = 0
    end = -1
    i = -1
    while start > end and i < len(toc)-1:
        i += 1
        if 'subject content' in toc[i][1].casefold() and start == 0:
            start = toc[i][2]
        elif start > 0 and toc[i][0] == 1:
            end = toc[i][2]
            
    if start < end:
        pages = range(start, end)
    doc.close()

    return pages
