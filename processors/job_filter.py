from typing import List
from job import Job


class JobFilter:
    """
    Internal logic to filter out job data before passing it to the LLM job evaluator
    """
    EXCLUDING_SITES = ["linkedin.com", "indeed.com", "ziprecruiter.com", "glassdoor.com"]
    EXCLUDING_WORDS = ["senior", "head", "lead", "principal", "director", "manager"]

    def __init__(self, jobs):
        self.jobs = jobs


    def filter_jobs(self) -> List[Job]:
        """
        Filter out data that should be excluded in order to reduce the workload of LLM Evaluator (Save costs and improve latency)
        """

        filtered_jobs = []

        seen_urls = set()

        for job in self.jobs:

            # Skip duplicate URLs
            if job.url in seen_urls:
                continue
            seen_urls.add(job.url)

            # First filter out URLs that point to these general job platforms that unlikely offer global/worldwide remote roles
            if not any(domain in job.url.lower() for domain in self.EXCLUDING_SITES):

                # Additionally, filter out data that contains these words on its title
                if not any(word in job.title.lower() for word in self.EXCLUDING_WORDS):
                    filtered_jobs.append(job)

        return filtered_jobs