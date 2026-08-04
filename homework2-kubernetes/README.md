# CSE644 Homework 2 – Local Kubernetes Deployment

## Student Information

**Name:** Rod Raemon Alvero

**Course:** CSE644 Advanced Cloud Computing

**Assignment:** Homework 2 – Local Kubernetes

---

# Local Kubernetes Environment

This project was completed using the following environment:

- Windows 11
- Docker Desktop
- Docker Desktop Kubernetes (Kind Cluster)
- Kubernetes v1.34.3
- kubectl
- Helm v4.2.3
- Traefik Ingress Controller

---

# GitHub Repository

https://github.com/rodraemonalvero/CSE644-Docker-Assignment

---

# Project Overview

The objective of this assignment is to deploy multiple containerized applications into a local Kubernetes cluster and demonstrate Kubernetes networking, service discovery, reverse proxying, persistent storage, application configuration, and Ingress routing.

The project includes:

- Custom Nginx web application
- Python Flask web application
- HAProxy reverse proxy
- Kubernetes Deployments
- Kubernetes Services
- PersistentVolumeClaim (PVC)
- ConfigMap
- Kubernetes Secret
- Readiness and Liveness Probes
- Traefik Ingress Controller

---

# Architecture Summary

The project consists of three primary workloads deployed inside the **cse644** namespace.

The Custom Nginx application serves a customized HTML webpage.

The Python Flask application provides a web service on port **8888**, health endpoints, external configuration through ConfigMaps, protected configuration through Kubernetes Secrets, and persistent storage using a PersistentVolumeClaim.

HAProxy acts as an independent reverse proxy that forwards requests to the Custom Nginx application using Kubernetes internal DNS service discovery rather than individual Pod IP addresses.

Traffic exposure is demonstrated through:

- ClusterIP
- NodePort
- LoadBalancer
- Traefik Ingress

---

# Local Image Loading Instructions

Docker Desktop Kubernetes shares the local Docker image store with the Kubernetes cluster, allowing locally built images to be deployed directly without pushing them to Docker Hub.

Build the images:

```bash
docker build -t rodraemonalvero/cse644-custom-nginx:1.0 ./custom-nginx

docker build -t rodraemonalvero/cse644-python-web:2.0 ./python-web
```

Verify images:

```bash
docker images
```

Deploy Kubernetes resources:

```bash
kubectl apply -f homework2-kubernetes/
```

---

# Kubernetes Resources Created

## Namespace

- cse644

## Deployments

- Custom Nginx Deployment
- Python Web Deployment
- HAProxy Deployment

## Services

- ClusterIP
- NodePort
- LoadBalancer

## Storage

- PersistentVolumeClaim (PVC)

## Configuration

- HAProxy ConfigMap
- Python ConfigMap
- Python Secret

## Networking

- Traefik Ingress Controller
- Kubernetes Ingress Resource

---

# Project Deployment Steps

1. Enable Kubernetes in Docker Desktop.

2. Verify the cluster.

```bash
kubectl get nodes
```

3. Create the namespace.

```bash
kubectl create namespace cse644
```

4. Build Docker images.

```bash
docker build -t rodraemonalvero/cse644-custom-nginx:1.0 ./custom-nginx

docker build -t rodraemonalvero/cse644-python-web:2.0 ./python-web
```

5. Deploy Kubernetes resources.

```bash
kubectl apply -f homework2-kubernetes/
```

6. Verify deployments.

```bash
kubectl get all -n cse644
```

---

# Features Demonstrated

This project successfully demonstrates:

- Kubernetes cluster creation
- Namespace creation
- Public image deployment
- Local Docker image deployment
- Pod inspection
- Interactive container shell
- Kubernetes service discovery
- ClusterIP networking
- NodePort networking
- LoadBalancer networking
- Traefik Ingress routing
- HAProxy reverse proxy
- PersistentVolumeClaim storage
- Persistent data after Pod replacement
- ConfigMap configuration management
- Kubernetes Secret usage
- Readiness and Liveness probes

---

# Persistent Storage

Persistent storage was implemented using a Kubernetes PersistentVolumeClaim (PVC).

The Python application mounts the persistent volume at:

```
/data
```

To verify persistence:

1. A file was written into the running container.
2. The Python Pod was deleted.
3. Kubernetes automatically recreated the Pod.
4. The same file remained available in the new Pod.

This demonstrates that application data is stored on persistent Kubernetes storage rather than inside the container filesystem.

---

# Configuration and Secret Management

Application configuration is separated from the container image.

The Python application receives public configuration from a Kubernetes ConfigMap.

ConfigMap values include:

- PUBLIC_MESSAGE
- APP_ENVIRONMENT

Updating the ConfigMap changes the webpage without rebuilding the Docker image.

A Kubernetes Opaque Secret supplies:

- APP_PROTECTED_VALUE

The application confirms that the Secret was successfully received by displaying:

```
Protected application value received: true
```

The actual Secret value is never displayed in screenshots, browser output, terminal output, logs, or source control.

The repository includes:

```
python-secret.example.yaml
```

while the real

```
python-secret.yaml
```

is ignored using `.gitignore`.

---

# Kubernetes Secret Security

Kubernetes Secrets are **not encrypted by default** in the Kubernetes API server data store.

