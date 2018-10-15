docker build -t gcr.io/${PROJECT_ID}/qlik-app:v3 .
sleep 5
gcloud docker -- push gcr.io/${PROJECT_ID}/qlik-app:v3
sleep 5
kubectl set image deployment/flask-web flask-web=gcr.io/${PROJECT_ID}/qlik-app:v3
