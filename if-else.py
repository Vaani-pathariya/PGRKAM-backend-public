import pandas as pd

# Read the CSV file
df1 = pd.read_csv('Job.csv', error_bad_lines=False, engine='python')

# Get the jobtitle from the 6th row (assuming 0-based indexing)
job_title = df1['jobtitle'][5]

# Iterate through the DataFrame and print jobid and jobdescription for matching job titles
for index, row in df1.iterrows():
    if row['jobtitle'] == job_title:
        print(job_title)
        print(f"Job ID: {row['jobid']}")
        print(f"Job Description: {row['jobdescription']}")
        print("\n")
