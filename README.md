# Voxel_Net
Just to check the Docker

# Steps to implement:

1. Create docker image
```
docker build -f Dockerfile -t voxel_model:train .
```

2. Training model
```
docker run -it --gpus 1 voxel_model:train <script/model_train.py>
```

3. Inference the model
```
docker run -it --gpus 1 voxel_model:train <script/inference.py>
```