A production Kubernetes cluster should enable:

- Encryption at rest
- Least-privilege Role-Based Access Control (RBAC)

These protections reduce the risk of unauthorized access to sensitive application configuration.

---

# Health Checks

The Python application implements both readiness and liveness probes.

### Readiness Probe

Endpoint:

```
/health/ready
```

Purpose:

Determines when the application is ready to receive traffic.

### Liveness Probe

Endpoint:

```
/health/live
```

Purpose:

Detects unhealthy containers and automatically restarts them if necessary.

Kubernetes successfully detected and configured both probes during deployment.

---

# Validation Steps

The deployment can be validated using:

```bash
kubectl get all -n cse644

kubectl get services -n cse644

kubectl get ingress -n cse644

kubectl get pvc -n cse644

kubectl get configmap -n cse644
```

Browser and curl tests successfully verified:

- ClusterIP
- NodePort
- LoadBalancer
- Ingress
- HAProxy reverse proxy

---

# Cleanup

To remove the deployment:

```bash
kubectl delete namespace cse644

helm uninstall traefik -n traefik
```

---

# Evidence Summary

| Evidence | Description |
|-----------|-------------|
| Evidence1 | Kubernetes Cluster Running |
| Evidence2 | Public Image Deployment |
| Evidence3 | Public Image Inspection |
| Evidence3A | Public Image Pod Inspection |
| Evidence4 | Public Image Logs |
| Evidence5 | Interactive Shell |
| Evidence6 | Namespace Created |
| Evidence7 | Custom Nginx Deployment |
| Evidence8 | ClusterIP Service Created |
| Evidence9 | Service Endpoints |
| Evidence10 | Nginx Internal Service Discovery |
| Evidence11 | Python Deployment |
| Evidence12 | Python ClusterIP Service |
| Evidence13 | Python Internal Service Discovery |
| Evidence14 | HAProxy ConfigMap |
| Evidence15 | HAProxy Deployment |
| Evidence16 | HAProxy Service |
| Evidence17 | HAProxy Proxied Request |
| Evidence18 | NodePort Service |
| Evidence19 | NodePort Access Test |
| Evidence19A | NodePort Browser Test |
| Evidence20 | LoadBalancer Service |
| Evidence21 | LoadBalancer Curl Test |
| Evidence21A | LoadBalancer Browser Test |
| Evidence22 | Ingress Created |
| Evidence23 | Ingress Description |
| Evidence24 | Ingress Browser Test |
| Evidence24A | Ingress Curl Test |
| Evidence25 | PersistentVolumeClaim Bound |
| Evidence26 | Persistent Data Written |
| Evidence27 | Persistent Data After Pod Replacement |
| Evidence28 | Python ConfigMap |
| Evidence29 | Python Secret |
| Evidence30 | Python Deployment Updated |
| Evidence31 | ConfigMap Application Behavior |
| Evidence32 | Health Probes Configured |
| Evidence32A | Health Probe Events |
| Evidence33 | ConfigMap Updated Message |

---

# Challenges Encountered

Several challenges were encountered during the implementation of this project.

The first challenge involved understanding Kubernetes networking in a local Docker Desktop environment. Unlike managed cloud Kubernetes clusters, local LoadBalancer and NodePort services required additional testing to determine the correct access method.

Another challenge occurred while configuring the Traefik Ingress Controller. Helm was initially unavailable on the system, preventing Traefik from being installed. After installing Helm and adding the Traefik chart repository, the Ingress Controller deployed successfully.

Testing Ingress and LoadBalancer services required Kubernetes port forwarding because Docker Desktop networking differs from managed cloud environments.

Additional troubleshooting was required while configuring PersistentVolumeClaims, ConfigMaps, Kubernetes Secrets, and application health probes. These steps improved understanding of Kubernetes storage, configuration management, and workload health monitoring.

---

# Reflection

This assignment provided valuable hands-on experience deploying multiple containerized applications into Kubernetes.

I learned how Deployments, Pods, Services, PersistentVolumeClaims, ConfigMaps, Secrets, and Ingress resources work together to build reliable containerized applications. Implementing HAProxy, Traefik, persistent storage, and Kubernetes health probes strengthened my understanding of application networking, configuration management, and high availability.

Troubleshooting local Kubernetes networking also improved my confidence in diagnosing deployment issues and understanding how Kubernetes differs from running standalone Docker containers.

Overall, this assignment strengthened my practical Kubernetes skills and gave me greater confidence deploying and managing applications in a container orchestration environment.

---

# Conclusion

This project successfully demonstrated deploying multiple containerized applications into a local Kubernetes cluster using Docker Desktop Kubernetes.

The Custom Nginx application, Python Flask application, and HAProxy reverse proxy were successfully deployed using Kubernetes Deployments. Internal communication was verified through Kubernetes service discovery, while external access was demonstrated using ClusterIP, NodePort, LoadBalancer, and Traefik Ingress.

Persistent storage was successfully verified after Pod replacement using a PersistentVolumeClaim. Configuration management was implemented using ConfigMaps and Kubernetes Secrets, while readiness and liveness probes improved application reliability.

Overall, this assignment provided practical experience with Kubernetes deployments, networking, persistent storage, configuration management, workload health monitoring, and local container orchestration.