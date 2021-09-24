FROM python:3.9.7

WORKDIR /usr/src/app

RUN python3 -m venv venv
ENV PATH venv/bin:$PATH

COPY . .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

CMD ["gunicorn", "--config", "gunicorn.py", "wsgi:app"]

