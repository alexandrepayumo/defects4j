package org.sonar.samples.java;

import java.util.*;
import org.sonar.api.Plugin;
import org.sonar.api.batch.fs.FileSystem;
import org.sonar.api.batch.fs.InputFile;
import org.sonar.api.batch.sensor.Sensor;
import org.sonar.api.batch.sensor.SensorContext;
import org.sonar.api.batch.sensor.SensorDescriptor;
import org.sonar.api.measures.CoreMetrics;
import org.sonar.api.measures.Metric;
import org.sonar.api.measures.Metrics;
import org.sonar.plugins.java.api.JavaFileScanner;
import org.sonar.plugins.java.api.JavaFileScannerContext;
import org.sonar.plugins.java.api.tree.*;
import org.slf4j.Logger;
    public static final Metric<Integer> LCOM4 = new Metric.Builder("lcom4", "LCOM4", Metric.ValueType.INT)
        .setDescription("Lack of Cohesion of Methods v4")
        .setDirection(Metric.DIRECTION.WORST)
        .setQualitative(true)
        .setDomain(CoreMetrics.DOMAIN_COMPLEXITY)
        .create();

    public static final Metric<Double> TCC = new Metric.Builder("tcc", "Tight Class Cohesion", Metric.ValueType.FLOAT)
        .setDescription("Tight Class Cohesion metric")
        .setDirection(Metric.DIRECTION.BETTER)
        .setQualitative(true)
        .setDomain(CoreMetrics.DOMAIN_COMPLEXITY)
        .create();

    @Override
    public List<Metric> getMetrics() {
        return Arrays.asList(LCOM4, TCC);
    }
}

class CohesionSensor extends JavaAstScanner {
    private final FileSystem fs;
    private final SensorContext context;

    @Override
    public void analyze(Project project, SensorContext context) {
        for (InputFile inputFile : fs.inputFiles(fs.predicates().hasLanguage("java"))) {
            analyzeFile(inputFile);
        }
    }

    private void analyzeFile(InputFile inputFile) {
        try {
            CompilationUnitTree tree = (CompilationUnitTree) parser.parse(inputFile.contents());
            ClassVisitor visitor = new ClassVisitor();
            tree.accept(visitor);
            
            // Calculate LCOM4
            int lcom4 = calculateLCOM4(visitor.getMethods(), visitor.getFieldAccesses());
            context.newMeasure().forMetric(CohesionMetrics.LCOM4).on(inputFile).withValue(lcom4).save();
            
            // Calculate TCC
            double tcc = calculateTCC(visitor.getMethods(), visitor.getFieldAccesses());
            context.newMeasure().forMetric(CohesionMetrics.TCC).on(inputFile).withValue(tcc).save();
        } catch (Exception e) {
            LOG.error("Could not analyze file " + inputFile.filename(), e);
        }
    }

    private int calculateLCOM4(List<MethodTree> methods, Map<String, Set<String>> fieldAccesses) {
        // LCOM4 = number of connected groups of methods sharing instance variable access
        DisjointSet<MethodTree> methodGroups = new DisjointSet<>();
        
        // Initialize each method in its own set
        methods.forEach(methodGroups::makeSet);
        
        // Connect methods that share instance variables
        for (MethodTree m1 : methods) {
            String m1Name = m1.simpleName().toString();
            Set<String> m1Fields = fieldAccesses.get(m1Name);
            
            for (MethodTree m2 : methods) {
                String m2Name = m2.simpleName().toString();
                Set<String> m2Fields = fieldAccesses.get(m2Name);
                
                // If methods share any fields, union their sets
                if (!Collections.disjoint(m1Fields, m2Fields)) {
                    methodGroups.union(m1, m2);
                }
            }
        }
        
        // LCOM4 is the number of disjoint sets
        return methodGroups.getNumberOfSets();
    }

    private double calculateTCC(List<MethodTree> methods, Map<String, Set<String>> fieldAccesses) {
        // TCC = NDC/NP where
        // NDC = number of directly connected method pairs
        // NP = N*(N-1)/2, N = number of visible methods
        
        int n = methods.size();
        if (n <= 1) return 1.0; // Perfect cohesion for 0 or 1 method
        
        int maxPairs = (n * (n-1)) / 2;
        int connectedPairs = 0;
        
        for (int i = 0; i < methods.size(); i++) {
            String m1Name = methods.get(i).simpleName().toString();
            Set<String> m1Fields = fieldAccesses.get(m1Name);
            
            for (int j = i+1; j < methods.size(); j++) {
                String m2Name = methods.get(j).simpleName().toString();
                Set<String> m2Fields = fieldAccesses.get(m2Name);
                
                if (!Collections.disjoint(m1Fields, m2Fields)) {
                    connectedPairs++;
                }
            }
        }
        
        return (double)connectedPairs / maxPairs;
    }
}

class ClassVisitor extends BaseTreeVisitor {
    private List<MethodTree> methods = new ArrayList<>();
    private Map<String, Set<String>> fieldAccesses = new HashMap<>();
    
    @Override
    public void visitMethod(MethodTree tree) {
        methods.add(tree);
        String methodName = tree.simpleName().toString();
        fieldAccesses.put(methodName, new HashSet<>());
        
        // Visit method body to collect field accesses
        FieldAccessVisitor fieldVisitor = new FieldAccessVisitor(methodName);
        tree.accept(fieldVisitor);
        
        super.visitMethod(tree);
    }
    
    public List<MethodTree> getMethods() {
        return methods;
    }
    
    public Map<String, Set<String>> getFieldAccesses() {
        return fieldAccesses;
    }
}

class FieldAccessVisitor extends BaseTreeVisitor {
    private final String methodName;
    private final Set<String> accessedFields;
    
    public FieldAccessVisitor(String methodName) {
        this.methodName = methodName;
        this.accessedFields = new HashSet<>();
    }
    
    @Override
    public void visitMemberSelectExpression(MemberSelectExpressionTree tree) {
        if (tree.expression().is(Tree.Kind.IDENTIFIER)) {
            String fieldName = ((IdentifierTree)tree.expression()).name();
            accessedFields.add(fieldName);
        }
        super.visitMemberSelectExpression(tree);
    }
}
