FROM nvidia/cuda:9.0-base-ubuntu16.04
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
    apt-get install -y python3.7 python3-pip
RUN python3.7 -m pip install --upgrade pip
RUN python3.7 -m pip install Flask && python3.7 -m pip install torch
WORKDIR /app
COPY main.py /app
EXPOSE 80

CMD [ "python3.7", "main.py"]
