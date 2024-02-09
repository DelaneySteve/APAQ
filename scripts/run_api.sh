#!/bin/bash

cd "$(dirname "$0")/.." || exit

api_key=$(openssl rand -base64 16)
export API_KEY=${api_key}
echo "The API key for this session is: ${api_key}"
echo

python -m src.main