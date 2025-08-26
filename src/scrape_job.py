import asyncio
import time

from selenium import webdriver

from utils import get_job_details, save_to_csv, search_jobs


def scrape_jobs(driver: webdriver.Chrome, keyword: str):
    """Scrape jobs offers and add them to the CSV file."""
    job_links = search_jobs(driver, keyword)

    for job_url in job_links:
        time.sleep(10)
        job_data = asyncio.run(get_job_details(driver, job_url))

        print("JOB OFFER : ", job_data.model_dump())

        break
        save_to_csv(job_data, f"jobs_{keyword}.csv")
