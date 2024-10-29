# Information Summarizer

Information Summarizer is a versatile tool built using Django, React, and Tailwind CSS. It allows users to generate summaries from various sources like plain text, PDFs, DOCX files, video transcripts, and website URLs, using advanced NLP models such as T5-small and DistilBERT.

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
