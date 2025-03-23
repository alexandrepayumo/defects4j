Background Research Report - Mahad and Maxence

Overview of DefectsJ4
Defects4J is a repository containing many different codebases for different software coded in Java. The repository contains the working code for the programs as well as intentionally bugged code, intended to further research in the software testing field.

There are a total of 835 bugs over 17 open-source Java projects. The repository contains a test suite that has a test that passes in the debugged version and fails in the bugged version, meaning the bug is reproducible and the codebase could contain mutants that can be strongly killed.

The repository offers a command-line interface with different commands able to perform important operations on the different codebases. Notable commands are “bids” which lists all bug IDs for a specified project, and “mutation” which conducts mutation testing for a specified project version. 

The repository can be used for many purposes. Test suites can be run on the different open-source projects to test their effectiveness, automated debugging tools can be tested on it, hypotheses using different metrics of the codebases can be tested. 

Explanation of testing methods
Software can be tested in several ways, each with its own purpose.

Mutation testing evaluates the effectiveness of test suites by introducing small changes (mutations) into the program’s code (ex: modifying an operator, changing a return value). Then, test cases are run to check if they can detect these intentional faults. If a test case fails, it means it “killed” the mutation and is effective. If not, the test needs to be reviewed. Mutation testing helps gauge the robustness of a test suite and catches subtle errors that might otherwise go unnoticed.

Regression testing, on the other hand, focuses on verifying that prior software still functions correctly after changes have been made. Typically, it involves writing a test for a known bug and re-running this test automatically on every change onwards. This allows developers to quickly identify any modification that reintroduces a bug. Regression testing is particularly useful in iterative development, as new code is pushed often and future releases should not cause issues that previous versions did not have.1

Finally, unit testing verifies individual software components (usually methods) in isolation. The goal is to ensure that each small unit behaves as expected. In test driven development, unit tests are produced before implementing the code itself. Unit tests help identify issues early in development and prevent them from propagating elsewhere in the program, which would create a larger defect that is more difficult to maintain. 
 
Experiment Design Document - Alexandre and Charbel
Title:
Experiment Design for relationship between cohesion and defects in a codebase.
1. Background and Objectives
Repository Overview: Defects4J is a repository on GitHub containing 17 different open-source Java projects. These Java projects altogether contain 854 bugs (and 10 deprecated bugs). Within the repository, for each project there is a fixed version and a buggy version of the project which are contained. The aim of this repository is to provide developers the opportunity to research software testing. Using this repository, automated testing, mutation testing, and other types of testing can be run across the different projects. Furthermore, the Defects4j repository provides direct support for JUnit, allowing developers to create their own tests. In addition, the repository provides a built-in command line tool which developers can use to view projects, run tests, run mutation tests, or complete other objectives.
Objective: The objective of our project is to determine the relationship between cohesion and defects within a codebase. Cohesion is the measure of which elements located in the same module belong together. In order to analyze the cohesion within different projects located within Defects4j, the Lack of Cohesion (LCOM) metric will be used. Defects4j does not provide native support for this metric, so data will be gathered by using SciTools Understand (sci-understand) to analyze the project and export the metrics. The LCOM metric can be calculated using the following formula:
LCOM=∣P∣−∣Q∣​max(∣P∣−∣Q∣,1)
Where:
P = Number of method pairs that do not share instance variables.
Q = Number of method pairs that share at least one instance variable.
	Using this formula, if a high LCOM is found, then this indicates that there is low cohesion. On the other hand, if a low LCOM is found within a project, then this indicates that there is high cohesion.

