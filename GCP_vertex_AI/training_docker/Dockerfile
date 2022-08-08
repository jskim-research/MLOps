FROM python:3.7
COPY . /

RUN python --version &&\
    pip --no-cache-dir install -r requirements.txt

CMD ["python", "bert_naver_movie_rating.py"]

