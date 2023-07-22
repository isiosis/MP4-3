README

docker build . -q | ForEach-Object { $imageID = $_.split(':')[1].Trim();
>> $dirName = Split-Path -Leaf (Get-Location).Path;
>> docker tag $imageID quantred/$($dirName):latest;
>> docker push quantred/$($dirName):latest;        
>> Set-Location -Path manifests;
>> kubectl delete -f ./;        
>> kubectl apply -f ./ ;
>> Set-Location -Path .. ;}

kubectl create secret generic gmail-address --from-literal=GMAIL_ADDRESS=<email>
kubectl create secret generic gmail-password --from-literal=GMAIL_PASSWORD=<password>