#!/bin/bash

# kurbeScript.sh
# Objective: Start a local Kubernetes cluster with Minikube,
# verify cluster status, and list available pods.

# Step 1: Ensure minikube is installed
if ! command -v minikube &> /dev/null
then
    echo "❌ Minikube is not installed. Please install it first."
    echo "👉 On Linux: curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64"
    echo "👉 sudo install minikube-linux-amd64 /usr/local/bin/minikube"
    exit 1
fi

# Step 2: Start Minikube cluster
echo "🚀 Starting Minikube cluster..."
minikube start

# Step 3: Verify cluster info
echo "🔍 Verifying cluster status..."
kubectl cluster-info

# Step 4: Retrieve available pods
echo "📋 Listing pods in all namespaces..."
kubectl get pods --all-namespaces
