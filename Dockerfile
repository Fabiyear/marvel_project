FROM python:3

WORKDIR ./src

COPY . .
ADD . .
RUN pip install -r ./requirements.txt

CMD sh -c sleep 45s ; python3 ./src/main.py