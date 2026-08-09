# CSE644 Assignment 03 — GitOps and Application Observability

**Student:** Rod Raemon Alvero  
**Course:** CSE644 — Advanced Cloud Computing & Cloud Management  
**Assignment:** Assignment 03 — GitOps and Application Observability  
**Environment:** Docker Desktop Kubernetes  
**GitOps Tool:** Argo CD  
**Monitoring:** Prometheus and Grafana  
**Application:** Python Web Application  

---

## 1. Overview

This assignment extends the Kubernetes application from Assignment 02 by introducing GitOps-based deployment management and application observability.

The Python web application is deployed to a local Docker Desktop Kubernetes cluster. Argo CD continuously reconciles the Kubernetes resources with the desired state stored in GitHub. Prometheus collects application metrics, and Grafana is used to visualize application activity.

The implementation demonstrates:

- Declarative Kubernetes deployment from Git
- Automated GitOps synchronization
- Git-driven application changes
- Detection and correction of configuration drift
- Controlled deployment failure and recovery
- Prometheus metrics collection
- Grafana application visualization
- Observable workload behavior

---

## 2. Architecture

The application uses the following workflow:

```text
GitHub Repository
       |
       v
    Argo CD
       |
       v
Docker Desktop Kubernetes
       |
       +----------------------+
       |                      |
       v                      v
Python Web Pod          Python Web Service
    :8888                    :8888
       |
       v
   /metrics
       |
       v
ServiceMonitor
       |
       v
  Prometheus
       |
       v
    Grafana
```

GitHub contains the desired Kubernetes configuration. Argo CD monitors the repository and automatically synchronizes the desired state into the Kubernetes cluster.

The Python application exposes Prometheus-compatible metrics through `/metrics`. A ServiceMonitor allows the Prometheus Operator to discover and scrape the application. Grafana uses Prometheus as its data source for visualization.

---

## 3. Repository Structure

```text
homework3-gitops/
|
+-- application/
|   +-- python-configmap.yaml
|   +-- python-deployment.yaml
|   +-- python-secret.yaml
|   +-- python-service.yaml
|
+-- argocd/
|   +-- application.yaml
|
+-- monitoring/
|   +-- python-servicemonitor.yaml
|
+-- screenshots/
|   +-- Screenshot01_GitOps_Deployment_Synced_Healthy.png
|   +-- Screenshot02_Application_Access.png
|   +-- Screenshot03_GitOps_Change_Reconciled.png
|   +-- Screenshot04_Live_Drift_Self_Healed.png
|   +-- Screenshot05_Controlled_Failure_Diagnosis.png
|   +-- Screenshot06_ArgoCD_Automatic_Recovery.png
|   +-- Screenshot07_Monitoring_Stack_Running.png
|   +-- Screenshot08_Prometheus_Target_Up.png
|   +-- Screenshot09_Prometheus_Custom_Metrics.png
|   +-- Screenshot10_Grafana-Dashboard-http-request-rate.png
|   +-- Screenshot11_Grafana_Workload_Activity.png
|
+-- README.md
```

---

## 4. Prerequisites

The following tools were used:

- Windows
- Docker Desktop
- Docker Desktop Kubernetes
- kubectl
- Git
- GitHub
- Helm
- Argo CD
- Prometheus
- Grafana

Verify Kubernetes:

```powershell
kubectl get nodes
```

Verify Helm:

```powershell
helm version
```

---

## 5. Application Deployment

The Python application runs in the `cse644` namespace.

The Kubernetes application consists of:

- Deployment
- ClusterIP Service
- ConfigMap
- Secret
- Liveness probe
- Readiness probe

The application listens on port `8888`.

The application can be inspected with:

```powershell
kubectl get all -n cse644
```

To access the application locally:

```powershell
kubectl port-forward service/python-web-service 8888:8888 -n cse644
```

Then open:

```text
http://localhost:8888
```

---

## 6. GitOps with Argo CD

Argo CD was installed in the Kubernetes cluster in the `argocd` namespace.

The Argo CD Application definition is stored at:

```text
homework3-gitops/argocd/application.yaml
```

Argo CD monitors:

```text
homework3-gitops/application
```

from the `main` branch of the GitHub repository.

Automated synchronization is enabled with:

```yaml
syncPolicy:
  automated:
    prune: true
    selfHeal: true
```

This allows Argo CD to automatically synchronize Git changes and correct live configuration drift.

Application status can be checked with:

```powershell
kubectl get applications -n argocd
```

A successful deployment displays:

```text
SYNC STATUS    HEALTH STATUS
Synced         Healthy
```

---

## 7. Git-Driven Change

