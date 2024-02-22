#!/bin/bash

echo "Starting product webapp..."

uvicorn product_webapp:app --host 0.0.0.0 --port 8000 --reload


echo "Product webapp successfully loaded."