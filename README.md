# streamlit-TaskManager
#### in this project :

 - you can create your account
 - you can creat team
 - you can apply for teams
 - you can generate the coverletter by ai using LLM
 - you can Add a task and My NLP classification will find the best member in your team who can do the task and automatically pass the task to that member

## 1. Job Classification
#### First of all i decided to just remove extra **Columns** because for example we dont need things like **Benefits** i Also remove extra jobs like **Teacher** , **Wedding Planner**, and others.

##### Next Part : 

 - Removing Tags
 - Remove Special Characters
 - Convert Everything in Lower Case
 - Remove all Stopwords
 - Lemmatizing the Words

The Dataset file has been transferred from **1.7GB** to **214.5MB**

#### To Classify the Jobs by Text i decided to use LogisticRegression model **you can see the full code [here](./DashBoard/Model.py)**


<p align="center" width="100%">
  <br>
  <br>
  Adding Task.<br>
 <img src="image/model.png">
 <br>
 <br>
</p>

## 2. Cover Letter Generator

##### LLaMa 2.0
- The heart of our Cover Letter Generator is the Llama 2 language model. It is Meta’s open source large language model.
- Replicate platform providing access to LLMs

## 3. Streamlit

##### Parts :
 
 - Authentication
 - Permissions
 - Applying to Teams
 - Offers
 - Adding Tasks & Creating Projects
 - Status of The Tasks in each Projects
 - Changing status of the Tasks by Members

<p align="center" width="100%">
 <br>
 <br>
 <img width="31%" src="image/status.png">
 <img width="33%" src="image/Tasks.png">
 <img width="33%" src="image/Offers.png">
 <br>
 <br>
</p>

## Usage

##### cleaning dataset **[code](./DashBoard/classification/clean.py)** 
```zsh
cd DashBoard/classification/
python3 clean.py
```

##### creating database manually with **Python & Sqlite3 [code](./data/create_data.py)** 
```zsh
cd data
python3 create_data.py
```

##### main **[code](./main.py)**
```zsh
streamlit run main.py
```

## Technology Used
##### **Streamlit, Pandas, Numpy, scikit-learn, matplotlib, Llama 2, replicate, nltk, NLP, SQL**