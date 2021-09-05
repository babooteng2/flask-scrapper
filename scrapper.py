import requests
from bs4 import BeautifulSoup

SO_URL = "https://stackoverflow.com"
HEADERS = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
}

def extract_job(html):
    title = html.find("h2", {"class": "mb4"}).find("a")["title"]
    company, location = html.find("h3", {"class": "fc-black-700"}).find_all("span", recursive=False)
    company = company.text.strip()
    location = location.text.strip().strip("/r").strip("/n")
    job_id = html["data-jobid"]
    return {
      "title": title,
      "company": company,
      "location": location,
      "link": f"{SO_URL}/jobs/{job_id}"}


def extract_jobs(last_page, url):
  jobs = []
  
  last_page = int(int(last_page) / 10) + 1
  
  for page in range(last_page):
    print(f"scrapping ----- {page + 1} / {last_page}")
    r = requests.get(f"{url}&pg={page}")
    soup = BeautifulSoup(r.text, "html.parser")
    results = soup.find_all("div", {"class": "-job"})
    for result in results:
        job = extract_job(result)
        jobs.append(job)

  return jobs


def get_last_page(url):    
    r = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, "html.parser")
    pages = soup.find("div", {"class": "s-pagination"}).find_all("a")
    last_page = pages[-2].text.strip()
    return last_page


def get_jobs(word):    
    url = f"{SO_URL}/jobs?q={word}"
    last_page = get_last_page(url)
    jobs = extract_jobs(last_page, url)
    return jobs
