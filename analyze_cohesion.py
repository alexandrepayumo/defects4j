import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def analyze_method_cohesion():
    # 1. Read the CSV file
    print("Reading CSV file...")
    df = pd.read_csv('chart.csv')
    
    # 2. Filter to only look at methods and extract LCOM from third-last column
    methods_df = df[df['Kind'].str.contains('Method', na=False)].copy()
    methods_df['LCOM'] = methods_df.iloc[:, -3]  # Get third-last column
    
    # 3. Look at LCOM distribution
    print("\nLCOM Analysis for Methods:")
    print(f"Total number of methods analyzed: {len(methods_df)}")
    
    # Calculate LCOM statistics
    lcom_stats = methods_df['LCOM'].describe()
    print("\nLCOM Statistics:")
    print(lcom_stats)
    
    # Categorize methods by cohesion level
    # LCOM interpretation:
    # 0.0-0.3: High cohesion
    # 0.3-0.7: Medium cohesion
    # 0.7-1.0: Low cohesion
    # >1.0: Very low cohesion
    methods_df['CohesionLevel'] = pd.cut(
        methods_df['LCOM'],
        bins=[-float('inf'), 0.3, 0.7, 1.0, float('inf')],
        labels=['High', 'Medium', 'Low', 'Very Low']
    )
    
    # Calculate percentage distribution
    cohesion_counts = methods_df['CohesionLevel'].value_counts()
    cohesion_percentages = (cohesion_counts / len(methods_df) * 100).round(1)
    
    print("\nCohesion Level Distribution:")
    for level in ['High', 'Medium', 'Low', 'Very Low']:
        count = cohesion_counts.get(level, 0)
        percentage = cohesion_percentages.get(level, 0)
        print(f"{level} Cohesion: {count} methods ({percentage}%)")
    
    # Print summary statistics for each cohesion level
    print("\nLCOM Statistics by Cohesion Level:")
    for level in ['High', 'Medium', 'Low', 'Very Low']:
        level_stats = methods_df[methods_df['CohesionLevel'] == level]['LCOM'].describe()
        print(f"\n{level} Cohesion:")
        print(f"  Count: {level_stats['count']}")
        print(f"  Mean LCOM: {level_stats['mean']:.2f}")
        print(f"  Min LCOM: {level_stats['min']:.2f}")
        print(f"  Max LCOM: {level_stats['max']:.2f}")
    
    # Create visualizations
    
    # 1. LCOM Distribution Histogram
    plt.figure(figsize=(12, 6))
    plt.hist(methods_df['LCOM'].dropna(), bins=50, edgecolor='black', alpha=0.7)
    plt.axvline(x=0.3, color='g', linestyle='--', label='High Cohesion Threshold (0.3)')
    plt.axvline(x=0.7, color='y', linestyle='--', label='Medium Cohesion Threshold (0.7)')
    plt.axvline(x=1.0, color='r', linestyle='--', label='Low Cohesion Threshold (1.0)')
    plt.xlabel('Lack of Cohesion (LCOM)')
    plt.ylabel('Number of Methods')
    plt.title('Distribution of Method Cohesion\n(Lower LCOM = Higher Cohesion)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('cohesion_distribution.png', bbox_inches='tight', dpi=300)
    plt.close()
    
    # 2. Cohesion Level Bar Plot
    plt.figure(figsize=(10, 6))
    colors = ['green', 'yellow', 'orange', 'red']
    ax = cohesion_counts.plot(kind='bar', color=colors)
    plt.xlabel('Cohesion Level')
    plt.ylabel('Number of Methods')
    plt.title('Methods by Cohesion Level\n(Higher is Better)')
    
    # Add percentage labels on top of each bar
    for i, (count, percentage) in enumerate(zip(cohesion_counts, cohesion_percentages)):
        ax.text(i, count, f'{percentage}%', ha='center', va='bottom')
    
    plt.grid(True, axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig('cohesion_levels.png', bbox_inches='tight', dpi=300)
    plt.close()
    
    # Save detailed results
    methods_df.to_csv('method_cohesion_analysis.csv', index=False)
    
    return methods_df

if __name__ == "__main__":
    result_df = analyze_method_cohesion()
    print("\nAnalysis complete. Results saved to:")
    print("- cohesion_distribution.png (LCOM distribution)")
    print("- cohesion_levels.png (cohesion level counts)")
    print("- method_cohesion_analysis.csv (detailed results)")
