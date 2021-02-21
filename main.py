from sklearn.feature_extraction.text import TfidfVectorizer
from file_reader import resume_reader, jobdesc_reader
from sklearn.metrics.pairwise import cosine_similarity
import os
import pandas as pd


class FindCandidates:
    def __init__(self):
        # folder that stores the resume of applicants
        self.resumes_folder = "./data/resumes/"

        # folder that stores the job description
        self.jobdesc_file = "./data/jobs/description.txt"

        self.read_jobdesc()
        self.parse_resumes()

    def parse_resumes(self):
        # parse the information from the resume of all candidates
        self.resumes = {}

        for file in os.listdir(self.resumes_folder):
            name, resume_text = resume_reader(self.resumes_folder + file)
            self.resumes[name] = resume_text

    def read_jobdesc(self):
        jobdesc = jobdesc_reader(self.jobdesc_file)
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.jobdesc_vectors = self.vectorizer.fit_transform([jobdesc])

    def rank_candidates(self):
        resume_vectors = self.vectorizer.transform(list(self.resumes.values())).toarray()
        sim = cosine_similarity(self.jobdesc_vectors, resume_vectors)[0]

        df = pd.DataFrame()
        df['name'] = list(self.resumes.keys())
        df['sim'] = sim
        df.columns = ['Candidate', 'Match Score']
        return df

    def search_candidates(self, keyword):
        matched_name = []
        for name, resume in self.resumes.items():
            if keyword in set(resume.split(" ")):
                matched_name.append(name)

        return matched_name


if __name__ == "__main__":
    candidateSearch = FindCandidates()
    print("Ranked List of candidates")
    print(candidateSearch.rank_candidates())
    print()
    print()
    print("Searching candidates with 'PHP' skill")
    print(candidateSearch.search_candidates("php"))
