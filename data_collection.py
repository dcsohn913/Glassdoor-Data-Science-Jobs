'''
Created on 10/3/2020

tutorial: https://www.youtube.com/watch?v=GmW4F6MHqqs
'''

import scraper as sc

path = 'C:/Users/User/PycharmProjects/GlassdoorDataScienceJobs/chromedriver'

df = sc.get_jobs('data scientist', 1000, False, path, 15)

df.to_csv('glassdoor_jobs.csv', index=False)