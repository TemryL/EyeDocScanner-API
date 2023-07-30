FROM python:3.11.2

# set the working directory
WORKDIR /app

# install dependencies
COPY ./requirements.txt /app
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# copy the scripts to the folder
COPY . /app

# start the server

# for production
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9999","--root-path","/scanner"]

# for local testing
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--root-path","/scanner"]