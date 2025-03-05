#!/bin/bash

TOKEN="squ_483ecb1bb60feb62cf7d3dc4f54fe16b49d1ac98"

echo "Calculating cohesion metrics for Chart project..."

# Get class-level metrics and calculate cohesion score
curl -s -u $TOKEN: "http://localhost:9000/api/measures/component_tree?component=chart&metricKeys=complexity,functions&strategy=leaves" | \
jq '
  def calc_cohesion_score:
    if (.measures | length) == 2 then
      (.measures[] | select(.metric == "complexity") | .value | tonumber) /
      (.measures[] | select(.metric == "functions") | .value | tonumber)
    else
      null
    end;

  .components |
  map(select(.measures | length > 0)) |
  map({
    file: .name,
    complexity: (.measures[] | select(.metric == "complexity") | .value),
    functions: (.measures[] | select(.metric == "functions") | .value),
    cohesion_score: calc_cohesion_score
  }) |
  map(select(.cohesion_score != null)) |
  sort_by(.cohesion_score) |
  {
    files: .,
    summary: {
      total_files: length,
      avg_cohesion_score: (map(.cohesion_score) | add) / length,
      min_cohesion: map(.cohesion_score) | min,
      max_cohesion: map(.cohesion_score) | max
    }
  }
'

echo -e "\nInterpretation:"
echo "- Cohesion score is complexity/functions ratio"
echo "- Lower scores indicate better cohesion (methods are simpler relative to their number)"
echo "- Higher scores suggest potential cohesion issues (complex methods, possible need for refactoring)"
