# 5. Experimental Procedure

## 5.1 Setting up the Environment

1. Infrastructure Setup:
   - Install required dependencies (Java 11, Docker, Perl modules, SVN)
   - Configure Docker environment for SonarQube
   - Set up SonarQube server locally on port 9000
   - Install and configure sonar-scanner CLI tool

2. Project Configuration:
   - Initialize Defects4J repository
   - Checkout selected projects (Chart, Collections, Compress, Lang)
   - Create sonar-project.properties for each project with:
     * Source and binary paths configuration
     * Test exclusion patterns
     * Cohesion metric enablement
     * Project-specific settings

3. SonarQube Configuration:
   - Set up initial admin account
   - Generate authentication tokens for each project
   - Create project spaces in SonarQube
   - Configure analysis parameters focusing on cohesion metrics

## 5.2 Running Tests and Analysis

1. Project Compilation:
   ```bash
   # For each project (Chart, Collections, Compress, Lang):
   cd /tmp/[project]
   defects4j compile
   ```

2. Static Analysis:
   - Run SonarQube analysis on each project:
   ```bash
   sonar-scanner \
     -Dsonar.projectKey=[project] \
     -Dsonar.sources=src/main/java \
     -Dsonar.java.binaries=target/classes \
     -Dsonar.host.url=http://localhost:9000 \
     -Dsonar.login=[project-specific-token]
   ```
   Note: Each project uses its own authentication token for secure analysis

3. Cohesion Analysis:
   - Execute custom cohesion analysis script:
   ```bash
   ./calculate_cohesion_and_bugs.sh
   ```
   This script:
   - Queries SonarQube API for metrics
   - Calculates LCOM using complexity and method relationships
   - Categorizes files by cohesion levels
   - Correlates cohesion with bug counts
   
   Metrics collected:
     * LCOM (Lack of Cohesion of Methods)
     * Function count
     * Complexity metrics
     * Bug counts

## 5.3 Data Collection and Recording

1. Metric Collection:
   - LCOM values for each file
   - Bug distribution across cohesion categories
   - Complexity metrics
   - Function counts

2. Data Organization:
   - Categorize files by cohesion levels:
     * High cohesion (LCOM 0-2): Well-organized code where methods work closely together
     * Medium cohesion (LCOM 3-5): Moderately organized code with some method relationships
     * Low cohesion (LCOM >5): Code where methods are loosely related or unrelated
   - Record bug distribution:
     * Track number of bugs in each cohesion category
     * Calculate bug density per category
     * Identify patterns in bug distribution
   - Calculate metrics:
     * Average LCOM per category
     * Overall project LCOM
     * Correlation between LCOM and bug counts

3. Data Storage and Analysis:
   - Store data in structured JSON format including:
     * File-level metrics (name, path, complexity, functions, bugs, LCOM)
     * Project summary statistics
     * Cohesion category distributions
     * Bug correlation data
   - Generate analysis reports with:
     * Category-wise bug distribution
     * Statistical correlations
     * Trend analysis
   - Maintain comprehensive logs:
     * Analysis execution details
     * Error reports
     * Edge cases and anomalies
     * Configuration changes

# 6. Risks and Mitigation

## 6.1 Technical Risks

1. SonarQube Analysis Failures
   - Risk: Analysis may fail due to project structure or compatibility issues
   - Mitigation:
     * Validate project structure before analysis
     * Use specific SonarQube version (latest LTS)
     * Maintain proper Java version compatibility
     * Document successful configuration patterns

2. Metric Calculation Accuracy
   - Risk: LCOM calculation might not perfectly reflect actual code cohesion
   - Mitigation:
     * Use multiple supporting metrics (complexity, functions)
     * Validate calculations against manual code review
     * Document calculation assumptions
     * Consider alternative cohesion metrics

3. Data Collection Completeness
   - Risk: Missing or incomplete metrics for some files
   - Mitigation:
     * Implement validation checks
     * Log files with missing data
     * Use fallback calculation methods
     * Monitor analysis coverage

## 6.2 Process Risks

1. Environment Consistency
   - Risk: Different results across different machines
   - Mitigation:
     * Use Docker for consistent environment
     * Document exact versions of all tools
     * Provide detailed setup instructions
     * Validate results across different setups

2. Project Compatibility
   - Risk: Some projects may not be analyzable
   - Mitigation:
     * Pre-validate project structure
     * Maintain list of compatible projects
     * Document project-specific requirements
     * Have backup projects available

3. Resource Constraints
   - Risk: Analysis of large projects may be time-consuming
   - Mitigation:
     * Implement parallel processing
     * Set reasonable timeouts
     * Focus on most relevant metrics
     * Optimize analysis configuration

## 6.3 Data Quality Risks

1. False Positives in Bug Detection
   - Risk: Static analysis may report false bugs
   - Mitigation:
     * Cross-validate with Defects4J known bugs
     * Manual verification of significant findings
     * Document false positive patterns
     * Adjust detection thresholds

2. Statistical Significance
   - Risk: Insufficient data points in some categories
   - Mitigation:
     * Ensure minimum sample sizes
     * Use appropriate statistical tests
     * Document data limitations
     * Adjust category boundaries if needed

## 6.4 Mitigation Strategy Implementation

1. Monitoring and Logging
   - Implement comprehensive logging
   - Regular validation of results
   - Track analysis progress
   - Document all issues encountered

2. Quality Assurance
   - Regular backups of collected data
   - Validation scripts for data integrity
   - Cross-checking of results
   - Peer review of analysis

3. Documentation
   - Maintain detailed setup guides
   - Document all assumptions
   - Record all configuration changes
   - Keep track of workarounds used

4. Contingency Planning
   - Backup analysis methods
   - Alternative metric calculations
   - Multiple data collection approaches
   - Fallback project selection criteria
