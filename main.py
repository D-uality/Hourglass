from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")

client = OpenAI(
  api_key=api_key
)

class PastPaper:
  def __init__(self, file_path: str, topics: list[str]):
    # private __file_path: String
    # private __topics: List[String]
    # private __chatlog: List[Dictionary]
    self.__file_path = file_path
    self.__topics = topics
    self.__chatlog = []
  def get_file_path(self):
    return self.__file_path
  def get_topics(self):
    return self.__topics
  
  def add_topic(self, topic):
    self.__topics.append(topic)
  def del_topic(self, topic):
    if topic in self.__topics:
      self.__topics.remove(topic)
  def categorize(self):
    file = client.files.create(
      file=open(self.__file_path, "rb"),
      purpose="user_data"
    )
    completion = client.chat.completions.create(
      model="gpt-4o-mini",
      messages=[ 
        {"role": "developer", "content": "The user will input a file of a CIE GCE AS & A Level past examination, and a list of topics that the examination covers. If the file is not a CIE GCE AS & A Level exam, simply output 'invalid file'. Categorize the CIE Past Paper into the topics provided by the user. Ignore subparts of questions and instead categorize a question into multiple topics if the question covers multiple topics. Only categorize the questions as a whole and not as subparts (e.g. regard Question 3(a) and Question 3(b) as just Question 3). Use the following structure: Topic:(new line) Question number(new line)Question number, etc. Give a concise answer with no introduction or concluding questions."},
        {"role": "user",  
         "content": [ 
           {"type": "file",
            "file": {
              "file_id": file.id,
            }
            },
            {
              "type": "text",
              "text": ', '.join(self.__topics)
            },
         ]

         }
      ], 
    )
    return completion.choices[0].message.content

class MathsPastPaper(PastPaper):
  pass

class PhysicsPastPaper(PastPaper):
  pass

class CompSciPastPaper(PastPaper):
  pass

def identify(file_path): # checks if past paper code is 9709, 9702 or 9618.
  if "9709" in file_path:
    return "9709"
  elif "9702" in file_path:
    return "9702"
  elif "9618" in file_path:
    return "9618"
  else:
    return -1


chatlog = []



test = PastPaper(r"C:\Users\victo\Downloads\9709_w24_qp_13.pdf", ["Quadratics", "Functions", "Coordinate Geometry", "Circular Measure", "Trigonometry", "Series", "Other"])


print(test.categorize())


