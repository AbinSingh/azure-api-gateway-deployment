###################
# to install helm #
###################

scoop install helm

# Install NGINX Ingress Controller (AKS)

# Add Helm repo:

helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx

helm repo update

# Install Ingress Controller
helm install ingress-nginx ingress-nginx/ingress-nginx --namespace ingress-nginx --create-namespace


Option 1 — BEST FOR YOU NOW (Hosts File)

    Map:

    fastapi-demo.local → 20.235.144.146

    locally on your machine.

    Then browser works naturally.

# Windows Hosts File

# Open Notepad as Administrator.

    Edit:
    
        C:\Windows\System32\drivers\etc\hosts
    
    Add:
    
        20.235.144.146 fastapi-demo.local
    
    Save file.


Below worked (Port forwarding):

In CMD or Powershell:

    kubectl port-forward -n ingress-nginx svc/ingress-nginx-controller 9090:80

In Powershell:

    curl.exe -H "Host: fastapi-demo.local" ` http://localhost:9090/users
    {"service":"user-service","pod":"user-deployment-78c499b56-rrxgv","users":["Alice","Bob"]}
