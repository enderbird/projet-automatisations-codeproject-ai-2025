FROM python:3.12-slim
LABEL borne="vision"

RUN apt-get update && apt-get install -y \
    fonts-dejavu-core wget ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    pygame==2.5.2 \
    onnxruntime==1.18.1 \
    Pillow==10.4.0 \
    numpy==1.26.4

WORKDIR /borne

# Modèle ONNX
RUN wget -q -O /borne/mobilenetv2-12.onnx \
    https://github.com/onnx/models/raw/main/validated/vision/classification/mobilenet/model/mobilenetv2-12.onnx

# Labels ImageNet
RUN wget -q -O /borne/imagenet-labels.txt \
    https://raw.githubusercontent.com/onnx/models/main/validated/vision/classification/synset.txt

COPY application/ /borne/

# Génération des images de test
RUN python generer-photos-test.py

CMD ["python", "vision.py"]