To demonstrate GitOps reconciliation, the `PUBLIC_MESSAGE` value in `python-configmap.yaml` was changed from the original application message to:

```text
GitOps change successfully reconciled by Argo CD.
```

The change was committed and pushed to GitHub.

Argo CD detected the new desired state and automatically reconciled the Kubernetes ConfigMap without manually applying the changed application manifest.

The resulting value was verified with:

```powershell
kubectl get configmap python-config -n cse644 -o jsonpath="{.data.PUBLIC_MESSAGE}"
```

This demonstrated that Git was acting as the source of truth.

---

## 8. Drift Detection and Self-Healing

A live Kubernetes resource was manually modified to demonstrate configuration drift.

Because Argo CD automatic self-healing was enabled, the live state was compared against the desired state stored in Git.

Argo CD restored the Git-defined configuration automatically.

The final state returned to:

```text
Synced
Healthy
```

This demonstrates that manual changes to managed resources do not permanently override the desired state stored in Git.

---

## 9. Controlled Failure and Recovery

A controlled deployment failure was introduced by changing the container image from the valid version:

```text
rodraemonalvero/cse644-python-web:3.0
```

to a nonexistent image:

```text
rodraemonalvero/cse644-python-web:99.99-broken
```

The change was committed and pushed to Git.

Argo CD synchronized the intentionally broken desired state. Kubernetes attempted to deploy the image and produced:

```text
ImagePullBackOff
```

Pod events showed that the requested container image could not be found.

The failure was diagnosed using:

```powershell
kubectl get pods -n cse644
kubectl describe pod -n cse644 -l app=python-web
```

### Recovery

Recovery was performed through Git rather than manually repairing the live Kubernetes Deployment.

The image was restored to:

```text
rodraemonalvero/cse644-python-web:3.0
```

The corrected configuration was committed and pushed.

Argo CD automatically reconciled the cluster with the restored desired state. The failed pod was removed and the application returned to:

```text
Synced
Healthy
```

This demonstrates Git-based operational recovery.

---

## 10. Prometheus Monitoring

The Prometheus monitoring stack was installed using Helm:

```powershell
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
kubectl create namespace monitoring
helm install monitoring prometheus-community/kube-prometheus-stack -n monitoring
```

The monitoring stack includes:

- Prometheus
- Grafana
- Alertmanager
- kube-state-metrics
- Prometheus Node Exporter
- Prometheus Operator

The monitoring components were verified with:

```powershell
kubectl get pods -n monitoring
```

---

## 11. Application Metrics

The Python application exposes Prometheus-compatible metrics at:

```text
/metrics
```

The Kubernetes Service includes the label:

```yaml
labels:
  app: python-web
```

and its HTTP port is named:

```yaml
ports:
  - name: http
    protocol: TCP
    port: 8888
    targetPort: 8888
```

The ServiceMonitor is stored at:

```text
homework3-gitops/monitoring/python-servicemonitor.yaml
```

Prometheus successfully discovered the Python web application as a scrape target.

The target was verified as:

```text
UP
```

---

## 12. Custom Application Metric

The primary application metric used for this assignment is:

```text
cse644_http_requests_total
```

This metric counts HTTP requests handled by the Python web application.

The metric contains useful labels such as:

- HTTP method
- exported endpoint
- HTTP status
- pod
- service
- namespace

Observed endpoints included:

```text
/health/live
/health/ready
/metrics
```

The metric is useful because it demonstrates real application activity rather than only Kubernetes infrastructure health.

---

## 13. Grafana Dashboard

Grafana was connected to Prometheus and used to visualize the application metric.

Dashboard:

```text
CSE644 Application Observability
```

The dashboard includes application HTTP request information and a request-rate visualization.

The request-rate panel is titled:

```text
CSE644 Python Web - Request Rate
```

Prometheus data from `cse644_http_requests_total` is used to show how request activity changes over time.

---

## 14. Workload Activity Demonstration

Additional HTTP requests were sent to the Python application to create observable workload activity.

For example:

```powershell
1..100 | ForEach-Object { curl.exe -s http://localhost:8888/ > $null }
```

After the workload was generated, Prometheus collected the updated application metrics and Grafana displayed the resulting change.

This demonstrates the complete observability flow:

```text
User Requests
     |
     v
Python Application
     |
     v
/metrics
     |
     v
Prometheus
     |
     v
Grafana Dashboard
```

---

## 15. Technical Decisions

### Git as the Source of Truth

Application configuration is stored in Git instead of relying on manual Kubernetes changes. This provides revision history and allows recovery through known Git states.

### Argo CD Automated Synchronization

