# Setting up SonarQube Analysis for Defects4J Projects

This guide explains how to set up SonarQube analysis for analyzing code cohesion in Chart, Collections, Compress, and Lang projects from defects4j.

## Prerequisites

- Java 11
- Docker
- Perl with required modules
- SVN (Subversion)

## Step 1: Install Required Packages

```bash
# Install Perl modules
sudo pacman -S perl-string-interpolate perl-dbi

# Install SVN
sudo pacman -S subversion

# Install Docker
sudo pacman -S docker
```

## Step 2: Initialize Defects4J

```bash
# Initialize defects4j
cd defects4j
./init.sh
```

## Step 3: Checkout Projects

```bash
# Checkout all projects
cd defects4j
./framework/bin/defects4j checkout -p Chart -v 1b -w /tmp/chart
./framework/bin/defects4j checkout -p Collections -v 1b -w /tmp/collections
./framework/bin/defects4j checkout -p Compress -v 1b -w /tmp/compress
./framework/bin/defects4j checkout -p Lang -v 1b -w /tmp/lang
```

## Step 4: Set Up Required Dependencies

```bash
# Set up Cobertura for code coverage
mkdir -p /home/tuturu/Documents/soen345/defects4j/framework/projects/lib/cobertura-2.0.3-lib
cd /home/tuturu/Documents/soen345/defects4j/framework/projects/lib
wget https://sourceforge.net/projects/cobertura/files/cobertura/2.0.3/cobertura-2.0.3-bin.tar.gz
tar -xzf cobertura-2.0.3-bin.tar.gz
cp -r cobertura-2.0.3/* cobertura-2.0.3-lib/
rm cobertura-2.0.3-bin.tar.gz

## Step 5: Set Up SonarQube

```bash
# Start Docker service
sudo systemctl start docker

# Pull and run SonarQube
sudo docker run -d --name sonarqube -p 9000:9000 sonarqube:latest

# Download and install sonar-scanner
curl -LO https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-5.0.1.3006-linux.zip
sudo unzip sonar-scanner-cli-5.0.1.3006-linux.zip -d /opt
sudo ln -s /opt/sonar-scanner-5.0.1.3006-linux/bin/sonar-scanner /usr/local/bin/sonar-scanner
```

## Step 5: Configure Projects

Create sonar-project.properties for each project:

### Chart Project (/tmp/chart/sonar-project.properties)
```properties
sonar.projectKey=chart
sonar.projectName=JFreeChart
sonar.projectVersion=1.0
sonar.sources=source
sonar.java.binaries=build
sonar.sourceEncoding=UTF-8

# Exclude test files and large files
sonar.exclusions=**/*Test.java,**/test/**/*,**/*.txt,**/*.xml,**/*.properties,**/lib/**/*
sonar.coverage.exclusions=**/*Test.java,**/test/**/*

# Focus on cohesion metrics
sonar.java.metrics.enable=true
```

### Collections Project (/tmp/collections/sonar-project.properties)
```properties
sonar.projectKey=collections
sonar.projectName=Apache Collections
sonar.projectVersion=1.0
sonar.sources=src/main/java
sonar.java.binaries=target/classes
sonar.sourceEncoding=UTF-8

# Exclude test files and large files
sonar.exclusions=**/*Test.java,**/test/**/*,**/*.txt,**/*.xml,**/*.properties,**/lib/**/*
sonar.coverage.exclusions=**/*Test.java,**/test/**/*

# Focus on cohesion metrics
sonar.java.metrics.enable=true
```

### Compress Project (/tmp/compress/sonar-project.properties)
```properties
sonar.projectKey=compress
sonar.projectName=Apache Compress
sonar.projectVersion=1.0
sonar.sources=src/main/java
sonar.java.binaries=target/classes
sonar.sourceEncoding=UTF-8

# Exclude test files and large files
sonar.exclusions=**/*Test.java,**/test/**/*,**/*.txt,**/*.xml,**/*.properties,**/lib/**/*
sonar.coverage.exclusions=**/*Test.java,**/test/**/*

# Focus on cohesion metrics
sonar.java.metrics.enable=true
```

### Lang Project (/tmp/lang/sonar-project.properties)
```properties
sonar.projectKey=lang
sonar.projectName=Apache Lang
sonar.projectVersion=1.0
sonar.sources=src/main/java
sonar.java.binaries=target/classes
sonar.sourceEncoding=UTF-8

# Exclude test files and large files
sonar.exclusions=**/*Test.java,**/test/**/*,**/*.txt,**/*.xml,**/*.properties,**/lib/**/*
sonar.coverage.exclusions=**/*Test.java,**/test/**/*

# Focus on cohesion metrics
sonar.java.metrics.enable=true
```

## Step 6: SonarQube UI Setup and Analysis

### 6.1 Initial Login
1. Open your browser and navigate to http://localhost:9000
2. You'll see the SonarQube login page
3. Use the default credentials:
   - Username: admin
   - Password: admin
4. On first login, you'll be prompted to change the password
   - Enter a new secure password
   - Remember this password for future use

### 6.2 Generate Authentication Tokens
You'll need to generate a separate token for each project:

1. For each project (Chart, Collections, Compress, Lang):
   a. Click on your profile icon in the top-right corner
   b. Select "My Account"
   c. Click on the "Security" tab
   d. Under "Generate Tokens":
      - Enter the project name as token name (e.g., "chart-analysis", "collections-analysis", etc.)
      - Leave "Type" as "User Token"
      - Set expiration if desired (optional)
   e. Click "Generate"
   f. IMPORTANT: Copy and save each generated token immediately - you won't be able to see them again
   g. Label each token clearly to know which belongs to which project

### 6.3 Create Projects
1. Click "Create New Project" on the main dashboard
2. Select "Manually" for project creation
3. Create four projects with these details:
   - Project: chart
     - Display Name: JFreeChart
     - Key: chart
   - Project: collections
     - Display Name: Apache Collections
     - Key: collections
   - Project: compress
     - Display Name: Apache Compress
     - Key: compress
   - Project: lang
     - Display Name: Apache Lang
     - Key: lang

### 6.4 Run Analysis

1. After creating each project, you'll see the analysis setup page
2. Select "Other" as your build tool (since defects4j uses Ant)
3. For each project, first compile it using defects4j:

```bash
# Compile Chart project
cd /tmp/chart && defects4j compile

