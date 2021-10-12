FROM nvidia/cuda:9.0-base-ubuntu16.04
EXPOSE 80
ENV LC_ALL=C.UTF-8
RUN apt-get update \
     && apt-get install -y \
        libgl1-mesa-glx \
        libx11-xcb1 \
        libglib2.0-0 \
        libsm6 \
        libxrender1 \
        libxext6 \
        software-properties-common

RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update && \
    apt-get install -y python3.7 python3-pip && apt-get clean all && rm -r /var/lib/apt/lists/*
WORKDIR /app
COPY . /app/
# RUN python3.7 -m pip install -r requirements.txt
RUN python3.7 -m pip install --upgrade pip
RUN python3.7 -m pip install numpy==1.18.5 scikit-image==0.18.3 matplotlib==3.4.3 Pillow==7.2.0 opencv-python==4.5.3.56 Flask torch==1.7.0

CMD [ "python3.7", "main.py"]