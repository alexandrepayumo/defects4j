#!/bin/bash

# Your SonarQube token
TOKEN="squ_483ecb1bb60feb62cf7d3dc4f54fe16b49d1ac98"

# Function to get available metrics for a project
get_available_metrics() {
    local project=$1
    echo "Available metrics for $project:"
    curl -s -u $TOKEN: "http://localhost:9000/api/measures/component?component=$project&metricKeys=ncloc,complexity,violations,bugs,code_smells,lcom,lcom4" | jq '.'
}

# Function to get LCOM metrics for a project
get_lcom() {
    local project=$1
    # Try to get both LCOM and LCOM4 metrics
    curl -s -u $TOKEN: "http://localhost:9000/api/measures/component?component=$project&metricKeys=lcom,lcom4" | \
    jq -r '.component.measures[] | select(.metric == "lcom" or .metric == "lcom4") | "\(.metric):\(.value)"'
}

# Function to get number of bugs/issues for a project
get_bugs() {
    local project=$1
    curl -s -u $TOKEN: "http://localhost:9000/api/measures/component?component=$project&metricKeys=bugs" | \
    jq -r '.component.measures[] | select(.metric == "bugs") | .value'
}

# Array of projects to analyze
projects=("chart" "collections" "compress" "lang")

echo "Checking available metrics..."
echo "============================"
for project in "${projects[@]}"; do
    get_available_metrics $project
    echo "----------------------------"
done

echo -e "\nProject Analysis Results"
echo "======================="
echo "Project | LCOM Metrics | Bugs"
echo "----------------------"

# Analyze each project
for project in "${projects[@]}"; do
    lcom=$(get_lcom $project)
    bugs=$(get_bugs $project)
    if [ -z "$lcom" ]; then
        lcom="N/A"
    fi
    if [ -z "$bugs" ]; then
        bugs="N/A"
    fi
    echo "$project | $lcom | $bugs"
done

echo -e "\nAnalysis Summary:"
echo "================="
echo "This data can be used to test the hypothesis that projects with higher LCOM (lower cohesion)"
echo "have more defects than projects with lower LCOM (higher cohesion)."
echo
echo "Expected results based on hypothesis:"
echo "- Collections and Lang: Higher LCOM values, more bugs"
echo "- Chart and Compress: Lower LCOM values, fewer bugs"

echo -e "\nNote: If LCOM metrics are showing as N/A, we may need to:"
echo "1. Enable the appropriate quality profile in SonarQube"
echo "2. Re-run the analysis with additional parameters"
echo "3. Check if the Java plugin is properly configured"
