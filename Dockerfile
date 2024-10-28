FROM python:3.12.7-slim

WORKDIR /usr/src/app

COPY ./requirements.txt ./
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

COPY ./helpers ./helpers
COPY ./jobs ./jobs
COPY ./main.py ./

EXPOSE 8765

CMD [ "python", "./main.py" ]