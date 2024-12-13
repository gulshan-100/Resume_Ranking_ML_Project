# Resume Ranking ML Project

## Project Overview
The Resume Ranking ML Project is a web application that ranks job candidates based on their resumes in relation to a given job description. It utilizes machine learning techniques, specifically TF-IDF vectorization and cosine similarity, to evaluate the relevance of candidates' qualifications and experiences against the job requirements.

## Interface Screenshots
![Screenshot (253)](https://github.com/user-attachments/assets/f3689fbb-3ace-404c-801a-d23604095353)

![Screenshot (254)](https://github.com/user-attachments/assets/88b74058-1bc6-4386-816b-3632058608e7)

## Installation Instructions
To set up the project locally, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/gulshan-100/Resume_Ranking_ML_Project
   cd Resume_Ranking_ML_Project
   ```

2. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Prepare the dataset**:
   Ensure you have a `dataset.csv` file in the project root directory containing the candidate information.

5. **Run the application**:
   ```bash
   python app.py
   ```

6. **Access the application**:
   Open your web browser and go to `http://127.0.0.1:5000/`.

## Usage
1. **Input the Job Description**: Enter the job description in the provided text area.
2. **Specify the Degree**: Input the required degree for the job.
3. **Enter Experience**: Provide the number of years of experience required.
4. **Submit the Form**: Click on the "Rank Resumes" button to see the ranked candidates.

## Features
- **Resume Ranking**: Ranks candidates based on text similarity, degree match, and work experience.
- **User-Friendly Interface**: Simple and intuitive web interface for inputting job requirements.
- **Data Visualization**: Displays ranked candidates in a tabular format.

## API Documentation
### Endpoints
- **GET /**: Renders the main input form.
- **POST /rank**: Accepts job description, degree, and experience, and returns ranked candidates.

### Classes
- **AdvancedCandidateRanker**: Contains methods for processing text, calculating similarity, and ranking candidates.

## Dependencies
- Flask
- Pandas
- Scikit-learn
- NumPy

## Acknowledgments
- [Flask](https://flask.palletsprojects.com/) for the web framework.
- [Scikit-learn](https://scikit-learn.org/) for machine learning functionalities.
- [Pandas](https://pandas.pydata.org/) for data manipulation.
