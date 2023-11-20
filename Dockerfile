

FROM python:3.10
COPY requirements.txt .
RUN pip install -r requirements.txt

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

RUN mkdir /RAHAB-VOTING-SYSTEM
WORKDIR /RAHAB-VOTING-SYSTEM
COPY . /RAHAB-VOTING-SYSTEM/

# Install any needed packages specified in requirements.txt
# RUN pip install -r requirements.txt