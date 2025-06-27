FROM pytorch/pytorch:2.7.1-cuda12.8-cudnn9-runtime

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    wget \
    git \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && wget -O /usr/local/bin/gosu "https://github.com/tianon/gosu/releases/download/1.17/gosu-amd64" \
    && chmod +x /usr/local/bin/gosu \
    && apt-get purge -y --auto-remove wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install 'git+https://github.com/facebookresearch/detectron2.git'

WORKDIR /app

COPY src/analyzers/analyzers/layoutparser/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh
ENTRYPOINT ["entrypoint.sh"]

CMD ["/bin/sh"]