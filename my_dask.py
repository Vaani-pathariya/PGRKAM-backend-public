import dask.dataframe as dd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import sigmoid_kernel
import pickle

# Read the dataset using Dask
df1 = dd.read_csv('Job sample dataset (1).csv', assume_missing=True, blocksize=1e6)

# Drop rows with missing values
df1 = df1.dropna().compute()

df1['salary'] = df1['Salary'].astype(str)
df1['education'] = df1['Education'].astype(str)
df1['experience'] = df1['EXP'].astype(str)

# Combine relevant columns into a new column 'jobinfo'
df1['jobinfo'] = df1['jobdescription'] + ' ' + df1['salary'] + ' ' + df1['education'] + ' ' + df1['experience'] 

# Create TF-IDF matrix
tfid = TfidfVectorizer(stop_words='english')
tfid_matrix = tfid.fit_transform(df1['jobinfo'])

# Calculate sigmoid kernel
cosine_sim = sigmoid_kernel(tfid_matrix, tfid_matrix)

# Create indices series
indices = df1.set_index('jobtitle').index

# Function to get recommendations with filters
def get_recommendation(title, salary, education, experience, cosine_sim=cosine_sim):
    # Get index of the given job title
    idx = indices.get_loc(title)

    # Get the cosine similarity scores
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the jobs based on similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the indices of the top 15 similar jobs
    sim_scores = sim_scores[0:16]
    tech_indices = [i[0] for i in sim_scores]

    # Apply additional filters
    filtered_jobs = df1.iloc[tech_indices]
    filtered_jobs = filtered_jobs[(filtered_jobs['salary'] == salary) & 
                                  (filtered_jobs['education'] == education) & 
                                  (filtered_jobs['experience'] == experience)]

    # Return the recommended job titles
    return filtered_jobs['jobtitle']

# Save the modified DataFrame and cosine similarity matrix
new1 = df1[['jobtitle', 'jobdescription','salary','education','experience']]
new1.to_csv('new2.csv', index=False)
pickle.dump(new1, open('job_list2.pkl', 'wb'))

