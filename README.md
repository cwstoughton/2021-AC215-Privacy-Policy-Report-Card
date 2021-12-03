AC215-Privacy Policy Report Card
==============================

AC215 Fall 2021



Project Description
------------

The goal of this project is to build an application that will allow users to enter
the URL of a privacy policy, and receive a "report card" explaining which categories
of user data the application collects and shares.

Project Demo
------------

This tutorial will allow you to create a Kubernetes cluster on GCP with an API backend and a React frontend. You can see a [demo here](http://34.134.205.218.sslip.io/). 

Design Overview
------------

When a user submits a privacy policy to be graded, the app needs to take a number of steps to evaluate it
1. The front end accepts the user's input
    - The React front end takes the url as input, and passes it to an API running as a separate microservice
2. The API receives the URL request and passes it to the backend inference engine
3. The inference engine incorporates elements of the training data pipeline to fetch and parse the text of the privacy policy
4. The inference engine passes the encoded privacy policy to the model for inference
   - Our model is designed to detect the presence of language that indicates the collection of certain user data.
     It does this for each paragraph of the policy. Because a given paragraph may contain any combination of trackers,
     we have created a custom ensemble model to detect each tracker type as a binary response variable. 
4. The model completes its inferences and passes the result as a dictionary back to the API
5. The API returns model inferences as a JSON to the frontend.
6. The front end renders the model's output for the user to review


Project Organization and Key Components
------------

- Data : Stores raw training data

- Pipeline: Stores files for processing raw data into training sets                                             
    - Create_Unlabeled_Dataset.py -> scrapes the web for fine-tuning data                
    - Labeled_Data_Pipeline.py -> parses raw training data from APP350 into dataframe    
    - Training_Data_Pipeline.py -> encodes text data for training                        
- models: contains files for training and generating models  

- Demo: Contains files for the prototype and demo backend                                            
    - demo_app.py -> API to serve model inferences                                          
    - demo_model_builder.py -> functions for inference model building                       
    - demo_inference_backend.py -> builds ensemble model using Demo_Model_Weights           
                                                                                                   
- Demo_frontend:Contains files for the prototype and demo react frontend
    - Todos.jsx -> functions for handling API calls                        
    - App.js -> structure of the app
      
--------

      .
      ├── LICENSE
      ├── Makefile
      ├── README.md
      ├── models
      ├── notebooks
      │   ├── Fine Tuning Experiments
      ├── Pipeline
      │   ├── Labeled_Data_Pipeline.py #Creates training data from APP350 Dataset
      │   ├── Create_Unlabeled_Dataset.py #Creates fine-tuning data via web-scraping
      │   ├── Training_Data_Piepline.py #Encodes text data for training
      ├── Demo # conains files for the backend prototype and demo to run locally
      │   ├── 
      ├── Demo_Frontend #conains files for the frontend prototype and demo to run locally
      │   ├── Fine Tuning Experiments
      ├── notebooks
      │   ├── Fine Tuning Experiments
      ├── references
      ├── requirements.txt
      ├── setup.py
      ├── src
      │   ├── __init__.py
      │   └── build_features.py
      ├── submissions
      │   ├── milestone1_groupname
      │   ├── milestone2_groupname
      ├── api-service # conains files for the backend prototype and demo to run in GCP GKE
      ├── frontend-react #conains files for the frontend prototype and demo to run GCP GKE
      ├── deployment #conains files for configuring deployment to GCP GKE
      └── test_project.py
      

# Privacy App - Deployment to GCP

## API's to enable in GCP before you begin
Search for each of these in the GCP search bar and click enable to enable these API's
* Compute Engine API
* Service Usage API
* Cloud Resource Manager API
* Google Container Registry API

## Create a service account for deployment

- Go to [GCP Console](https://console.cloud.google.com/home/dashboard), search for  "Service accounts" from the top search box. or go to: "IAM & Admins" > "Service accounts" from the top-left menu and create a new service account called "deployment"
- Give the following roles:
- For `deployment`:
    - Compute Admin
    - Compute OS Login
    - Container Registry Service Agent
    - Kubernetes Engine Admin
    - Service Account User
    - Storage Admin
- Then click done.
- This will create a service account
- On the right "Actions" column click the vertical ... and select "Create key". A prompt for Create private key for "deployment" will appear select "JSON" and click create. This will download a Private key json file to your computer. Copy this json file into the **secrets** folder.
- Rename the json key file to `deployment.json`
- Follow the same process Create another service account called `gcp-service`
- For `gcp-service` give the following roles:
    - Storage Object Viewer
- Then click done.
- This will create a service account
- On the right "Actions" column click the vertical ... and select "Create key". A prompt for Create private key for "gcp-service" will appear select "JSON" and click create. This will download a Private key json file to your computer. Copy this json file into the **secrets** folder.
- Rename the json key file to `gcp-service.json`

## Setup Docker Container (Ansible, Docker, Kubernetes)

Rather than each of installing different tools for deployment we will use Docker to build and run a standard container will all required software.

### Download the folder `deployment`
- Clone this repository
- cd into `deployment`
- Go into `docker-shell.sh` or `docker-shell.bat` and change `GCP_PROJECT` to your project id
- Run `sh docker-shell.sh` or `docker-shell.bat` for windows

- Check versions of tools:
```
gcloud --version
ansible --version
kubectl version --client
```

- Check to make sure you are authenticated to GCP
- Run `gcloud auth list`

Now you have a Docker container that connects to your GCP and call create VMs, deploy containers all from the command line

## SSH Setup
### Configuring OS Login for service account
```
gcloud compute project-info add-metadata --project <YOUR GCP_PROJECT> --metadata enable-oslogin=TRUE
```

### Create SSH key for service account
```
cd /secrets
ssh-keygen -f ssh-key-deployment
cd /app
```

### Providing public SSH keys to instances
```
gcloud compute os-login ssh-keys add --key-file=/secrets/ssh-key-deployment.pub
```
From the output of the above command keep note of the username. Here is a snippet of the output 
```
- accountId: ac215-project
    gid: '3906553998'
    homeDirectory: /home/sa_100110341521630214262
    name: users/deployment@ac215-project.iam.gserviceaccount.com/projects/ac215-project
    operatingSystemType: LINUX
    primary: true
    uid: '3906553998'
    username: sa_100110341521630214262
```
The username is `sa_100110341521630214262`


## Deployment Setup
* Add ansible user details in inventory.yml file
* GCP project details in inventory.yml file
* GCP Compute instance details in inventory.yml file

## Deployment

### Build and Push Docker Containers to GCR (Google Container Registry)
```
ansible-playbook deploy-docker-images.yml -i inventory.yml
```

# Deploy the Privacy App to K8s Cluster
------------

## API's to enable in GCP for Project
Search for each of these in the GCP search bar and click enable to enable these API's
* Compute Engine API
* Service Usage API
* Cloud Resource Manager API
* Google Container Registry API
* Kubernetes Engine API

## Start Deployment Docker Container
**This step is only required if you have NOT already done this**
-  `cd deployment`
- Run `sh docker-shell.sh` or `docker-shell.bat` for windows
- Check versions of tools
`gcloud --version`
`kubectl version`
`kubectl version --client`

- Check if make sure you are authenticated to GCP
- Run `gcloud auth list`


# Deploy to Kubernetes Cluster
We will use ansible to create and deploy the Privacy app into a Kubernetes Cluster

### Create a Deployment Yaml file (Ansible Playbook)
* Add a file called `deploy-k8s-cluster.yml` inside the deployment folder
* Add the following script:

```
---
- name: "Create Kubernetes Cluster and deploy multiple containers"
  hosts: localhost
  gather_facts: false

  vars:
    cluster_name: "privacy-app-cluster"
    machine_type: "n1-standard-1"
    machine_disk_size: 30
    initial_node_count: 2

  tasks:
  - name: "Create a GKE cluster"
    google.cloud.gcp_container_cluster:
      name: "{{cluster_name}}"
      initial_node_count: "{{ initial_node_count }}"
      location: "{{ gcp_zone }}"
      project: "{{ gcp_project }}"
      release_channel:
        channel: "UNSPECIFIED"
      ip_allocation_policy:
        use_ip_aliases: "yes"
      auth_kind: "{{ gcp_auth_kind }}"
      service_account_file: "{{ gcp_service_account_file }}"
      state: "{{ cluster_state }}"
    register: cluster
  
  - name: "Create a Node Pool"
    google.cloud.gcp_container_node_pool:
      name: default-pool
      initial_node_count: "{{ initial_node_count }}"
      cluster: "{{ cluster }}"
      location: "{{ gcp_zone }}"
      project: "{{ gcp_project }}"
      config:
        machine_type: "{{ machine_type }}"
        image_type: "COS"
        disk_size_gb: "{{ machine_disk_size }}"
        oauth_scopes:
          - "https://www.googleapis.com/auth/devstorage.read_only"
          - "https://www.googleapis.com/auth/logging.write"
          - "https://www.googleapis.com/auth/monitoring"
          - "https://www.googleapis.com/auth/servicecontrol"
          - "https://www.googleapis.com/auth/service.management.readonly"
          - "https://www.googleapis.com/auth/trace.append"
      autoscaling:
        enabled: "yes"
        min_node_count: "1"
        max_node_count: "{{ initial_node_count }}"
      management:
        auto_repair: "yes"
        auto_upgrade: "yes"
      auth_kind: "{{ gcp_auth_kind }}"
      service_account_file: "{{ gcp_service_account_file }}"
      state: "{{ cluster_state }}"
  
  - name: "Connect to cluster (update kubeconfig)"
    shell: "gcloud container clusters get-credentials {{ cluster.name }} --zone {{ gcp_zone }} --project {{ gcp_project }}"
    when: cluster_state == "present"

  - name: "Create Namespace"
    k8s:
      name: "{{cluster_name}}-namespace"
      api_version: v1
      kind: Namespace
      state: present
    when: cluster_state == "present"

  - name: "Add nginx-ingress helm repo"
    community.kubernetes.helm_repository:
      name: nginx-stable
      repo_url: https://helm.nginx.com/stable
    when: cluster_state == "present"

  - name: "Install nginx-ingress"
    community.kubernetes.helm:
      name: nginx-ingress
      namespace: "{{cluster_name}}-namespace"
      chart_ref: nginx-stable/nginx-ingress
      state: present
    when: cluster_state == "present"

  - name: "Copy docker tag file"
    copy:
      src: .docker-tag
      dest: .docker-tag
      mode: 0644
    when: cluster_state == "present"

  - name: "Get docker tag"
    shell: "cat .docker-tag"
    register: tag
    when: cluster_state == "present"

  - name: "Print tag"
    debug:
      var: tag
    when: cluster_state == "present"

  - name: "Create Persistent Volume Claim"
    k8s:
      state: present
      definition:
        apiVersion: v1
        kind: PersistentVolumeClaim
        metadata:
          name: persistent-pvc
          namespace: "{{cluster_name}}-namespace"
        spec:
          accessModes:
            - ReadWriteOnce
          resources:
            requests:
              storage: 5Gi
    when: cluster_state == "present"
  
  - name: Importing credentials as a Secret
    shell: |
      #!/bin/bash
      kubectl create secret generic bucket-reader-key --from-file=bucket-reader.json=../secrets/bucket-reader.json --namespace="{{cluster_name}}-namespace"
    register: create_secret_op
    ignore_errors: yes
    when: cluster_state == "present"
  
  - name: "Print Create Secret Output"
    debug:
      var: create_secret_op
    when: cluster_state == "present"
  
  - name: "Create Deployment for Frontend"
    k8s:
      state: present
      definition:
        apiVersion: v1
        kind: Deployment
        metadata:
          name: frontend
          namespace: "{{cluster_name}}-namespace"
        spec:
          selector:
            matchLabels:
              run: frontend
          template:
            metadata:
              labels:
                run: frontend
            spec:
              containers:
              - image: "gcr.io/{{ gcp_project }}/privacy-app-frontend-react:{{ tag.stdout}}"
                imagePullPolicy: IfNotPresent
                name: frontend
                ports:
                - containerPort: 80
                  protocol: TCP
    when: cluster_state == "present"

  - name: "Create Deployment for API Service"
    k8s:
      state: present
      definition:
        apiVersion: v1
        kind: Deployment
        metadata:
          name: api
          namespace: "{{cluster_name}}-namespace"
        spec:
          selector:
            matchLabels:
              run: api
          template:
            metadata:
              labels:
                run: api
            spec:
              volumes:
                - name: persistent-vol
                  emptyDir: {}
                  # persistentVolumeClaim:
                  #   claimName: persistent-pvc
                - name: google-cloud-key
                  secret:
                    secretName: bucket-reader-key
              containers:
              - image: gcr.io/{{ gcp_project }}/privacy-app-api-service:{{ tag.stdout}}
                imagePullPolicy: IfNotPresent
                name: api
                ports:
                - containerPort: 9000
                  protocol: TCP
                volumeMounts:
                  - name: persistent-vol
                    mountPath: /persistent
                    #readOnly: false
                  - name: google-cloud-key
                    mountPath: /secrets
                env:
                  - name: GOOGLE_APPLICATION_CREDENTIALS
                    value: /secrets/bucket-reader.json
                  - name: GCP_PROJECT
                    value: ac215-project
                  - name: GCP_ZONE
                    value: us-central1-a
    when: cluster_state == "present"

  - name: "Create Service for Frontend"
    k8s:
      state: present
      definition:
        apiVersion: v1
        kind: Service
        metadata:
          name: frontend
          namespace: "{{cluster_name}}-namespace"
        spec:
          ports:
          - port: 80
            protocol: TCP
            targetPort: 80
          selector:
            run: frontend
          type: NodePort
    when: cluster_state == "present"

  - name: "Create Service for API Service"
    k8s:
      state: present
      definition:
        apiVersion: v1
        kind: Service
        metadata:
          name: api
          namespace: "{{cluster_name}}-namespace"
        spec:
          ports:
          - port: 9000
            protocol: TCP
            targetPort: 9000
          selector:
            run: api
          type: NodePort
    when: cluster_state == "present"

  - name: Wait for Ingress Nginx to get ready
    shell: |
      #!/bin/bash
      kubectl get service nginx-ingress-nginx-ingress --namespace="{{cluster_name}}-namespace" -ojson | jq -r '.status.loadBalancer.ingress[].ip'
    register: nginx_ingress
    delay: 10
    retries: 20
    until: nginx_ingress.stderr == ""
    when: cluster_state == "present"

  - name: Set Nginx Ingress IP
    set_fact:
      nginx_ingress_ip: "{{nginx_ingress.stdout}}"
    when: cluster_state == "present"

  - name: Debug Ingress Nginx IP Address
    debug:
      msg: "Ingress Nginx IP Address: {{ nginx_ingress_ip }}"
    when: cluster_state == "present"

  - name: Debug vars
    debug:
      var: nginx_ingress_ip
      verbosity: 0
    when: cluster_state == "present"

  - name: "Create Ingress Controller"
    k8s:
      state: present
      definition:
        apiVersion: networking.k8s.io/v1
        kind: Ingress
        metadata:
          name: ingress-resource
          namespace: "{{cluster_name}}-namespace"
          annotations:
            kubernetes.io/ingress.class: "nginx"
            nginx.ingress.kubernetes.io/ssl-redirect: "false"
            nginx.org/rewrites: "serviceName=frontend rewrite=/;serviceName=api rewrite=/"
        spec:
          rules:
          - host: "{{ nginx_ingress_ip }}.sslip.io" # Host requires a domain and not just an IP
            http:
              paths:
              - path: /
                pathType: Prefix
                backend:
                  service:
                    name: frontend
                    port:
                      number: 80
              - path: /api/
                pathType: Prefix
                backend:
                  service:
                    name: api
                    port:
                      number: 9000
    when: cluster_state == "present"
```

### Create & Deploy Cluster
```
ansible-playbook deploy-k8s-cluster.yml -i inventory.yml --extra-vars cluster_state=present
```

### Try some kubectl commands
```
kubectl get all
kubectl get all --all-namespaces
kubectl get pods --all-namespaces
```

```
kubectl get componentstatuses
kubectl get nodes
```

### If you want to shell into a container in a Pod
```
kubectl get pods --namespace=privacy-app-cluster-namespace
kubectl get pod api-5d4878c545-47754 --namespace=privacy-app-cluster-namespace
kubectl exec --stdin --tty api-5d4878c545-47754 --namespace=privacy-app-cluster-namespace  -- /bin/bash
```

### View the App
* Copy the `nginx_ingress_ip` from the terminal from the create cluster command
* Go to `http://<YOUR INGRESS IP>.sslip.io`
      
<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>

