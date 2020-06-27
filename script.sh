docker build -t flask_app -f Dockerfile .
docker tag flask_app:latest rogermonteiro/flask_app
docker push rogermonteiro/flask_app
