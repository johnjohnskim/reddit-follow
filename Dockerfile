FROM python:3.9-alpine

WORKDIR /opt/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src/reddit_follow reddit_follow
COPY settings.ini posts.ini ./

ENV SETTINGS_PATH /opt/app/settings.ini
ENV POSTS_PATH /opt/app/posts.ini

CMD ["python", "-m", "reddit_follow"]
