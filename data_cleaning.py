'''
Created on 10/6/2020

tutorial: https://www.youtube.com/watch?v=fhi4dOhmW-g
'''

import pandas as pd
df = pd.read_csv('glassdoor_jobs.csv')

# remove data where salary estimate = -1
df = df[df['Salary Estimate'] != '-1']
df['hourly'] = df['Salary Estimate'].apply(lambda x: 1 if 'per hour' in x.lower() else 0)
df['employer_provided'] = df['Salary Estimate'].apply(lambda x: 1 if 'employer provided salary' in x.lower() else 0)

# clean salary estimate
salary = df['Salary Estimate'].apply(lambda x: x.split('(')[0])
clean_salary = salary.apply(lambda x: x.replace('$', '').replace('K', ''))
cleaner_salary = clean_salary.apply(lambda x: x.lower().replace('per hour', '').replace('employer provided salary:', ''))
df['min_salary'] = cleaner_salary.apply(lambda x: int(x.split('-')[0]))
df['max_salary'] = cleaner_salary.apply(lambda x: int(x.split('-')[1]))
df['avg_salary'] = (df.min_salary + df.max_salary)/2

# Company name
df['name'] = df['Company Name'].apply(lambda x: x.split('\n')[0])

# Create state column
df['state'] = df['Location'].apply(lambda x: x.split(',')[1])

# Age of company (founded)
df['age'] = df['Founded'].apply(lambda x: 2020-x if x != -1 else x)

# job description analysis
df['python_jd'] = df['Job Description'].apply(lambda x: 1 if 'python' in x.lower() else 0)
df['spark_jd'] = df['Job Description'].apply(lambda x: 1 if 'spark' in x.lower() else 0)
df['aws_jd'] = df['Job Description'].apply(lambda x: 1 if 'aws' in x.lower() else 0)
df['excel_jd'] = df['Job Description'].apply(lambda x: 1 if 'excel' in x.lower() else 0)
df['tensor_jd'] = df['Job Description'].apply(lambda x: 1 if 'tensorflow' in x.lower() or 'tensor' in x.lower() else 0)
df['ruby_jd'] = df['Job Description'].apply(lambda x: 1 if 'ruby' in x.lower() else 0)
df['js_jd'] = df['Job Description'].apply(lambda x: 1 if 'javascript' in x.lower() or 'java script' in x.lower() else 0)

df.to_csv('glassdoor_cleaned.csv', index=False)