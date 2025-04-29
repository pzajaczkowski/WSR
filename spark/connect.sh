#!/bin/bash
docker run -it --rm -v "$(pwd)/data:/data" apache/spark-py:latest /opt/spark/bin/pyspark