# Compile Collections project
cd /tmp/collections && defects4j compile

# Compile Compress project
cd /tmp/compress && defects4j compile

# Compile Lang project
cd /tmp/lang && defects4j compile
```

4. Then run sonar-scanner for each project:

```bash
# Analyze Chart project
cd /tmp/chart && sonar-scanner \
  -Dsonar.projectKey=chart \
  -Dsonar.sources=src/main/java \
  -Dsonar.java.binaries=target/classes \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.login=squ_483ecb1bb60feb62cf7d3dc4f54fe16b49d1ac98

# Analyze Collections project
cd /tmp/collections && sonar-scanner \
  -Dsonar.projectKey=collections \
  -Dsonar.sources=src/java \
  -Dsonar.java.binaries=build/classes \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.login=<your-collections-project-token>

# Analyze Compress project
cd /tmp/compress && sonar-scanner \
  -Dsonar.projectKey=compress \
  -Dsonar.sources=src/main/java \
  -Dsonar.java.binaries=target/classes \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.login=<your-compress-project-token>

# Analyze Lang project
cd /tmp/lang && sonar-scanner \
  -Dsonar.projectKey=lang \
  -Dsonar.sources=src/main/java \
  -Dsonar.java.binaries=target/classes \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.login=<your-lang-project-token>
```

5. After running each command:
   - Wait for the analysis to complete
   - The page will automatically refresh when done
   - You'll see the analysis results in the SonarQube UI

Note: The paths for sources and binaries might need adjustment based on the actual project structure after compilation. You can verify the correct paths by checking the project directories.

## Step 7: View and Interpret Results

### 7.1 Access Project Results
1. Go to http://localhost:9000
2. Login with your credentials
3. Click "Projects" in the top navigation
4. You'll see all four projects listed with their overall metrics

### 7.2 Analyze Cohesion Metrics
For each project:
1. Click on the project name to view detailed metrics
2. In the left sidebar, click on "Measures"
3. Look for these key cohesion metrics:
   - LCOM4 (Lack of Cohesion of Methods): Lower is better
   - RFC (Response for Class): Lower indicates better encapsulation
   - CBO (Coupling Between Objects): Lower indicates better modularity

### 7.3 Compare Projects
1. Focus on these aspects to verify the hypothesis:
   - Collections and Lang (Expected less cohesive):
     * Should show higher LCOM4 values
     * Likely higher RFC and CBO metrics
   - Chart and Compress (Expected more cohesive):
     * Should show lower LCOM4 values
     * Likely lower RFC and CBO metrics

### 7.4 View Code Details
1. Click on any metric to see class-level breakdown
2. Click on specific classes to view:
   - Detailed code analysis
   - Specific cohesion issues
   - Suggestions for improvement

### 7.5 Export Metrics via API
To fetch the cohesion metrics (LCOM4, RFC, CBO) programmatically using the SonarQube Web API:

```bash
# Replace <your-token> with your SonarQube authentication token
# For Chart project
curl -u <your-token>: "http://localhost:9000/api/measures/component?component=chart&metricKeys=lcom4,rfc,cbo"

# For Collections project
curl -u <your-token>: "http://localhost:9000/api/measures/component?component=collections&metricKeys=lcom4,rfc,cbo"

# For Compress project
curl -u <your-token>: "http://localhost:9000/api/measures/component?component=compress&metricKeys=lcom4,rfc,cbo"

# For Lang project
curl -u <your-token>: "http://localhost:9000/api/measures/component?component=lang&metricKeys=lcom4,rfc,cbo"
```

The API will return JSON responses containing the requested metrics. You can also get class-level metrics by using the search API:

```bash
# Example: Get metrics for all classes in the Chart project
curl -u <your-token>: "http://localhost:9000/api/measures/search?projectKeys=chart&metricKeys=lcom4,rfc,cbo"
```

For automated processing, you can use tools like `jq` to parse the JSON response:

```bash
# Example: Extract just the metric values for Chart project
curl -u <your-token>: "http://localhost:9000/api/measures/component?component=chart&metricKeys=lcom4,rfc,cbo" | jq '.component.measures[] | {metric: .metric, value: .value}'
```

### 7.6 Export Results (Optional)
1. Click on "More" in the top-right of any project
2. Select "Download PDF Report" for documentation
3. Use "Activity" tab to track analysis history

## Cleanup

```bash
# Stop and remove SonarQube container
sudo docker stop sonarqube
sudo docker rm sonarqube

# Remove temporary project directories
rm -rf /tmp/chart /tmp/collections /tmp/compress /tmp/lang
squ_483ecb1bb60feb62cf7d3dc4f54fe16b49d1ac98
```