2. Hypothesis
The hypothesis for our project is the following: “A codebase with low cohesion will have a test suite finding a high amount of defects in the code, as compared to a codebase with high cohesion which will have lower defects”. Our hypothesis is rooted in the fact that in projects where functions are loosely located together despite not being related to each other, more defects will be found given the fact that there is less of a logical organization to the code. A lower cohesion means that either classes are too big and encompass too much code, or, functions within a class need to access more code from classes found elsewhere. This complication in the code makes it so that the code is less maintainable, which should theoretically lead to a higher rate of defects. Our hypothesis does not assume any given relationship between cohesion in defects (i.e. linear, quadratic, logarithmic, etc.), it simply assumes that the two variables are positively correlated together.
3. Selected Tools and Techniques
Tools:
Defects4j: Will be using the CLI of Defects4j in order to gather the number of defects for a project
Sci-understand: Will be using this tool to compute the LCOM metric across different projects
Testing techniques:
The main testing technique that will be assessed is unit testing. Unit testing is the method of testing if specific functions have an expected output. The reason this method of testing was chosen is because this is the testing method used within the Defects4j repository to assess the number of defects.
Projects:
Chart: This is a Java library that can be used to create charts and graphs, and is important for data visualization applications.
Collections: Apache Common Collections is a library that adds new advanced data structures to the Java Collections framework such as Bag and Trie.
Compress: Compress is a library that can be used to handle many different compression formats like ZIP, GZIP, TAR, etc.
Lang:This Java library provides improved functions to Java functionality such as String manipulation, mathematical functions, etc.
Metrics:
The metrics we will be collecting are defects and LCOM. Defects will be measured directly be Defects4j by seeing how many test cases fail in the test suite. LCOM will be measured by sci-understand.
 5. Experimental Procedure

 5.1 Setting up the Environment

1. Infrastructure Setup:
   - Install required dependencies (Java 11, Perl modules, SVN)
   - Install SciTools Understand (sci-understand)

2. Project Configuration:
  - Initialize Defects4J repository
  - Checkout selected projects (Chart, Collections, Compress, Lang)
  - Configure sci-understand project settings for each project:
Source and binary paths configuration
Test exclusion patterns
Cohesion metric extraction settings
Project-specific settings	 

3. SciTools Understand Configuration:
   - Set up analysis parameters focusing on cohesion metrics
   - Configure LCOM metric extraction
   - Create analysis scripts for batch processing
   - Set up export formats for metric data
 5.2 Data Collection and Recording

1. Metric Collection:
 - Use defects4j CLI + sci-understand to extract LCOM values for each file
   - Calculate bug distribution across cohesion categories
   - Extract cohesion metrics using sci-understand
   - Collect function counts and method information

2. Data Organization:
   - Categorize files by cohesion levels:
 High cohesion (LCOM 0-2): Well-organized code where methods work closely together
 Medium cohesion (LCOM 3-5): Moderately organized code with some method relationships
 Low cohesion (LCOM >5): Code where methods are loosely related or unrelated
   - Record bug distribution:
 	* Track number of bugs in each cohesion category
 	* Calculate bug density per category
 	* Identify patterns in bug distribution
   - Calculate metrics:
 Average LCOM per category
 Overall project LCOM
 Correlation between LCOM and bug counts

 6. Risks and Mitigation

 6.1 Technical Risks

1. SciTools Understand Analysis Failures
   - Risk: Analysis may fail due to project structure or compatibility issues
   - Mitigation:
 Validate project structure before analysis
 Use specific SciTools Understand version
 Maintain proper Java version compatibility
 Document successful configuration patterns

2. Metric Calculation Accuracy
   - Risk: LCOM calculation might not perfectly reflect actual code cohesion
   - Mitigation:
 Use multiple supporting metrics (complexity, functions)
 Validate calculations against manual code review
 Document calculation assumptions
 Consider alternative cohesion metrics

3. Data Collection Completeness
   - Risk: Missing or incomplete metrics for some files
   - Mitigation:
Implement validation checks
Log files with missing data
 Use fallback calculation methods
 Monitor analysis coverage

 6.2 Process Risks

1.  Environment Consistency
   - Risk: Different results across different machines
   - Mitigation:
 Use Docker for consistent environment
 Document exact versions of all tools
 Provide detailed setup instructions
 Validate results across different setups

2. Project Compatibility
   - Risk: Some projects may not be analyzable
   - Mitigation:
 Pre-validate project structure
 Maintain list of compatible projects
 Document project-specific requirements
 Have backup projects available

 6.3 Data Quality Risks

1. False Positives in Bug Detection
   - Risk: Static analysis may report false bugs
   - Mitigation:
 Cross-validate with Defects4J known bugs

2. Statistical Significance
   - Risk: Insufficient data points in some categories
   - Mitigation:
 Ensure minimum sample sizes
 Use appropriate statistical tests
 Document data limitations