Automated synchronization with pruning and self-healing was enabled so that the cluster continuously converges toward the desired Git state.

### ClusterIP Service

The application uses a ClusterIP service because external exposure is not required for Prometheus monitoring. Local application access is provided through `kubectl port-forward`.

### ServiceMonitor

A ServiceMonitor was used because the kube-prometheus-stack includes the Prometheus Operator and provides native Kubernetes service discovery.

### Application-Level Metrics

A custom HTTP request metric was selected instead of relying only on infrastructure metrics. This provides visibility into actual application behavior.

---

## 16. Limitations

This implementation uses a local Docker Desktop Kubernetes cluster and is intended for coursework rather than production use.

Current limitations include:

- Local-only Kubernetes environment
- Port-forwarding required for browser access
- No public ingress for Grafana or Prometheus
- No persistent production monitoring storage configuration
- Basic Grafana dashboard
- No production alerting rules
- Single application workload

A production implementation would normally include persistent monitoring storage, authentication, TLS, ingress, alerting policies, resource limits, high availability, and external secret management.

---

## 17. Cleanup

Application resources can be removed with:

```powershell
kubectl delete application cse644-python-web -n argocd
```

Monitoring can be removed with:

```powershell
helm uninstall monitoring -n monitoring
kubectl delete namespace monitoring
```

Argo CD can be removed with:

```powershell
kubectl delete namespace argocd
```

The application namespace can be removed with:

```powershell
kubectl delete namespace cse644
```

These commands remove the assignment workloads and supporting GitOps/monitoring components from the local Kubernetes cluster.

---

## 18. Evidence

### Screenshot 01 — GitOps Deployment

`Screenshot01_GitOps_Deployment_Synced_Healthy.png`

Shows the Argo CD application in `Synced` and `Healthy` state and the Kubernetes application resources running successfully.

### Screenshot 02 — Application Access

`Screenshot02_Application_Access.png`

Shows the Python web application successfully accessible through `localhost:8888`.

### Screenshot 03 — GitOps Change Reconciled

`Screenshot03_GitOps_Change_Reconciled.png`

Shows the Git-driven ConfigMap change successfully reconciled by Argo CD.

### Screenshot 04 — Live Drift Self-Healed

`Screenshot04_Live_Drift_Self_Healed.png`

Shows Argo CD correcting manually introduced live configuration drift.

### Screenshot 05 — Controlled Failure Diagnosis

`Screenshot05_Controlled_Failure_Diagnosis.png`

Shows the intentionally invalid image producing an `ImagePullBackOff` condition and Kubernetes diagnostic information.

### Screenshot 06 — Argo CD Automatic Recovery

`Screenshot06_ArgoCD_Automatic_Recovery.png`

Shows the application returning to `Synced` and `Healthy` after the valid image was restored through Git.

### Screenshot 07 — Monitoring Stack Running

`Screenshot07_Monitoring_Stack_Running.png`

Shows Prometheus, Grafana, Alertmanager, and related monitoring components running in the `monitoring` namespace.

### Screenshot 08 — Prometheus Target UP

`Screenshot08_Prometheus_Target_Up.png`

Shows Prometheus successfully discovering and scraping the Python application target.

### Screenshot 09 — Prometheus Custom Metrics

`Screenshot09_Prometheus_Custom_Metrics.png`

Shows the custom `cse644_http_requests_total` application metric available in Prometheus.

### Screenshot 10 — Grafana HTTP Request Rate

`Screenshot10_Grafana-Dashboard-http-request-rate.png`

Shows the Grafana request-rate visualization based on application metrics.

### Screenshot 11 — Grafana Workload Activity

`Screenshot11_Grafana_Workload_Activity.png`

Shows Grafana responding to generated application workload and demonstrates observable application behavior.

---

## 19. Git Revision History

The repository contains separate commits demonstrating the major GitOps lifecycle steps, including:

```text
Add Argo CD application configuration
Update application message through GitOps
Introduce controlled deployment failure
Recover application by restoring valid image
Add Prometheus monitoring for Python application
Add Homework 3 GitOps and observability evidence
```

This revision history demonstrates that application changes, failure, recovery, and monitoring configuration were tracked through Git.

---

## 20. Conclusion

This assignment demonstrates a complete local GitOps and observability workflow.

Argo CD manages the desired Kubernetes application state from Git and automatically reconciles configuration changes and drift. A controlled deployment failure demonstrated how Git history can be used as part of an operational recovery workflow.

Prometheus provides application-level metrics collection, while Grafana visualizes application behavior. Together, Git, Argo CD, Kubernetes, Prometheus, and Grafana provide a basic example of declarative deployment management and observable cloud-native operations.