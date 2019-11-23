FROM python:3.6.5

# set work directory
WORKDIR /usr/src/app


COPY . .
# install dependencies
RUN pip install --upgrade pip

RUN pip install -r requirements.txt
