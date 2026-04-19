variable "subscription_id" {
  description = "Azure Subscription ID"
  type        = string
}

variable "resource_group_name" {
  description = "Resource Group name"
  type        = string
  default     = "ghaith-aks-gitops-rg"
}

variable "location" {
  description = "Azure region"
  type        = string
  default     = "swedencentral"
}

variable "acr_name" {
  description = "Azure Container Registry name (globally unique)"
  type        = string
  default     = "ghaithaksacr2026"
}

variable "aks_cluster_name" {
  description = "AKS cluster name"
  type        = string
  default     = "ghaith-aks-gitops"
}

variable "aks_dns_prefix" {
  description = "DNS prefix for AKS cluster"
  type        = string
  default     = "ghaithaks"
}

variable "node_count" {
  description = "Number of AKS worker nodes"
  type        = number
  default     = 2
}

variable "node_vm_size" {
  description = "VM size for AKS nodes"
  type        = string
  default     = "Standard_B2s"
}

variable "environment" {
  description = "Environment tag"
  type        = string
  default     = "dev"
}
