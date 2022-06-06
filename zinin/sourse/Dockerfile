FROM python:3.8
RUN mkdir /sourse
WORKDIR /sourse
#COPY ../requirements.txt .
COPY ./requirements.txt /requirements.txt
#EXPOSE 8080
RUN ["pip3", "install", "-r", "/requirements.txt"]
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install wkhtmltopdf -y
RUN apt-get install libreoffice-java-common -y
RUN apt-get install libreoffice-common -y
RUN apt-get install libreoffice-writer -y
RUN ["pip3", "install", "pdfkit"]
RUN ["pip3", "install", "PyPDF2"]
RUN ["pip3", "install", "flask-cors"]
RUN ["pip3", "install", "pymongo"]
ENV PYTHONUNBUFFERED=0
ENV AWS_ACCESS_KEY_ID="AKIASB4X5LU7PTFBB7SD"
ENV AWS_SECRET_ACCESS_KEY="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"
CMD gunicorn app:run --bind 0.0.0.0:8000 --worker-class aiohttp.GunicornWebWorker
#ADD .. /sourse/
COPY . /sourse