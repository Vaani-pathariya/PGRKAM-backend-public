import pandas as pd
import numpy as np
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import sigmoid_kernel

# Read the CSV file
df1 = pd.read_csv('new2.csv', error_bad_lines=False, engine='python')
df1 = df1.dropna()

# Use TfidfVectorizer to create a TF-IDF matrix
tfidf = TfidfVectorizer(stop_words='english')
df1['jobdescription'] = df1['jobdescription'].fillna('')
tfidf_matrix = tfidf.fit_transform(df1['jobdescription'])

# Use sigmoid_kernel to calculate the cosine similarity
cosine_sim = sigmoid_kernel(tfidf_matrix, tfidf_matrix)
indices = pd.Series(df1.index, index=df1['jobtitle']).drop_duplicates()

def get_recommendations(title, salary=None, experience=None, education=None, cosine_sim=cosine_sim):
    # Get index of the given job title
    idx = indices[title]

    # Get the cosine similarity scores
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Use numpy array for sorting
    sim_scores = np.array(sorted(sim_scores, key=lambda x: x[1], reverse=True), dtype=object)

    # Extract indices after sorting
    tech_indices = sim_scores[1:16, 0].astype(int)

    # Apply additional filters
    filtered_jobs = df1.iloc[tech_indices]
    
    if salary:
        filtered_jobs = filtered_jobs[filtered_jobs['salary'] == salary]

    if experience:
        filtered_jobs = filtered_jobs[filtered_jobs['experience'] == experience]

    if education:
        filtered_jobs = filtered_jobs[filtered_jobs['education'] == education]

    return filtered_jobs['jobtitle']

# Load the job list from pickle
jobs = pickle.load(open('job_list2.pkl', 'rb'))

# Get a list of job titles
job_titles = jobs['jobtitle'].values

# Select a job title for which you want recommendations
selected_job_title = job_titles[5] # SAP FICO Architect
print(selected_job_title)
# Set filter values (replace with your actual filter values)
salary_filter = "10,000"
experience_filter = 0
education_filter = "Graduate"

# Get and print recommended job titles with filters
recommended_jobs = get_recommendations(selected_job_title, salary=salary_filter, experience=experience_filter, education=education_filter)
for job in recommended_jobs:
    print(job)
