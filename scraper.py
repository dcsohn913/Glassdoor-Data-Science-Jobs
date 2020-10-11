'''
Created on 10/3/2020

author: Ömer Sakarya
url: https://github.com/arapfaik/scraping-glassdoor-selenium
'''

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium import webdriver
import time
import pandas as pd


def get_jobs(keyword, num_jobs, verbose, path, sleep_time):
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''

    # Initializing the webdriver
    options = webdriver.ChromeOptions()

    # Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    # options.add_argument('headless')

    # Change the path to where chromedriver is in your home folder.
    driver = webdriver.Chrome(executable_path=path, options=options)
    driver.set_window_size(1120, 1000)

    url = 'https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=' + keyword + '&sc.keyword=' + keyword + '&locT=&locId=&jobType='
    driver.get(url)
    jobs = []

    while len(jobs) < num_jobs:  # If true, should be still looking for new jobs.

        # Let the page load. Change this number based on your internet speed.
        # Or, wait until the webpage is loaded, instead of hardcoding it.
        time.sleep(sleep_time)

        # Test for the "Sign Up" prompt and get rid of it.
        try:
            driver.find_element_by_class_name("selected").click()
        except ElementClickInterceptedException:
            pass

        time.sleep(.1)

        try:
            driver.find_element_by_css_selector('[alt="Close"]').click()  # clicking to the X.
        except NoSuchElementException:
            pass

        # Going through each job in this page
        job_buttons = driver.find_elements_by_class_name("jl")  # jl for Job Listing. These are the buttons we're going to click.
        for job_button in job_buttons:
            print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
            if len(jobs) >= num_jobs:
                break

            driver.execute_script("arguments[0].click();", job_button)
            time.sleep(8)

            collected_successfully = False
            while not collected_successfully:
                try:
                    company_name = driver.find_element_by_xpath(
                        '//div[@class="empInfo newDetails"]//div[@class="employerName"]').text
                    location = driver.find_element_by_xpath(
                        '//div[@class="empInfo newDetails"]//div[@class="location"]').text
                    job_title = driver.find_element_by_xpath(
                        '//div[@class="empInfo newDetails"]//div[@class="title"]').text
                    job_description = driver.find_element_by_xpath(
                        './/div[@class="jobDescriptionContent desc"]').text
                    collected_successfully = True
                except:
                    time.sleep(5)

            try:
                salary_estimate = driver.find_element_by_xpath(
                    '//div[@class="salary"]//span[@class="gray salary"]').text
            except NoSuchElementException:
                salary_estimate = -1  # You need to set a "not found value. It's important."

            try:
                rating = driver.find_element_by_xpath('//span[@class="rating"]').text
            except NoSuchElementException:
                rating = -1  # You need to set a "not found value. It's important."

            # Printing for debugging
            if verbose:
                print("Job Title: {}".format(job_title))
                print("Salary Estimate: {}".format(salary_estimate))
                print("Job Description: {}".format(job_description[:500]))
                print("Rating: {}".format(rating))
                print("Company Name: {}".format(company_name))
                print("Location: {}".format(location))

            # Going to the Company tab...
            # clicking on this:
            # <div class="tab" data-tab-type="overview"><span>Company</span></div>
            try:
                driver.find_element_by_xpath(
                    './/div[@class="tab" and @data-test="tab" and @data-tab-type="overview"]').click()
                try:
                    size = driver.find_element_by_xpath(
                        './/div[@class="infoEntity"]//label[text()="Size"]//following-sibling::*').text
                except NoSuchElementException:
                    size = -1
                except StaleElementReferenceException:
                    size = driver.find_element_by_xpath(
                        './/div[@class="infoEntity"]//label[text()="Size"]//following-sibling::*').text

                try:
                    founded = driver.find_element_by_xpath(
                        './/div[@class="infoEntity"]//label[text()="Founded"]//following-sibling::*').text
                except NoSuchElementException:
                    founded = -1
                except StaleElementReferenceException:
                    founded = driver.find_element_by_xpath(
                        './/div[@class="infoEntity"]//label[text()="Founded"]//following-sibling::*').text

                try:
                    type_of_ownership = driver.find_element_by_xpath(
                        './/div[@class="infoEntity"]//label[text()="Type"]//following-sibling::*').text
                except NoSuchElementException:
                    type_of_ownership = -1
                except StaleElementReferenceException:
                    type_of_ownership = driver.find_element_by_xpath(
                        './/div[@class="infoEntity"]//label[text()="Type"]//following-sibling::*').text

                try:
                    industry = driver.find_element_by_xpath(
                        './/div[@class="infoEntity"]//label[text()="Industry"]//following-sibling::*').text
                except NoSuchElementException:
                    industry = -1
                except StaleElementReferenceException:
                    industry = driver.find_element_by_xpath(
                        './/div[@class="infoEntity"]//label[text()="Industry"]//following-sibling::*').text

                try:
                    sector = driver.find_element_by_xpath(
                        './/div[@class="infoEntity"]//label[text()="Sector"]//following-sibling::*').text
                except NoSuchElementException:
                    sector = -1
                except StaleElementReferenceException:
                    sector = driver.find_element_by_xpath(
                        './/div[@class="infoEntity"]//label[text()="Sector"]//following-sibling::*').text

                try:
                    revenue = driver.find_element_by_xpath(
                        './/div[@class="infoEntity"]//label[text()="Revenue"]//following-sibling::*').text
                except NoSuchElementException:
                    revenue = -1
                except StaleElementReferenceException:
                    revenue = driver.find_element_by_xpath(
                        './/div[@class="infoEntity"]//label[text()="Revenue"]//following-sibling::*').text

            except NoSuchElementException: # Rarely, some job postings do not have the "Company" tab.
                size = -1
                founded = -1
                type_of_ownership = -1
                industry = -1
                sector = -1
                revenue = -1

            if verbose:
                print("Size: {}".format(size))
                print("Founded: {}".format(founded))
                print("Type of Ownership: {}".format(type_of_ownership))
                print("Industry: {}".format(industry))
                print("Sector: {}".format(sector))
                print("Revenue: {}".format(revenue))
                print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

            jobs.append({"Job Title": job_title,
                         "Salary Estimate": salary_estimate,
                         "Company Name": company_name,
                         "Job Description": job_description,
                         "Rating": rating,
                         "Location": location,
                         "Size": size,
                         "Founded": founded,
                         "Type of ownership": type_of_ownership,
                         "Industry": industry,
                         "Sector": sector,
                         "Revenue": revenue})

        # Clicking on the "next page" button
        try:
            driver.find_element_by_xpath('.//li[@class="next"]//a').click()
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs,
                                                                                           len(jobs)))
            break

    return pd.DataFrame(jobs)  # This line converts the dictionary object into a pandas DataFrame.
