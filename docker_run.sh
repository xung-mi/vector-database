# docker run --gpus all -it -d --name vtdbv2 \
#   -v /mnt/d/VectorDatabase:/app \
#   -v /mnt/d/VectorDatabase/db/chroma_persistent:/app/db/chroma_persistent \
#   vtdb:v2 /bin/bash
docker run --gpus all -it -d \
  --name vtdbv1 \
  --env-file /mnt/d/VectorDatabase/.env \
  -e OLLAMA_BASE_URL=http://host.docker.internal:11434 \
  -v /mnt/d/VectorDatabase:/app \
  -v /mnt/d/VectorDatabase/db/chroma_persistent:/app/db/chroma_persistent \
  -p 7860:7860 \
  -p 8000:8000 \
  -p 8501:8501 \
  vtdb:v1 \
  /bin/bash

