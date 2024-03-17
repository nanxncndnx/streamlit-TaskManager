import pandas as pd 
import nltk
nltk.download('punkt')
nltk.download('wordnet')
import re
from nltk.corpus import stopwords
nltk.download('stopwords')
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

data = pd.read_csv("job.csv")
del_col = ["Country", "latitude", "longitude", "Work Type", "Company Size", "Job Posting Date", "Preference", "Contact Person",
           "Contact", "Role", "Job Portal", "Benefits", "Company", "Company Profile", "Qualifications", "Salary Range", "location", "Experience"]

del_jobs = ['Teacher', 'Event Manager', 'Wedding Planner', 'QA Analyst', 'Litigation Attorney', 'Mechanical Engineer', 'Account Manager',
				'Brand Manager', 'Social Worker', 'Social Media Coordinator', 'Email Marketing Specialist', 'HR Generalist', 'Legal Assistant',
				'Nurse Practitioner', 'Account Director','Purchasing Agent', 'Sales Consultant', 'Civil Engineer', 'Financial Planner',
				'Event Planner', 'Psychologist', 'Electrical Designer', 'Technical Writer', 'Tax Consultant', 'Account Executive',
				'Research Analyst', 'Data Entry Clerk', 'Registered Nurse', 'Investment Analyst', 'Speech Therapist', 'Sales Manager', 'Landscape Architect',
				'Key Account Manager', 'UX Researcher', 'Investment Banker', 'Art Director', 'Customer Service Manager', 'Procurement Manager',
				'Substance Abuse Counselor', 'Supply Chain Analyst', 'Accountant', 'Sales Representative', 'Environmental Consultant',
				'Electrical Engineer', 'Systems Engineer', 'Art Teacher',  'Human Resources Manager', 'Inventory Analyst', 'Legal Counsel','Procurement Specialist',
				'Systems Analyst',  'Copywriter', 'Content Writer', 'HR Coordinator', 'Business Development Manager', 'Supply Chain Manager', 'Event Coordinator',
				'Family Nurse Practitioner', 'Customer Success Manager', 'Procurement Coordinator', 'Urban Planner',  'Architectural Designer', 'Financial Analyst',
				'Environmental Engineer', 'Structural Engineer', 'Market Research Analyst', 'Customer Service Representative',
				'Customer Support Specialist', 'Business Analyst', 'Social Media Manager', 'Family Lawyer',  'Chemical Analyst', 'Network Technician', 'Interior Designer',
				'Software Architect', 'Nurse Manager', 'Veterinarian', 'Process Engineer', 'Quality Assurance Analyst', 'Pharmaceutical Sales Representative',
				'Office Manager', 'Architect', 'Physician Assistant', 'Marketing Director',  'Research Scientist', 'Executive Assistant', 'HR Manager',
				'Marketing Manager', 'Public Relations Specialist', 'Financial Controller', 'Investment Advisor', 'Aerospace Engineer', 'Marketing Analyst', 'Paralegal',
				'Occupational Therapist', 'Landscape Designer', 'Legal Advisor', 'Marketing Coordinator', 'Dental Hygienist', 'Pediatrician', 'QA Engineer',
				'Financial Advisor', 'Personal Assistant',  'Network Analyst', 'Mechanical Designer', 'Marketing Specialist', 'Finance Manager', 'Physical Therapist',
				'Product Designer', 'Administrative Assistant', 'Brand Ambassador', 'Project Coordinator', 'Product Manager', 'Sales Associate',
				'Chemical Engineer', 'Legal Secretary', 'Market Analyst']

for D in del_col:
    data.drop(D , inplace = True, axis=1)

for R in del_jobs:
    data = data[data["Job Title"] != R]

#Just Responsibilities and Job Description -->
Col = ["Responsibilities", "Job Description"]

#Removing Tags
def remove_tags(info):
    remove = re.compile(r'')
    return re.sub(remove, '', info)

for tags in Col:
    data[tags] = data[tags].apply(remove_tags)

#Remove Special Characters
def special_char(info):
    reviews = ''
    for x in info:
        if x.isalnum():
            reviews = reviews + x
        else:
            reviews = reviews + ' '
    return reviews

for char in Col:
    data[char] = data[char].apply(special_char)

#Convert Everything in Lower Case
def convert_lower(info):
    return info.lower()

for lower in Col:
    data[lower] = data[lower].apply(convert_lower)
    data[lower][1]

#Remove all Stopwords
def remove_stopwords(info):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(info)
    return [x for x in words if x not in stop_words]

for stop in Col:
    data[stop] = data[stop].apply(remove_stopwords)
    data[stop][1]

#Lemmatizing the Words
def lemmatize_word(info):
    wordnet = WordNetLemmatizer()
    return " ".join([wordnet.lemmatize(word) for word in info])

for Lemmatizing in Col:
    data[Lemmatizing] = data[Lemmatizing].apply(lemmatize_word)
    data[Lemmatizing][1]

data.to_csv("clean_data.csv", index=False)
print(data)

