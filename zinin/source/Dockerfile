FROM pypy:3.7-7.3.5-buster
RUN mkdir /source
WORKDIR /sourse
COPY ./requirements.txt /requirements.txt
RUN apt-get -y update && apt-get install -y libzbar-dev
RUN apt-get install -y libmupdf-dev
RUN chmod -R 777 .
RUN apt-get install libxml2-dev -y
RUN apt-get install libxslt-dev -y
RUN apt-get install python3-dev -y
RUN apt-get install python3-lxml -y
RUN apt-get install g++ -y
RUN apt-get install gcc -y
RUN apt-get install -y zlib1g-dev
RUN apt-get install python3-pip -y
RUN ["pip3", "install", "--upgrade", "pip"]
#RUN ["pip3", "install", "pip==20.2.4"]
RUN apt-get install cython3
#RUN pip3 install lxml
#--use-deprecated=legacy-resolver
RUN apt-get install swig3.0
RUN apt install awscli -y
RUN apt-get install expect -y
COPY aws_configure.sh .
RUN chmod -R 777 .
RUN pip install --use-deprecated=legacy-resolver lxml
RUN ["pip3", "install", "-r", "/requirements.txt"]
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install wkhtmltopdf -y
RUN apt-get install libreoffice-java-common -y
RUN apt-get install libreoffice-common -y
RUN apt-get install libreoffice-writer -y
RUN ["pip3", "install", "pdfkit"]
RUN ["pip3", "install", "PyPDF2"]
ENV PYTHONUNBUFFERED=0
CMD gunicorn app:run --bind 0.0.0.0:8000 --worker-class aiohttp.GunicornWebWorker
