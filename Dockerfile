FROM python:3

COPY kbqa-saas-flask .

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN python3 -m nltk.downloader stopwords

ENTRYPOINT [ "python" ]

CMD ["simplifi.py"]
