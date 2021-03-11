import pandas as pd

data = pd.read_csv('./occupation_data.csv')

growing_job = data.groupby('occupation_name')["Job Outlook, 2019-29"].max()
growing_job.head()