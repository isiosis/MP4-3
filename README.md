# MP4 -> MP3 Over Microservices
This repo contains that code for an MP4 -> MP3 conversion through a microservice architecture. 

It contains a Gateway, an Authentication service, a Converter Service and a Notification Service (through email).

The services are written in Python. All services include the associted infra code for docker and kuberneter manifests.

It uses MySQL for user logins and MongoDB for storing MP4 and MP3 data. 

It is uses RabbitMQ as a message queue. 


### Installation and Running
The following are required: 
* Minikube (For running a local kubernetes cluster)
* Kubectl for cluster management
* Python 3
* Docker engine (alternatively hyperx enabled machine)

To setup the sending email, the following two kubectl secrets must be created

```
kubectl create secret generic gmail-address --from-literal=GMAIL_ADDRESS=<email>
kubectl create secret generic gmail-password --from-literal=GMAIL_PASSWORD=<password>   
```


##### The following scripts might prove to be somewhat useful when fixing issues to quickly rebuild docker images and redeploy them in minikube

```
docker build . -q | ForEach-Object { $imageID = $_.split(':')[1].Trim();
>> $dirName = Split-Path -Leaf (Get-Location).Path;
>> docker tag $imageID quantred/$($dirName):latest;
>> docker push <DockerHub username>/$($dirName):latest;        
>> Set-Location -Path manifests;
>> kubectl delete -f ./;        
>> kubectl apply -f ./ ;
>> Set-Location -Path .. ;}
```
