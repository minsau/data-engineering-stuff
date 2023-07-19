#!/bin/bash
set -e
source scripts/env.sh
source scripts/common.sh

green "Set project"
gcloud config set project ${PROJECT_ID}

green "Authorise GCP"
gcloud auth login --update-adc