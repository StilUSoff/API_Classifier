FROM python:3.11

RUN apt-get update && apt-get install -y libgl1-mesa-glx unzip p7zip-full

RUN wget https://www.rarlab.com/rar/unrarsrc-6.2.3.tar.gz && \
    tar -xzvf unrarsrc-6.2.3.tar.gz && \
    cd unrar && \
    make && \
    make install && \
    cd .. && \
    rm -r unrar unrarsrc-6.2.3.tar.gz

COPY requirements.txt .
RUN pip3 install -r requirements.txt

WORKDIR /app

COPY app /app

CMD ["python3", "api.py"]