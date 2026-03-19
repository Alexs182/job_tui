import re

import requests
from bs4 import BeautifulSoup

class RequestHandler():
    def __init__(self):
        self.url = "https://www.linkedin.com/jobs/search/?keywords=DataEngineer&&location=United%20Kingdom"

        self.data = list

    def run(self) -> list:
        self.get_job_data()
        jobs = self.parse_job_data()

        return jobs


    def get_job_data(self):
        print(f"Requesting Data from: {self.url}")
        response = requests.get(self.url)

        if response.status_code == 200:
            self.data = response.content
        else:
            print(f"Error: {response.status_code}: {response.text}")
            self.data = None


    def parse_job_data(self) -> list:
        if self.data is None:
            print("No data to parse.")
            return []
        
        soup = BeautifulSoup(self.data, "html.parser")
        base_card = soup.find_all('div', attrs={'class': re.compile('^base-card *')})

        jobs = []
        for items in base_card:
            raw_data ={
                "job_link": items.find("a", attrs={"class": re.compile("^base-card__full-link *")}),
                "title": items.find("h3", attrs={"class": "base-search-card__title"}),
                "company": items.find("h4", attrs={"class": "base-search-card__subtitle"}),
                "location": items.find("span", attrs={"class", "job-search-card__location"}),
                "list_date": items.find("time", attrs={"class", "job-search-card__listdate"})
            }

            jobs.append({
                "job_link": raw_data['job_link']['href'].strip() if raw_data['job_link'] else None,
                "job_title": raw_data['title'].text.strip() if raw_data['title'] else None,
                "company": raw_data['company'].text.strip() if raw_data['company'] else None,
                "location": raw_data['location'].text.strip() if raw_data['location'] else None,
                "list_date": raw_data['list_date']['datetime'].strip() if raw_data['list_date'] else None,
            })

        print(f"Found: {len(jobs)} jobs.")
        
        return jobs
