import pandas as pd
import numpy as np
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import sigmoid_kernel

# Read the CSV file
df1 = pd.read_csv('new2.csv',engine='python')
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

    if salary is not None:
        salary = float(salary.replace(',', ''))
        filtered_jobs = filtered_jobs[filtered_jobs['salary'].astype(float) == salary]

    if experience is not None:
        filtered_jobs = filtered_jobs[filtered_jobs['experience'].astype(float) == float(experience)]

    if education is not None:
        filtered_jobs = filtered_jobs[filtered_jobs['education'] == education]

    return filtered_jobs['jobtitle']

# Load the job list from pickle
jobs = pickle.load(open('job_list2.pkl', 'rb'))

# Get a list of job titles
job_titles = jobs['jobtitle'].values

# Select a job title for which you want recommendations
selected_job_title = job_titles[5]  # SAP FICO Architect
print("Selected Job Title:", selected_job_title)

# Only provide the salary filter
recommended_jobs = get_recommendations(selected_job_title, salary="10,000")
print("Recommended Jobs with Salary Filter:")
print(recommended_jobs)

# Provide both salary and education filters
recommended_jobs = get_recommendations(selected_job_title, salary="10,000", education="Graduate")
print("Recommended Jobs with Salary and Education Filters:")
print(recommended_jobs)

# No filters provided
recommended_jobs = get_recommendations(selected_job_title)
print("Recommended Jobs without Filters:")
print(recommended_jobs)
