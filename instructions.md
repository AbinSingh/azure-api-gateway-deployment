###################################################
################### API Gateway ###################
###################################################

# In enterprises, an API Gateway becomes much more than “just routing.”
# It becomes the central traffic control layer for all APIs.
    Think of it as:
    Security + Routing + Observability + Governance
    for microservices

# Path-Based Routing

    Example:
    /users   → user-service
    /orders  → order-service
    /payments → payment-service

# Host-Based Routing

    Example:
    api.company.com      → API
    admin.company.com    → Admin
    partner.company.com  → Partner APIs

# First Important Concept

    The gateway usually does NOT directly know every pod.

    Instead:

        Gateway routes to a Kubernetes Service

    Example:

        fastapi-service

    Then the service distributes traffic to pods.

##############################################
############## to install helm ###############
##############################################

scoop install helm

# Install NGINX Ingress Controller (AKS)

# Step 1: Add Helm repo:

helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx # Register this repository locally

helm repo update # This downloads latest chart metadata/index.

# Install Ingress Controller
helm install ingress-nginx ingress-nginx/ingress-nginx --namespace ingress-nginx --create-namespace # application name/repo name/chart name


# Important Clarification

    Helm is NOT installing software directly onto nodes.

    Helm is basically:
    
        YAML package manager for Kubernetes
    
    It submits Kubernetes manifests to:
    
        kube-apiserver
    
    just like: kubectl apply would do.

            helm install
                  ↓
            Helm downloads ingress-nginx chart
                  ↓
            Chart contains YAML manifests
                  ↓
            Helm submits manifests to kube-apiserver
                  ↓
            etcd stores resources
                  ↓
            Deployment controller creates pods
                  ↓
            Scheduler places pods on worker nodes


# High-Level Answer --
    
      Helm installs into AKS because:
    
      Helm uses the same kubeconfig/context that kubectl uses.
    
      So Helm talks to: the Kubernetes API server of your AKS cluster.
    
# Step 1: "Here is a catalog/repository of Helm charts" --
    
      Tool	Similar Concept
      ---     ---------------
    
      apt	    apt repository
      pip	    PyPI
      npm	    npm registry
      helm	chart repository
    
# What Is a Helm Chart?
    
      A Helm chart is basically: Parameterized Kubernetes YAML templates
    
      Example chart contains:
    
          - Deployment YAML
          - Service YAML
          - ConfigMaps
          - RBAC
          - templates
          - values
          - for ingress-nginx.

################################################################
################# HOST RULE ####################################
################################################################
# Host Rule
    The host rule is one of the most important Layer-7 (HTTP) routing concepts.
    
    host: fastapi-demo.local means: 
    "Apply these routing rules ONLY when HTTP Host header matches fastapi-demo.local"

    This is NOT: DNS itself, IP address, Kubernetes node name

    It is specifically: HTTP Host header matching.


# Example Browser Request --

    When you open:
    
    http://fastapi-demo.local/users  , browser sends HTTP request:

        GET /users HTTP/1.1
        Host: fastapi-demo.local

    Notice:
    Host: fastapi-demo.local
    
    This header is what ingress checks.

    
# Why HTTP Needs Host Header --
 
    Many websites share same public IP.
    
    Example:
    
    Google Cloud VM IP may host:
    - api.company.com
    - admin.company.com
    - shop.company.com
    
    all on same: IP, port 80
    
    How does server know which website user wants?
        - Using: Host header

    So Host-Based Routing Means
    Same IP + Same Port, BUT different domains route to different applications.


This Is Pure L7 Routing

Because: only HTTP-aware software understands Host header.

# Important Distinction
    DNS maps:

    fastapi-demo.local
    →
    20.235.144.146

# Important Networking Insight

IP Address

    Decides: which machine/load balancer.

Port

    Decides: which process/socket.

Host Header

    Decides: which website/application.

Path

    Decides: which API/backend route.

### To edit host file ###
Option 1 — BEST FOR YOU NOW (Hosts File)

    Map:

    fastapi-demo.local → 20.235.144.146

    locally on your machine.

    Then browser works naturally.

# Windows to edit Hosts File

# Open Notepad as Administrator.

    Edit:
    
        C:\Windows\System32\drivers\etc\hosts
    
    Add:
    
        20.235.144.146 fastapi-demo.local
    
    Save file.


# Can you explain me the meaning of COPY ./app ./app in the dockerfile?
    WORKDIR /app - set current working directory inside container to: /app

    order-service/
    ├── app/
    │   └── main.py
    ├── Dockerfile
    └── requirements.txt

    -- Dockerfile contains: --
    
        COPY ./app ./app
        COPY <source> <destination>

    -- First Important Concept --
    
    Docker build has TWO worlds:
    
    World	                Meaning
    -----                   -------
    Host filesystem	        Your laptop/project files
    Container filesystem	Files inside Docker image
    
    COPY moves files:
        from host into container image

    docker build -t order-service:v1 .

    This dot means: Build context = current directory

    -- Common Beginner Confusion --

    People think:
    
    COPY path is relative to Dockerfile, Not exactly.
    
    It is relative to: build context.

    -- Final Container Filesystem --
    
    Inside container:
    
    /app
    ├── requirements.txt
    └── app/
        └── main.py

# Below worked (Port forwarding):

In CMD or Powershell:

    kubectl port-forward -n ingress-nginx svc/ingress-nginx-controller 9090:80

In Powershell:

    curl.exe -H "Host: fastapi-demo.local" ` http://localhost:9090/users
    {"service":"user-service","pod":"user-deployment-78c499b56-rrxgv","users":["Alice","Bob"]}
