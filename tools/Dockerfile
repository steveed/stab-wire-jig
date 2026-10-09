# CadQuery for the jig model: STEP, DXF and SVG exports.
FROM python:3.11-slim
RUN apt-get update && apt-get install -y --no-install-recommends libgl1 libglib2.0-0 libxrender1 fontconfig fonts-dejavu-core libcairo2 \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir cadquery==2.4.0 numpy==1.26.4 cairosvg==2.7.1
