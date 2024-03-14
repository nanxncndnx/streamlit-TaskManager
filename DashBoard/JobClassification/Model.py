import pandas as pd 
import numpy as np 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.metrics import make_scorer, roc_curve, roc_auc_score
from sklearn.metrics import precision_recall_fscore_support as score
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC, LinearSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB,MultinomialNB,BernoulliNB

def classificationModel():
    #i do not share csv files in github !!!
    data = pd.read_csv("clean_data.csv")
    data['Job_Title_Id'] = data['Job Title'].factorize()[0]

    data.to_csv("clean_data.csv", index = False)

    # you can use other field like Job Description and Responsibilities and skills
    x = data['skills']
    y = data['Job_Title_Id']

    x = np.array(data.iloc[:,0].values)
    y = np.array(data.Job_Title_Id.values)
    cv = CountVectorizer(max_features = 5000)
    #you need to change here also {data.skills} to other columns if you want!
    x = cv.fit_transform(data.skills).toarray()

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.3, random_state = 0, shuffle = True)

    # Create list of model and accuracy dicts
    perform_list = [ ]

    def run_model(model_name, est_c, est_pnlty):
        mdl = ""
        if model_name == 'Logistic Regression':
            mdl = LogisticRegression()
        elif model_name == 'Random Forest':
            mdl = RandomForestClassifier(n_estimators=100 ,criterion='entropy' , random_state=0)
        elif model_name == 'Multinomial Naive Bayes':
            mdl = MultinomialNB(alpha=1.0,fit_prior=True)
        elif model_name == 'Support Vector Classifer':
            mdl = SVC()
        elif model_name == 'Decision Tree Classifier':
            mdl = DecisionTreeClassifier()
        elif model_name == 'K Nearest Neighbour':
            mdl = KNeighborsClassifier(n_neighbors=10 , metric= 'minkowski' , p = 4)
        elif model_name == 'Gaussian Naive Bayes':
            mdl = GaussianNB()

        oneVsRest = OneVsRestClassifier(mdl)
        oneVsRest.fit(x_train, y_train)
        y_pred = oneVsRest.predict(x_test)

        # Performance metrics
        accuracy = round(accuracy_score(y_test, y_pred) * 100, 2)

        # Get precision, recall, f1 scores
        precision, recall, f1score, support = score(y_test, y_pred, average='micro')
        print(f'Test Accuracy Score of Basic {model_name}: % {accuracy}')
        print(f'Precision : {precision}')
        print(f'Recall : {recall}')
        print(f'F1-score : {f1score}')

        # Add performance parameters to list
        perform_list.append(dict([('Model', model_name),('Test Accuracy', round(accuracy, 2)),('Precision', round(precision, 2)),('Recall', round(recall, 2)),('F1', round(f1score, 2))]))

    #Logistic Regression
    #run_model('Logistic Regression', est_c=None, est_pnlty=None)

    #Random Forest
    #run_model('Random Forest', est_c=None, est_pnlty=None)

    #Multinomial Naive Bayes
    #run_model('Multinomial Naive Bayes', est_c=None, est_pnlty=None)

    #Support Vector Machine
    #run_model('Support Vector Classifer', est_c=None, est_pnlty=None)

    #Decision Tree
    #run_model('Decision Tree Classifier', est_c=None, est_pnlty=None)

    #KNN
    #run_model('K Nearest Neighbour', est_c=None, est_pnlty=None)

    #Gaussian Naive Bayes
    #run_model('Gaussian Naive Bayes', est_c=None, est_pnlty=None)

    #Create Dataframe of Model, Accuracy, Precision, Recall and F1
    """model_performance = pd.DataFrame(dataF = perform_list)
    model_performance = model_performance[['Model', 'Test Accuracy', 'Precision', 'Recall', 'F1']]
    print(model_performance)

    #Best Model to Perform Accuracy Score
    model = model_performance["Model"]
    max_value = model_performance["Test Accuracy"].max()
    print("The best accuracy of model is", max_value,"from Random")"""

    classifier = LogisticRegression().fit(x_train, y_train)

    value = input("PLease Explain The Task : ")

    y_pred1 = cv.transform([value])
    yy = classifier.predict(y_pred1)
    result = ""

    if yy == [0]:
        result = "Digital Marketing Specialist"
    elif yy == [1]:
        result = "Web Developer"
    elif yy == [2]:
        result = "Operations Manager"
    elif yy == [3]:
        result = "Network Engineer"
    elif yy == [4]:
        result = "Software Tester"
    elif yy == [5]:
        result = "UX/UI Designer"
    elif yy == [6]:
        result = "Network Administrator"
    elif yy == [7]:
        result = "Software Engineer"
    elif yy == [8]:
        result = "Network Security Specialist"
    elif yy == [9]:
        result = "UI Developer"
    elif yy == [10]:
        result = "Data Analyst"
    elif yy == [11]:
        result = "Systems Administrator"
    elif yy == [12]:
        result = "Database Administrator"
    elif yy == [14]:
        result = "IT Support Specialist"
    elif yy == [15]:
        result = "Project Manager"
    elif yy == [16]:
        result = "Data Engineer"
    elif yy == [17]:
        result = "Database Developer"
    elif yy == [18]:
        result = "Java Developer"
    elif yy == [19]:
        result = "Front-End Engineer"
    elif yy == [20]:
        result = "Back-End Developer"
    elif yy == [21]:
        result = "IT Manager"
    elif yy == [22]:
        result = "Front-End Developer"
    elif yy == [23]:
        result = "Web Designer"
    elif yy == [24]:
        result = "SEM Specialist"
    elif yy == [25]:
        result = "SEO Specialist"
    elif yy == [26]:
        result = "Data Scientist"
    elif yy == [27]:
        result = "SEO Analyst"
    elif yy == [28]:
        result = "Graphic Designer"
    elif yy == [29]:
        result = "IT Administrator"

    return result