#!/bin/bash

TOKEN="squ_483ecb1bb60feb62cf7d3dc4f54fe16b49d1ac98"

echo "Running analysis for Chart project with cohesion metrics..."

# Run sonar-scanner with simplified configuration
cd /tmp/chart && sonar-scanner \
  -Dsonar.projectKey=chart \
  -Dsonar.sources=source \
  -Dsonar.java.binaries=build \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.login=$TOKEN \
  -Dsonar.java.source=11 \
  -Dsonar.sourceEncoding=UTF-8 \
  -Dsonar.java.metrics.enable=true \
  -Dsonar.exclusions=**/*Test.java,**/test/**/* \
  -X

echo "Analysis complete. Fetching metrics..."

# Get all available metrics first
echo "Available metrics:"
curl -s -u $TOKEN: "http://localhost:9000/api/metrics/search" | jq '.metrics[] | select(.key | contains("complexity") or .key | contains("cohesion") or .key | contains("coupling"))'

echo -e "\nFetching component metrics:"
curl -s -u $TOKEN: "http://localhost:9000/api/measures/component?component=chart&metricKeys=complexity,functions,cognitive_complexity,comment_lines_density" | jq '.'

echo -e "\nFetching component tree metrics (class-level):"
curl -s -u $TOKEN: "http://localhost:9000/api/measures/component_tree?component=chart&metricKeys=complexity,functions,cognitive_complexity&strategy=leaves" | jq '.'

echo "Done. Check the output above for available metrics."
