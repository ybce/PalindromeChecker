# Palindrome Checker


Hello!
This is a simple REST API using Flask+Python deployed in a kubernetes cluster! This is my second time using Flask and Kubernetes.

This file should show how the API was roughly created and eventually deployed. 

This checker will check alphanumeric strings under 100 characters only.

## Schema
For the backend database, I used SQLite3 to store and retrieve the data. Again, I opted for something more lightweight for this challenge for the quick prototyping benefit.  I have 1 table in my schema and it was created as follows: 

### Messages:
```
CREATE TABLE "messages" ( 
`message_id` INTEGER PRIMARY KEY AUTOINCREMENT, 
`message` TEXT NOT NULL, 
`palindrome` INTEGER DEFAULT -1 
);
```

## Endpoints:
There is a total of 4 endpoints for this API:


### GET `/`
This endpoint serves the main homepage of the application.

### POST  `/check/`
Checks if the given message is a palindrome. Example of a request json.

```
{
    "message_id": 1
}

```

If the request is successful the call will the message_id along with a palindrome boolean `{“status”: “Your new shop has been added”}`

### POST  `/add/`
Adds a message to the table. It accepts a JSON in the body of the request. An example of a valid request body:
```
{
    "message": "HelloWorld"
}
```

If the request is successful the call will return `{“status”: “Your message has been added”}` .

### DELETE `/delete/`
Deletes a message from the list. It accepts a JSON in the body of the request. An example of a valid request body: 

```
{
 "message_id": 

}
```

# Deploying To Kubernetes

The app was containerized using Docker and deployed to a Kubernetes cluster on GKE. It is currently exposed on 
the IP Address [http://35.185.97.219:31788](http://35.185.97.219:31788). This was my second time using Kubernetes
it was pretty challenging to understand all the networking involved the first time around but I managed to research and get the image
deployed and expose it to the internet. I was mainly following [this](https://cloud.google.com/kubernetes-engine/docs/tutorials/hello-app) 
tutorial for guidance. 

### Creating and Pushing a docker image

First of all, I created a Dockerfile that dictates how the image will be built:

```
FROM ubuntu:16.04

MAINTAINER Youssef El Khalili "elkhalili.youssef@outlook.com"

#Install python and pip
RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

#Swtich working directories
WORKDIR /app

#Install requirements from requirements.txt
RUN pip install -r requirements.txt

#Copy contents of the directory into a new app direcroty on the VM
COPY . /app

#Choosing which port to be exposed in the container
EXPOSE 5000

# What commands to run
CMD ["python", "run.py"]

```

I then ran:
``` 
docker build -t gcr.io/${PROJECT_ID}/qlik-app:v1 .
```
to build the the docker container where PROJECT_ID is the ID for google cloud project.
After the image has been created I had to push it to the container registry using:
```
docker push gcr.io/${PROJECT_ID}/flask-app:v1
```
I then verified that my app can run locally using this command:

```
docker run --rm -p 8080:5000 gcr.io/${PROJECT_ID}/qlik-app:v1
```

which allows me to run `curl http://localhost:8080` and check the respose. The `-p`
flag was very important becuase it allows you to expose the port on which the application
is running and forward it to your preferred port on the host machine.

### Creating a cluster on GCE

Now I had to create a container cluster so I can run the container image that
I tested in the previouse test. This was done using a simple `gcloud` command:

```commandline
gcloud container clusters create hello-cluster --num-nodes=3
```
We can then run this command to check that the VMs have been instantiated 

```commandline
gcloud compute instances list
```

which returns: 

```
NAME                                          ZONE        MACHINE_TYPE   PREEMPTIBLE  INTERNAL_IP  EXTERNAL_IP     STATUS
gke-flask-cluster-default-pool-c414426b-1cnf  us-east1-b  n1-standard-1               10.142.0.4   x.x.x.x         RUNNING
gke-flask-cluster-default-pool-c414426b-m541  us-east1-b  n1-standard-1               10.142.0.2   x.x.x.x         RUNNING
gke-flask-cluster-default-pool-c414426b-t5jp  us-east1-b  n1-standard-1               10.142.0.3   x.x.x.x         RUNNING
```

### Deploying and exposing the application to the internet

To deploy and manage applications on a GKE cluster, 
I had to do this by using the `kubectl` command-line tool. To create a deployment, I had to run this command:
```
kubectl run flask-web --labels="run=flask-web" --image=gcr.io/${PROJECT_ID}/qlik-app:v1 --port=5000
```
again the port option is crucial to make sure the pod was exposing port 5000 which the application is running on.

The next and final step was to expose the deployment to the internet:

```
kubectl expose deployment flask-web --type=NodePort --name=flask-app
```

The `type` flag is important becuase it dictates what type of application will be deployed the other option was to use
`LoadBlancer` but I decided that `NodePort` would be more suitable for a demo application. I read this 
[article](https://medium.com/google-cloud/kubernetes-nodeport-vs-loadbalancer-vs-ingress-when-should-i-use-what-922f010849e0)
to understand the differences, pros and cons and finally decided to use `NodePort`

### GCE Config

Since the service is running in a GCE cluster, the last step was to allow a TCP connection
to the port where the app is exposed on in the deployment which happens to be 31788 in my case.
I got this value by running `kubectl describe services flask-app` which returns

```
Name:                     flask-app
Namespace:                default
Labels:                   run=flask-web
Annotations:              <none>
Selector:                 run=flask-web
Type:                     NodePort
IP:                       x.x.x.x
Port:                     <unset>  5000/TCP
TargetPort:               5000/TCP
NodePort:                 <unset>  31788/TCP
Endpoints:                x.x.x.x
Session Affinity:         None
External Traffic Policy:  Cluster
Events:                   <none>
```

and using the `NodePort` value. This can be achieved by adding a firewall rule in the google cloud
console. 

After all this setup, I was able to query application by using any external ip address of one the VMs
in the cluster with the port `http://35.185.97.219:31788` and got a successful response.

## Usage

It is recommended to use [Postman](https://www.getpostman.com/) to test this API for its ease of use. 
Alternatively, one can use [curl](https://curl.haxx.se/) or any other preferred method.

The app is available on this IP address: `http://35.185.97.219:31788`

### Note
This API was created for demo purposes only and is not representative of a development grade deployment. The API 
could use more features such as API token headers for authorization and a test suite.






