import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

def analyze_class_cohesion(csv_file='charts.csv'):
    # 1. Read the CSV file
    print(f"Reading CSV file: {csv_file}...")
    df = pd.read_csv(csv_file)
    
    # Extract project name from CSV filename
    project_name = os.path.splitext(os.path.basename(csv_file))[0].capitalize()
    project_dir = project_name.lower()
    
    # Create graph and output directories
    graphs_dir = 'graphs'
    project_graphs_dir = os.path.join(graphs_dir, project_dir)
    
    
    # Create the directories if they don't exist
    os.makedirs(project_graphs_dir, exist_ok=True)
    
    
    classes_df = df.copy()
    #filter  rows with test  in the name
    classes_df = classes_df[~classes_df['Name'].str.contains('test', case=False)]
    #filter rows with public interface in the kind column
    classes_df = classes_df[~classes_df['Kind'].str.contains('public interface', case=False)]
  
    # Check if the DataFrame is empty
    if classes_df.empty:
        print("No classes found in the CSV file.")
        return None, project_graphs_dir
    
    # Check for LCOM columns
    required_columns = ['PercentLackOfCohesion', 'PercentLackOfCohesionModified']
    missing_columns = [col for col in required_columns if col not in classes_df.columns]
    
    if missing_columns:
        print(f"\nERROR: Missing required columns: {missing_columns}")
        return None, project_graphs_dir
    
    print("\nAnalyzing both LCOM metrics:")
    print("- PercentLackOfCohesion (LCOM)")
    print("- PercentLackOfCohesionModified (LCOM*)")
    
    # Check for missing values in both columns
    for col in required_columns:
        missing_count = classes_df[col].isna().sum()
        total_count = len(classes_df)
        print(f"\nMissing values in {col}: {missing_count} out of {total_count} classes ({(missing_count/total_count*100):.1f}%)")
    
    # Print sample of LCOM values
    print("\nSample of LCOM values (first 10 rows):")
    sample_df = classes_df[['Kind', 'Name', 'PercentLackOfCohesion', 'PercentLackOfCohesionModified']].head(10)
    print(sample_df)
    
    


    
    # Use the PercentLackOfCohesion column for primary LCOM analysis
    classes_df['LCOM'] = classes_df['PercentLackOfCohesion']
    
    # Calculate LCOM statistics
    lcom_stats = classes_df['LCOM'].describe()
    print("\nLCOM Statistics:")
    print(lcom_stats)
    
    # Categorize classes by cohesion level
    # LCOM interpretation for class-level analysis:
    # 0-25: High cohesion
    # 25-50: Medium cohesion
    # 50-75: Low cohesion
    # >75: Very low cohesion
    classes_df['CohesionLevel'] = pd.cut(
        classes_df['LCOM'],
        bins=[-float('inf'), 25, 50, 75, float('inf')],
        labels=['High', 'Medium', 'Low', 'Very Low']
    )
    
    # Calculate percentage distribution
    cohesion_counts = classes_df['CohesionLevel'].value_counts()
    cohesion_percentages = (cohesion_counts / len(classes_df) * 100).round(1)
    
    print("\nCohesion Level Distribution:")
    for level in ['High', 'Medium', 'Low', 'Very Low']:
        count = cohesion_counts.get(level, 0)
        percentage = cohesion_percentages.get(level, 0)
        print(f"{level} Cohesion: {count} classes ({percentage}%)")
    
    # Print summary statistics for each cohesion level
    print("\nLCOM Statistics by Cohesion Level:")
    for level in ['High', 'Medium', 'Low', 'Very Low']:
        level_stats = classes_df[classes_df['CohesionLevel'] == level]['LCOM'].describe()
        print(f"\n{level} Cohesion:")
        print(f"  Count: {level_stats['count']}")
        print(f"  Mean LCOM: {level_stats['mean']:.2f}")
        print(f"  Min LCOM: {level_stats['min']:.2f}")
        print(f"  Max LCOM: {level_stats['max']:.2f}")
    
    # Create visualizations
    
    # 1. LCOM Distribution Histogram - Compare both metrics
    plt.figure(figsize=(15, 7))
    
    # Create a subplot for the original LCOM
    plt.subplot(1, 2, 1)
    plt.hist(classes_df['PercentLackOfCohesion'].dropna(), bins=50, edgecolor='black', alpha=0.7, color='blue')
    plt.axvline(x=25, color='g', linestyle='--', label='High (25)')
    plt.axvline(x=50, color='y', linestyle='--', label='Medium (50)')
    plt.axvline(x=75, color='r', linestyle='--', label='Low (75)')
    plt.xlabel('Lack of Cohesion (LCOM)')
    plt.ylabel('Number of Classes')
    plt.title('LCOM Distribution')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Create a subplot for the modified LCOM
    plt.subplot(1, 2, 2)
    plt.hist(classes_df['PercentLackOfCohesionModified'].dropna(), bins=50, edgecolor='black', alpha=0.7, color='green')
    plt.axvline(x=25, color='g', linestyle='--', label='High (25)')
    plt.axvline(x=50, color='y', linestyle='--', label='Medium (50)')
    plt.axvline(x=75, color='r', linestyle='--', label='Low (75)')
    plt.xlabel('Lack of Cohesion Modified (LCOM*)')
    plt.ylabel('Number of Classes')
    plt.title('LCOM* Distribution')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.suptitle(f'Distribution of Class Cohesion - {project_name} Project\n(Lower LCOM = Higher Cohesion)', fontsize=14)
    plt.tight_layout()
    plt.legend()
    plt.grid(True, alpha=0.3)
    distribution_path = os.path.join(project_graphs_dir, 'cohesion_distribution.png')
    plt.savefig(distribution_path, bbox_inches='tight', dpi=300)
    plt.close()
    
    # 2. Cohesion Level Bar Plot
    plt.figure(figsize=(10, 6))
    colors = ['green', 'yellow', 'orange', 'red']
    ax = cohesion_counts.plot(kind='bar', color=colors)
    plt.xlabel('Cohesion Level')
    plt.ylabel('Number of Classes')
    plt.title(f'Classes by Cohesion Level - {project_name} Project\n(Higher is Better)')
    
    # Add percentage labels on top of each bar
    for i, (count, percentage) in enumerate(zip(cohesion_counts, cohesion_percentages)):
        ax.text(i, count, f'{percentage}%', ha='center', va='bottom')
    
    plt.grid(True, axis='y', alpha=0.3)
    plt.tight_layout()
    levels_path = os.path.join(project_graphs_dir, 'cohesion_levels.png')
    plt.savefig(levels_path, bbox_inches='tight', dpi=300)
    plt.close()
    
    # Save detailed results
    csv_path = os.path.join(project_graphs_dir, 'class_cohesion_analysis.csv')
    classes_df.to_csv(csv_path, index=False)
    
    return classes_df, project_graphs_dir

if __name__ == "__main__":
    # Modify this to process a specific CSV file
    csv_file = 'Collections.csv'  
    result_df, output_dir = analyze_class_cohesion(csv_file)
    
    project_name = os.path.splitext(os.path.basename(csv_file))[0].capitalize()
    print("\nAnalysis complete. Results saved to:")
    print(f"- {output_dir}/cohesion_distribution.png (LCOM distribution)")
    print(f"- {output_dir}/cohesion_levels.png (cohesion level counts)")
    print(f"- {output_dir}/class_cohesion_analysis.csv (detailed results)")
