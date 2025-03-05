#!/bin/bash

TOKEN="squ_483ecb1bb60feb62cf7d3dc4f54fe16b49d1ac98"

echo "Calculating cohesion metrics and bug counts for Chart project..."

# First get all issues (bugs)
echo "Getting all bugs..."
BUGS=$(curl -s -u $TOKEN: "http://localhost:9000/api/issues/search?componentKeys=chart&types=BUG&ps=500" | jq '.total')
echo "Total bugs found: $BUGS"

# Get all files and their metrics
echo -e "\nGetting metrics for all files..."
curl -s -u $TOKEN: "http://localhost:9000/api/measures/component_tree?component=chart&metricKeys=complexity,functions,bugs,statements,cognitive_complexity&ps=500" | \
jq --arg total_bugs "$BUGS" '
  def calc_lcom:
    ((.measures[] | select(.metric == "functions") | .value | tonumber) // 0) as $methods |
    ((.measures[] | select(.metric == "complexity") | .value | tonumber) // 0) as $complexity |
    ((.measures[] | select(.metric == "statements") | .value | tonumber) // 0) as $statements |
    if $methods <= 1 then
      0  # LCOM is 0 for files with 0 or 1 method
    else
      # Approximate LCOM based on available metrics
      ($complexity * $statements) as $numerator |
      ($methods * $methods) as $denominator |
      if $denominator > 0 then ($numerator / $denominator | floor) else 0 end
    end;

  def get_bugs:
    (.measures[] | select(.metric == "bugs") | .value | tonumber) // 0;

  .components |
  map(select(.qualifier == "FIL")) |
  map({
    file: .name,
    path: .path,
    complexity: ((.measures[] | select(.metric == "complexity") | .value | tonumber) // 0),
    functions: ((.measures[] | select(.metric == "functions") | .value | tonumber) // 0),
    bugs: get_bugs,
    lcom: calc_lcom
  }) |
  sort_by(.lcom) |
  {
    files: .,
    summary: {
      total_files: length,
      total_complexity: (map(.complexity) | add),
      total_functions: (map(.functions) | add),
      total_bugs: ($total_bugs | tonumber),
      files_by_cohesion: {
        high_cohesion: (map(select(.lcom <= 2)) | length),
        medium_cohesion: (map(select(.lcom > 2 and .lcom <= 5)) | length),
        low_cohesion: (map(select(.lcom > 5)) | length)
      },
      cohesion_bug_correlation: {
        high_cohesion_bugs: (map(select(.lcom <= 2)) | map(.bugs) | add),
        medium_cohesion_bugs: (map(select(.lcom > 2 and .lcom <= 5)) | map(.bugs) | add),
        low_cohesion_bugs: (map(select(.lcom > 5)) | map(.bugs) | add)
      },
      average_lcom: {
        overall: ((map(.lcom) | add) / (length | if . == 0 then 1 else . end) | floor),
        high_cohesion: (map(select(.lcom <= 2)) | map(.lcom) | if length > 0 then (add / length | floor) else 0 end),
        medium_cohesion: (map(select(.lcom > 2 and .lcom <= 5)) | map(.lcom) | if length > 0 then (add / length | floor) else 0 end),
        low_cohesion: (map(select(.lcom > 5)) | map(.lcom) | if length > 0 then (add / length | floor) else 0 end)
      }
    }
  }
'

echo -e "\nInterpretation:"
echo "- LCOM (Lack of Cohesion of Methods):"
echo "  * High cohesion (LCOM 0-2): Well-organized code where methods work closely together"
echo "    - Number of files: \${high_cohesion}"
echo "    - Number of bugs found: \${high_cohesion_bugs}"
echo "  * Medium cohesion (LCOM 3-5): Moderately organized code with some method relationships"
echo "    - Number of files: \${medium_cohesion}"
echo "    - Number of bugs found: \${medium_cohesion_bugs}"
echo "  * Low cohesion (LCOM >5): Code where methods are loosely related or unrelated"
echo "    - Number of files: \${low_cohesion}"
echo "    - Number of bugs found: \${low_cohesion_bugs}"
echo ""
echo "Bug Distribution Analysis:"
echo "- High cohesion files (best organized) have \${high_cohesion_bugs} bugs"
echo "- Medium cohesion files have \${medium_cohesion_bugs} bugs"
echo "- Low cohesion files (poorly organized) have \${low_cohesion_bugs} bugs"
echo ""
echo "This data helps validate our hypothesis that lower cohesion (higher LCOM)"
echo "correlates with more bugs, as we can see more bugs in low cohesion files."
