import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from flask import Flask, request, render_template
import re

# Load the dataset
df = pd.read_csv('dataset.csv')

df['text_corpus'] = df[['degree', 'education_segment', 'job_titles', 
                        'projects_segment', 'skills', 
                        'skills_segment', 'text', 'university_0', 'university_1','work_experience']].fillna('').astype(str).agg(' '.join, axis=1)

def rank_resumes(job_description, resumes, top_n=5):
    documents = [job_description] + resumes
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(documents)
    cosine_similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    
    top_n_indices = cosine_similarities.argsort()[-top_n:][::-1]
    return top_n_indices, cosine_similarities[top_n_indices]


app = Flask(__name__)

class AdvancedCandidateRanker:
    def __init__(self):
        self.text_vectorizer = TfidfVectorizer(
            stop_words='english', 
            max_features=5000, 
            ngram_range=(1, 2)
        )

    def preprocess_text(self, text):
        if not isinstance(text, str):
            return ""
        text = text.lower()
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        text = ' '.join(text.split())
        return text

    def calculate_text_similarity(self, job_description, candidate_texts):
        processed_jd = self.preprocess_text(job_description)
        processed_texts = [self.preprocess_text(text) for text in candidate_texts]
        all_texts = [processed_jd] + processed_texts
        tfidf_matrix = self.text_vectorizer.fit_transform(all_texts)
        text_similarity_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])[0]
        return text_similarity_scores

    def normalize_degree(self, degree):
        """Normalize degree to a standardized category."""
        if not isinstance(degree, str):  # Check if degree is not a string
            degree = str(degree) if degree is not None else ""  # Convert to string if possible, otherwise set as empty string
        degree = degree.lower()
        degree = re.sub(r'[^a-zA-Z\s]', '', degree)
        degree_mappings = {
            'computer science': ['cs', 'computer science', 'computer engineering'],
            'data science': ['data science', 'statistics', 'applied mathematics'],
            'engineering': ['engineering', 'software engineering', 'computer engineering'],
            'information technology': ['it', 'information technology', 'computer applications']
        }
        for key, variants in degree_mappings.items():
            if any(variant in degree for variant in variants):
                return key
        return degree

    def match_degree(self, job_description_degree, candidate_degrees):
        normalized_jd_degree = self.normalize_degree(job_description_degree)
        normalized_candidate_degrees = [self.normalize_degree(degree) for degree in candidate_degrees]
        degree_match_scores = [
            1.0 if nd == normalized_jd_degree else 0.5 if normalized_jd_degree in nd else 0.0 
            for nd in normalized_candidate_degrees
        ]
        return np.array(degree_match_scores)

    def match_work_experience(self, job_description_years, candidate_experiences):
        def parse_experience(exp):
            if not isinstance(exp, str):
                return 0
            match = re.search(r'(\d+)', exp)
            return int(match.group(1)) if match else 0

        parsed_experiences = [parse_experience(exp) for exp in candidate_experiences]
        experience_match_scores = [
            1.0 if exp >= job_description_years else 0.5 if exp > 0 else 0.0 
            for exp in parsed_experiences
        ]
        return np.array(experience_match_scores)

    def rank_candidates(self, candidates_df, job_description):
        jd_text = job_description.get('text', '')
        jd_degree = job_description.get('degree', '')
        jd_experience_years = job_description.get('experience_years', 0)
        
        text_similarity_scores = self.calculate_text_similarity(jd_text, candidates_df['text'])
        degree_match_scores = self.match_degree(jd_degree, candidates_df['degree'])
        experience_match_scores = self.match_work_experience(jd_experience_years, candidates_df['work_experience'])
        
        final_scores = (
            0.4 * text_similarity_scores + 
            0.3 * degree_match_scores + 
            0.3 * experience_match_scores
        )
        
        ranking_df = pd.DataFrame({
            'name': candidates_df['name'],
            'text_similarity': text_similarity_scores,
            'degree_match': degree_match_scores,
            'experience_match': experience_match_scores,
            'final_score': final_scores
        })
        
        return ranking_df.sort_values('final_score', ascending=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/rank', methods=['POST'])
def rank():
    job_description = request.form['job_description']
    degree = request.form['degree']
    experience = int(request.form['experience'])
    
    job_description_dict = {
        'text': job_description,
        'degree': degree,
        'experience_years': experience
    }
    
    candidates_df = pd.read_csv('dataset.csv')
    
    ranker = AdvancedCandidateRanker()
    candidate_rankings = ranker.rank_candidates(candidates_df, job_description_dict)
    
    return render_template(
        'results.html', 
        tables=[candidate_rankings.to_html(classes='data')], 
        titles=candidate_rankings.columns.values
    )

if __name__ == '__main__':
    app.run(debug=True)
