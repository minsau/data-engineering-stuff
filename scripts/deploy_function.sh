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
--trigger-http --entry-point process --region ${REGION}  \
--service-account ${IAM_ACCOUNT}@${PROJECT_ID}.iam.gserviceaccount.com \
--set-env-vars TOPIC_PROJECT_ID=${PROJECT_ID} \
--set-env-vars BUCKET_NAME=${BUCKET_NAME} \
--memory 256MB --timeout 60s --max-instances 5 \
--runtime python38 --source "src/cloud_functions/places_transformer" --quiet

gcloud --project=${PROJECT_ID} functions add-iam-policy-binding ${function_name} \
--region ${REGION} --member serviceAccount:${IAM_ACCOUNT}@${PROJECT_ID}.iam.gserviceaccount.com \
--role roles/cloudfunctions.invoker