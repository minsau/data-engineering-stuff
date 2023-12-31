#!/bin/bash
set -e
source scripts/env.sh
source scripts/common.sh

function_name=$1

green "Enable required services"
gcloud --project=${PROJECT_ID} services enable cloudfunctions.googleapis.com
gcloud --project=${PROJECT_ID} services enable cloudbuild.googleapis.com
sleep 5

green "Create the function (${function_name}) & give the IAM user invoke access"
gcloud --project=${PROJECT_ID} functions deploy ${function_name} \
--trigger-resource ${BUCKET_NAME} \
--trigger-event "google.storage.object.finalize" \
--service-account ${IAM_ACCOUNT}@${PROJECT_ID}.iam.gserviceaccount.com \
--set-env-vars PROJECT_ID=${PROJECT_ID} \
--set-env-vars BUCKET_NAME=${BUCKET_NAME} \
--set-env-vars BQ_DATASET_PREFIX=${BQ_DATASET_PREFIX} \
--set-env-vars GOOGLE_CREDENTIALS_PATH=${GOOGLE_CREDENTIALS_PATH} \
--set-env-vars GCP_SECRET_NAME=${GCP_SECRET_NAME} \
--set-secrets GCP_SECRET_VALUE=${GCP_SECRET_NAME}:latest \
--memory 256MB --timeout 60s --max-instances 5 \
--runtime python38 --source "src/cloud_functions/places_transformer" --quiet

gcloud --project=${PROJECT_ID} functions add-iam-policy-binding ${function_name} \
--region ${REGION} --member serviceAccount:${IAM_ACCOUNT}@${PROJECT_ID}.iam.gserviceaccount.com \
--role roles/cloudfunctions.invoker