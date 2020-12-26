FROM python:3

WORKDIR ./hcloud-tg

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "./bot.py" ]
