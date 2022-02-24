# Simple Flask API with SQLAlchemy

# Docker usage

```
docker build --tag thisimg .
docker push thisimg
docker run --env-file .env -p 8080:8080 thisimg:latest
docker run --entrypoint '' -ti thisimg /bin/bash
```

# Example .env file

```
USERNAME=tester
PASSWORD=tester123
```