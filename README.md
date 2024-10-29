# Information Summarizer

Information Summarizer is a versatile tool built using Django, React, and Tailwind CSS. It allows users to generate summaries from various sources like plain text, PDFs, DOCX files, video transcripts, and website URLs, using advanced NLP model - Trained T5-base, which trained on abisee/cnn_dailymail , 3.0.0. dataset of hugging face.

## Table of Contents
- [Description](#description)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contribution Guidelines](#contribution-guidelines)
- [License](#license)

## Description
Information Summarizer is designed to streamline the summarization process for various content types, leveraging AI models to produce concise, meaningful summaries. Users can upload text files, PDFs, DOCX documents, and input URLs or video links to generate summaries.

## Features
- Summarize various content types:
  - Plain text
  - PDF files
  - DOCX files
  - Video transcripts from YouTube
  - Web URLs
- User authentication (login and signup)
- PDF and text file upload and summary generation
- Video transcription and summarization using the `youtube-transcript-api`
- Summarization models like T5-small and DistilBERT

## Technologies Used
- **Frontend**: React, Tailwind CSS
- **Backend**: Django, Django REST Framework
- **Database**: SQLite
- **OCR and Summarization**: PyTesseract, T5-small, DistilBERT
- **Other Libraries**: `youtube-transcript-api` for video transcription

## Requirements
- Python 3.12
- Django (version compatible with your Python version)
- React and Node.js
- Required Python libraries (see `requirements.txt`)

## Installation
1. **Clone the Repository**
   ```bash
   git clone https://github.com/patilprathamesh07/Information_Summarizer.git
   cd Information_Summarizer
    ```
2. Install Python Dependencies
  ```bash
  pip install -r requirements.txt
  ```

## All set to start the program :
```bash
cd Information_Summarizer
```
```bash
python manage.py migrate
python manage.py runserver
```
## Usage
1.  Login and Signup: Access authentication features at the login page.
2.  Upload Content: Go to the upload page to submit text, PDF, DOCX, or video links.
3.  Summary Generation: Choose the content type and receive a summarized version on the result page.
## Project Structure
```
Information_Summarizer/
├── info_summarizer/
│   ├── settings.py
│   ├── urls.py
│   ├── views.py
│   └── templates/
│       ├── login.html
│       ├── upload.html
│       └── result.html
├── frontend/
│   ├── src/
│   ├── App.js
│   └── index.js
├── README.md
└── requirements.txt
```
## Contribution Guidelines
1.  Fork the repository.
2.  Create a feature branch (git checkout -b feature/AmazingFeature).
3.  Commit your changes (git commit -m 'Add some AmazingFeature').
4.  Push to the branch (git push origin feature/AmazingFeature).
5.  Open a pull request.
## License
This project is licensed under the MIT License.
