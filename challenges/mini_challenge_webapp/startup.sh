#!/bin/bash

echo "Starting product webapp..."

uvicorn product_webapp:app --reload

echo "Product webapp successfully loaded."