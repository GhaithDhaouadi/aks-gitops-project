# AKS GitOps Pipeline with Flux v2

![Azure](https://img.shields.io/badge/Azure-0078D4?style=for-the-badge&logo=microsoftazure&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)
![Terraform](https://img.shields.io/badge/Terraform-7B42BC?style=for-the-badge&logo=terraform&logoColor=white)
![Flux](https://img.shields.io/badge/Flux-2563EB?style=for-the-badge&logo=flux&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)

## Live Demo
| Environment | URL | Status |
| :--- | :--- | :--- |
| **Development** | http://74.241.159.108 | Live |
| **Production** | http://4.225.242.109 | Live |
| **Staging** | Internal (ClusterIP) | Running |

## Overview
Enterprise-grade GitOps pipeline on Azure Kubernetes Service (AKS) featuring multi-environment deployment, infrastructure as code, and automated continuous delivery with Flux v2. Any change pushed to GitHub is automatically synchronized to the cluster.

## Architecture
| Component | Technology | Purpose |
| :--- | :--- | :--- |
| Kubernetes Cluster | Azure Kubernetes Service (AKS) | Managed container orchestration |
| Container Registry | Azure Container Registry (ACR) | Private Docker image storage |
| GitOps Controller | Flux v2 | Automated sync from Git to cluster |
| Infrastructure as Code | Terraform | Version-controlled infrastructure |
| Application | FastAPI | REST API with health endpoints |
| Authentication | Managed Identity | Passwordless ACR access |

## Features
- GitOps continuous delivery with Flux v2 - cluster state defined entirely in Git
- Multi-environment deployment (dev/staging/prod) with environment-specific configurations
- Infrastructure as Code using Terraform for repeatable, version-controlled AKS provisioning
- Secure passwordless image pulling via AKS managed identity with AcrPull role
- Automated pod recovery with Kubernetes liveness and readiness probes
- Horizontal scaling demonstrated through Git commits (1 → 3 replicas)
- Zero-touch deployments - no manual kubectl commands required

## Project Structure
.
├── app/ # FastAPI application
│ ├── main.py # Application code
│ ├── requirements.txt # Python dependencies
│ └── Dockerfile # Container definition
├── terraform/ # Infrastructure as Code
│ ├── main.tf # AKS + ACR resources
│ ├── variables.tf # Input variables
│ └── outputs.tf # Output values
├── gitops-repo/ # Flux-synced manifests
│ ├── dev/ # Development environment
│ │ ├── namespace.yaml
│ │ ├── deployment.yaml
│ │ └── service.yaml
│ ├── staging/ # Staging environment
│ │ ├── namespace.yaml
│ │ ├── deployment.yaml
│ │ └── service.yaml
│ └── prod/ # Production environment
│ ├── namespace.yaml
│ ├── deployment.yaml
│ └── service.yaml
└── .gitignore # Git ignore rules

## GitOps Flow
Git Push → Flux Detects Change → Pulls Manifests → Applies to AKS
↓
Dev (1 pod) / Staging (2 pods) / Prod (3 pods)

## GitOps in Action
| Action | Result |
| :--- | :--- |
| Change `replicas: 1` to `replicas: 3` in `dev/deployment.yaml` | |
| Git commit and push | Flux detects change within 60 seconds |
| Cluster automatically scales | 3 pods running in dev namespace |

## Azure Resources Created
| Resource | Name | Purpose |
| :--- | :--- | :--- |
| Resource Group | `ghaith-aks-gitops-rg` | Logical container for all resources |
| AKS Cluster | `ghaith-aks-gitops` | Managed Kubernetes cluster (2 nodes) |
| Container Registry | `ghaithaksacr2026` | Private Docker image registry |
| Public IPs | 2x LoadBalancer | DEV and PROD external access |
| Managed Identity | System-assigned | Passwordless ACR authentication |

## Constraints & Learnings
| Constraint | Solution |
| :--- | :--- |
| Student subscription VM size limitation | Used `standard_b2s_v2` instead of `Standard_B2s` |
| Public IP limit (3 per region) | Staging configured as internal ClusterIP |
| Cloud Shell Docker restrictions | Built images on local VM and pushed to ACR |
| Flux sudo requirement in Cloud Shell | Installed locally in `~/.local/bin` |

These constraints demonstrate real-world troubleshooting and adaptation to enterprise security boundaries.

## Skills Demonstrated
- Azure Kubernetes Service (AKS) cluster provisioning and management
- Flux v2 GitOps continuous delivery
- Terraform Infrastructure as Code
- Azure Container Registry (ACR) with managed identity authentication
- Kubernetes manifests (Deployments, Services, Namespaces)
- Multi-environment deployment strategies
- FastAPI development with health check endpoints
- Docker containerization
- Git version control and GitHub integration
- Cloud resource troubleshooting and debugging

## Screenshots
<img width="1867" height="477" alt="Terraform Output" src="https://github.com/user-attachments/assets/c7231d71-f613-403c-9035-dcadead1d2ab" />
<img width="1867" height="726" alt="Azure Portal - AKS Cluster" src="https://github.com/user-attachments/assets/495421bf-b539-44ce-8ab3-3e7fde5405aa" />
<img width="1030" height="152" alt="Nodes Health" src="https://github.com/user-attachments/assets/ec97656a-3500-4c75-ac84-8f885d7bb33d" />
<img width="1257" height="826" alt="All Pods Health" src="https://github.com/user-attachments/assets/043b6bae-48b6-45ee-a06e-b629f0533c30" />
<img width="921" height="64" alt="Flux Healthy" src="https://github.com/user-attachments/assets/857632f8-167b-4083-8387-0c65498d3eb8" />
<img width="1866" height="971" alt="DEV Dashboard (Blue)" src="https://github.com/user-attachments/assets/c60248ab-9b5e-42ea-b89d-0b55c8084d16" />
<img width="1865" height="969" alt="PROD Dashboard (Green)" src="https://github.com/user-attachments/assets/2d1410f1-64e0-4c0c-bd1c-180408c0f4f0" />

## Author
**Ghaith Dhaouadi** - Cloud DevOps Engineer
