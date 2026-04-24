from typing import List
from urllib.parse import urlparse
import random
from job import Job
import time


def no_adjacent_same_domains(jobs: List[Job], max_attempts=50) -> List[Job]:
    """
    Shuffle jobs to avoid jobs with adjacent domains straight to each other which can cause a throttling with bursty requests to domains (for web-scraping)
    :param jobs: a list of jobs
    :param max_attempts: maximum limit of domain shuffling
    :return: a list of Job objects with root domains in a shuffled order
    """
    def get_root_domain(url):
        return urlparse(url).netloc

    for _ in range(max_attempts):
        random.shuffle(jobs)
        valid = True

        for i in range(len(jobs) - 1):
            if get_root_domain(jobs[i].url) == get_root_domain(jobs[i + 1].url):
                valid = False
                break

        if valid:
            return jobs

    return jobs

def apply_delay(index, job, prev_job_domain):
    """
    Delay between domain requests based on the conditions
    :param index: refer to each iteration of Job objects
    :param job: refer to each Job object
    :param prev_job_domain: The previous domain requested to for scraping
    :return: prev_job_domain
    """

    ### For extra web-scraping safety!

    # Domain-Aware Delay
    current_domain = urlparse(job.url).netloc

    if current_domain == prev_job_domain:
        print("Domain-Aware sleep...")
        time.sleep(random.uniform(9, 15.7))
    else:
        # Small random delay (always)
        time.sleep(random.uniform(2.5, 4))


    # Batch pause (longer delay) every 15 jobs
    if (index + 1) % 15 == 0:
        print("Batch sleep...")
        time.sleep(random.uniform(5, 9))

    prev_job_domain = current_domain

    return prev_job_domain



def get_root_domain(url):
    return urlparse(url).netloc