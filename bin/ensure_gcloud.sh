#!/bin/bash
set -euo pipefail

# Ensure gcloud CLI user auth (for `gcloud ...` commands)
if ! gcloud auth print-access-token >/dev/null 2>&1; then
  echo "[ensure_gcloud] No gcloud user auth found. Launching browser login..."
  gcloud auth login
fi

# Ensure ADC (for client libraries / scripts using application default creds)
if ! gcloud auth application-default print-access-token >/dev/null 2>&1; then
  # If a service account key is already configured via env var, honor it.
  if [[ -n "${GOOGLE_APPLICATION_CREDENTIALS:-}" && -f "$GOOGLE_APPLICATION_CREDENTIALS" ]]; then
    echo "[ensure_gcloud] ADC via GOOGLE_APPLICATION_CREDENTIALS is set to: $GOOGLE_APPLICATION_CREDENTIALS"
  else
    echo "[ensure_gcloud] No ADC found. Launching browser login for Application Default Credentials..."
    gcloud auth application-default login
  fi
fi

echo "[ensure_gcloud] gcloud user auth and ADC are ready."

