from typing import List
from job import Job

class QualityChecker:
    """
    Check if the job description of each job object has proper JD text
    """

    def __init__(self, jobs: List[Job]):
        self.jobs = jobs

    def check_jd_quality(self) -> List[Job]:
        """
        Check if job.text (job description) is at low quality which implies an improper web scrape or poor content.
        If determined as poor content, the Job objects (with low_quality=True) should pass to the auto-browsing class later on.
        """

        # Missing job related keywords
        keywords = [
            "responsibilities", "responsibility", "requirements", "requirement",
            "experience","qualifications", "qualification","skills",
            "what you'll do", "what you will do", "about the role", "role overview",
            "the role", "nice-to-have", "nice to have", "preferred",
            "must have", "what we’re looking for", "what we are looking for",
            "about you", "who you are", "responsibilities","duties", "apply",
            "job description", "description", "benefits"
        ]

        counter = 0
        for job in self.jobs:

            text = job.text or ""
            words = text.split()
            low_quality = False

            match_count = sum(1 for k in keywords if k in text.lower())

            if len(words) < 150 and match_count < 2:
                low_quality = True

            job.low_quality = low_quality

            if job.low_quality:
                counter += 1

        print(f"LOW QUALITY URLs: {counter} out of {len(self.jobs)} URLs")

        return self.jobs