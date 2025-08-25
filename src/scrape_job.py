import asyncio
import time

from selenium import webdriver

from utils import get_job_details, save_to_csv, search_jobs


def scrape_jobs(driver: webdriver.Chrome, keyword: str):
    """Traite les jobs et les ajoute au CSV"""
    job_links = search_jobs(driver, keyword)

    for job_url in job_links:
        time.sleep(10)
        job_data = asyncio.run(get_job_details(driver, job_url))
        print("JOB OFFER : ", job_data)
        break
        save_to_csv(job_data, f"jobs_{keyword}.csv")
        print("Title:", job_data[0])
        print("Company:", job_data[1])
        print("Date Posted:", job_data[2])
        print("Applicants:", job_data[3])
        print("Offer Types:", job_data[4])
        print("===============================")
