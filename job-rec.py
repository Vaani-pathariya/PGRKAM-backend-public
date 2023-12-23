import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
df1=pd.read_csv('dice_com-job_us_sample.csv',error_bad_lines=False, engine='python')
df1.info()
df1=df1.dropna()
df1.dropna()
from sklearn.feature_extraction.text import TfidfVectorizer
tfid=TfidfVectorizer(stop_words='english')
df1['jobdescription']=df1['jobdescription'].fillna('')
tfid_matrix=tfid.fit_transform(df1['jobdescription'])
tfid_matrix.shape
from sklearn.metrics.pairwise import sigmoid_kernel

cosine_sim=sigmoid_kernel(tfid_matrix,tfid_matrix)
indices=pd.Series(df1.index, index=df1['jobtitle']).drop_duplicates()
def get_recommendation(title,cosine_sim=cosine_sim):
    idx=indices[title]
    sim_scores=list(enumerate(cosine_sim[idx]))
    sim_scores=sorted(sim_scores,key=lambda X: X[1], reverse=True)
    sim_scores=sim_scores[1:16]
    tech_indices=[i[0] for i in sim_scores]
    return df1['jobtitle'].iloc[tech_indices]
new1= df1[['jobtitle','jobdescription']]
df1.tail()
new1.to_csv('new.csv')
pickle.dump(new1,open('job_list.pkl','wb'))
pickle.dump(cosine_sim,open('similarity.pkl','wb'))