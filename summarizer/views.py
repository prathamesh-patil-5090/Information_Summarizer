import json
import os
import requests
import pdfplumber
from bs4 import BeautifulSoup
from django.conf import settings
from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from django.contrib.auth import login
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm   
from django.urls import reverse_lazy
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import T5Tokenizer, T5ForConditionalGeneration

# Paths to model and tokenizer
model_path = os.path.join(settings.BASE_DIR, 'summarizer/model/t5_cnn_model')
tokenizer_path = os.path.join(settings.BASE_DIR, 'summarizer/model/t5_cnn_tokenizer')
model = T5ForConditionalGeneration.from_pretrained(model_path)
tokenizer = T5Tokenizer.from_pretrained(tokenizer_path)

def homepage(request):
    return render(request, 'index.html')

def upload_text(request):
    return render(request, 'upload.html')

def summarize_text(request):
    if request.method == 'POST':
        input_text = request.POST['textInput']
        summary = summarize(input_text)
        return render(request, 'result.html', {'summary': summary})
    return render(request, 'upload.html')

def summarize(input_text):
    inputs = tokenizer.encode("summarize: " + input_text, return_tensors="pt", max_length=512, truncation=True)
    input_length = len(inputs[0])
    max_length = int(input_length * 0.5) if input_length > 400 else min(150, int(input_length * 0.8))
    min_length = int(input_length * 0.20) if input_length > 400 else min(50, int(input_length * 0.4))
    
    summary_ids = model.generate(inputs, max_length=max_length, min_length=min_length, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return '. '.join(sentence.capitalize() for sentence in summary.split('. '))

def upload_pdf(request):
    return render(request, 'upload_pdf.html')

def get_pdf(request):
    if request.method == 'POST' and request.FILES.get('pdf_file'):
        pdf_file = request.FILES['pdf_file']
        file_path = default_storage.save('pdfs/' + pdf_file.name, pdf_file)
        full_file_path = os.path.join(settings.MEDIA_ROOT, file_path)
        extracted_text = pdf_extractor(full_file_path)
        summary = summarize(extracted_text)
        request.session['pdf_summary'] = summary
        return redirect('pdf_result')
    return render(request, 'upload_pdf.html')

def pdf_result(request):
    summary = request.session.get('pdf_summary', "No summary available")
    return render(request, 'result-pdf.html', {'summary': summary})

def pdf_extractor(pdf_path):
    main_text = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            raw_text = page.extract_text()
            tables = page.extract_tables()
            if tables:
                for table in tables:
                    for row in table:
                        for cell in row:
                            if cell and cell in raw_text:
                                raw_text = raw_text.replace(cell, '')
            main_text.append(raw_text.strip())
    return '\n'.join(main_text)

def upload_video(request):
    return render(request, 'upload_video.html')

def get_transcript(request):
    if request.method == 'POST':
        video_url_or_id = request.POST['videoId']
        output_directory = os.path.join(settings.MEDIA_ROOT, 'transcripts')
        os.makedirs(output_directory, exist_ok=True)
        output_file = os.path.join(output_directory, "transcript.json")
        extract_transcript(video_url_or_id, output_file)
        if os.path.exists(output_file):
            with open(output_file, 'r') as f:
                transcript_data = json.load(f)
            summary = summarize(transcript_data["transcript"])
            return render(request, 'video_result.html', {'summary': summary})
        else:
            return render(request, 'upload_video.html', {'error': 'Transcript file not created.'})
    return render(request, 'upload_video.html')

def extract_transcript(video_url_or_id, output_file):
    if "youtube.com" in video_url_or_id or "youtu.be" in video_url_or_id:
        video_id = video_url_or_id.split('/')[-1].split('?')[0] if "youtu.be" in video_url_or_id else video_url_or_id.split('v=')[-1].split('&')[0]
    else:
        video_id = video_url_or_id
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        combined_text = " ".join([item["text"] for item in transcript]).replace('\n', ' ').replace('\t', ' ').strip()
        transcript_json = {"transcript": combined_text}
        with open(output_file, 'w') as f:
            json.dump(transcript_json, f, indent=4)
    except Exception as e:
        print(f"Error: {str(e)}")

def upload_url(request):
    return render(request, 'upload_url.html')

def extract_main_content(soup):
    paragraphs = soup.find_all('p')
    return ' '.join(map(str, [p.get_text() for p in paragraphs])) if paragraphs else ' '.join(map(str, soup.stripped_strings))

def summarize_html_content(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    for unwanted in soup(['script', 'style', 'header', 'footer', 'nav', 'aside']):
        unwanted.extract()
    text = extract_main_content(soup)
    input_ids = tokenizer.encode(text, return_tensors='pt', max_length=1024, truncation=True)
    summary_ids = model.generate(input_ids, max_length=int(0.5 * len(text.split())), min_length=min(100, int(0.25 * len(text.split()))), length_penalty=2.0, num_beams=4, early_stopping=True)
    return '. '.join(sentence.capitalize() for sentence in tokenizer.decode(summary_ids[0], skip_special_tokens=True).split('. '))

def summarize_url(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        try:
            response = requests.get(url)
            response.raise_for_status()
            summary = summarize_html_content(response.text)
            return render(request, 'result-web.html', {'summary': summary})
        except requests.exceptions.RequestException as e:
            return render(request, 'upload_url.html', {'error': f"An error occurred: {e}"})
    return render(request, 'upload_url.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Your account has been created successfully!')
            return redirect('homepage')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})
