import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from scipy import stats
# Create graphs directory if it doesn't exist
os.makedirs('graphs/results', exist_ok=True)

# Project data
projects = {
    'Chart': {'name': 'jfreechart', 'defects': 26, 'csv': 'Charts.csv'},
    'Collections': {'name': 'commons-collections', 'defects': 28, 'csv': 'Collections.csv'},
    'Compress': {'name': 'commons-compress', 'defects': 47, 'csv': 'compress.csv'},
    'Lang': {'name': 'commons-lang', 'defects': 61, 'csv': 'Lang.csv'}
}

# Function to load and process data for a project
def load_project_data(project_info):
    csv_file = project_info['csv']
    print(f"Reading CSV file: {csv_file}...")
    
    try:
        df = pd.read_csv(csv_file)
        
        # Filter out test classes and interfaces
        df = df[~df['Name'].str.contains('test', case=False)]
        if 'Kind' in df.columns:
            df = df[~df['Kind'].str.contains('public interface', case=False)]
        
        # Check if LCOM columns exist
        if 'PercentLackOfCohesion' not in df.columns:
            print(f"Error: PercentLackOfCohesion column not found in {csv_file}")
            return None
        
        # Use PercentLackOfCohesion as LCOM
        df['LCOM'] = df['PercentLackOfCohesion']
        
        # Categorize classes by cohesion level
        df['CohesionLevel'] = pd.cut(
            df['LCOM'],
            bins=[-float('inf'), 25, 50, 75, float('inf')],
            labels=['High', 'Medium', 'Low', 'Very Low']
        )
        
        return df
    except Exception as e:
        print(f"Error loading {csv_file}: {e}")
        return None

# Load data for all projects
project_data = {}
for project, info in projects.items():
    df = load_project_data(info)
    if df is not None:
        project_data[project] = df

# Calculate summary statistics for each project
summary_data = []
for project, info in projects.items():
    if project in project_data:
        df = project_data[project]
        
        # Calculate statistics
        avg_lcom = df['LCOM'].mean()
        median_lcom = df['LCOM'].median()
        min_lcom = df['LCOM'].min()
        max_lcom = df['LCOM'].max()
        
        # Count classes in each cohesion level
        cohesion_counts = df['CohesionLevel'].value_counts()
        high_cohesion = cohesion_counts.get('High', 0)
        medium_cohesion = cohesion_counts.get('Medium', 0)
        low_cohesion = cohesion_counts.get('Low', 0)
        very_low_cohesion = cohesion_counts.get('Very Low', 0)
        
        # Calculate percentages
        total_classes = len(df)
        high_cohesion_pct = (high_cohesion / total_classes) * 100 if total_classes > 0 else 0
        medium_cohesion_pct = (medium_cohesion / total_classes) * 100 if total_classes > 0 else 0
        low_cohesion_pct = (low_cohesion / total_classes) * 100 if total_classes > 0 else 0
        very_low_cohesion_pct = (very_low_cohesion / total_classes) * 100 if total_classes > 0 else 0
        
        # Calculate defect density (defects per class)
        defect_density = info['defects'] / total_classes if total_classes > 0 else 0
        
        # Add to summary data
        summary_data.append({
            'Project': project,
            'Total Classes': total_classes,
            'Defects': info['defects'],
            'Avg LCOM': avg_lcom,
            'Median LCOM': median_lcom,
            'Min LCOM': min_lcom,
            'Max LCOM': max_lcom,
            'High Cohesion Classes': high_cohesion,
            'Medium Cohesion Classes': medium_cohesion,
            'Low Cohesion Classes': low_cohesion,
            'Very Low Cohesion Classes': very_low_cohesion,
            'High Cohesion %': high_cohesion_pct,
            'Medium Cohesion %': medium_cohesion_pct,
            'Low Cohesion %': low_cohesion_pct,
            'Very Low Cohesion %': very_low_cohesion_pct,
            'Defect Density': defect_density
        })

# Create summary DataFrame
summary_df = pd.DataFrame(summary_data)

# Save summary to CSV
summary_df.to_csv('graphs/results/lcom_defects_summary.csv', index=False)
print("Saved summary data to graphs/results/lcom_defects_summary.csv")

# Create visualizations

# 1. Scatter plot of Average LCOM vs Defect Count
plt.figure(figsize=(10, 6))
plt.scatter(summary_df['Avg LCOM'], summary_df['Defects'], s=100, alpha=0.7)

# Add project labels to points
for i, row in summary_df.iterrows():
    plt.annotate(row['Project'], 
                 (row['Avg LCOM'], row['Defects']),
                 xytext=(5, 5),
                 textcoords='offset points',
                 fontsize=12)

# Add trendline
z = np.polyfit(summary_df['Avg LCOM'], summary_df['Defects'], 1)
p = np.poly1d(z)
plt.plot(summary_df['Avg LCOM'], p(summary_df['Avg LCOM']), "r--", alpha=0.7)

# Calculate correlation coefficient
correlation = summary_df['Avg LCOM'].corr(summary_df['Defects'])
plt.title(f'Average LCOM vs Defect Count (Correlation: {correlation:.2f})', fontsize=14)
plt.xlabel('Average LCOM (Higher = Lower Cohesion)', fontsize=12)
plt.ylabel('Number of Defects', fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('graphs/results/lcom_vs_defects_scatter.png', dpi=300)
print("Saved scatter plot to graphs/results/lcom_vs_defects_scatter.png")

# 2. Bar chart of Defect Density vs Average LCOM
plt.figure(figsize=(10, 6))
bars = plt.bar(summary_df['Project'], summary_df['Defect Density'], alpha=0.7)

# Color bars based on average LCOM
norm = plt.Normalize(summary_df['Avg LCOM'].min(), summary_df['Avg LCOM'].max())
colors = plt.cm.viridis(norm(summary_df['Avg LCOM']))
for bar, color in zip(bars, colors):
    bar.set_color(color)

# Add LCOM values on top of bars
for i, row in summary_df.iterrows():
    plt.text(i, row['Defect Density'] + 0.01, f"LCOM: {row['Avg LCOM']:.1f}", 
             ha='center', va='bottom', fontsize=10)

plt.title('Defect Density by Project (colored by Avg LCOM)', fontsize=14)
plt.xlabel('Project', fontsize=12)
plt.ylabel('Defect Density (Defects per Class)', fontsize=12)
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('graphs/results/defect_density_by_project.png', dpi=300)
print("Saved defect density chart to graphs/results/defect_density_by_project.png")

# 3. Stacked bar chart of cohesion level distribution with defect overlay
plt.figure(figsize=(12, 7))

# Prepare data for stacked bars
cohesion_data = summary_df[['Project', 'High Cohesion %', 'Medium Cohesion %', 'Low Cohesion %', 'Very Low Cohesion %']]
cohesion_data = cohesion_data.set_index('Project')

# Create stacked bar chart
ax = cohesion_data.plot(kind='bar', stacked=True, figsize=(12, 7), 
                        color=['green', 'yellow', 'orange', 'red'], alpha=0.7)

# Add defect count as a line on secondary y-axis
ax2 = ax.twinx()
ax2.plot(ax.get_xticks(), summary_df['Defects'], 'bo-', linewidth=2, markersize=8)
ax2.set_ylabel('Number of Defects', fontsize=12, color='blue')
ax2.tick_params(axis='y', colors='blue')

# Set labels and title
ax.set_xlabel('Project', fontsize=12)
ax.set_ylabel('Percentage of Classes', fontsize=12)
ax.set_title('Cohesion Level Distribution vs Defect Count by Project', fontsize=14)
ax.legend(title='Cohesion Level', bbox_to_anchor=(1.15, 0.5), loc='center left')

# Add defect count labels
for i, defects in enumerate(summary_df['Defects']):
    ax2.annotate(f"{defects}", 
                 (i, defects),
                 xytext=(0, 5),
                 textcoords='offset points',
                 ha='center',
                 fontsize=10,
                 color='blue')

plt.tight_layout()
plt.savefig('graphs/results/cohesion_distribution_vs_defects.png', dpi=300)
print("Saved cohesion distribution chart to graphs/results/cohesion_distribution_vs_defects.png")

# 4. Correlation matrix heatmap
correlation_columns = ['Defects', 'Avg LCOM', 'High Cohesion %', 'Medium Cohesion %', 
                       'Low Cohesion %', 'Very Low Cohesion %', 'Defect Density']
correlation_matrix = summary_df[correlation_columns].corr()

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, center=0, 
            square=True, linewidths=.5, cbar_kws={"shrink": .8})
plt.title('Correlation Matrix: LCOM Metrics vs Defects', fontsize=14)
plt.tight_layout()
plt.savefig('graphs/results/correlation_matrix.png', dpi=300)
print("Saved correlation matrix to graphs/results/correlation_matrix.png")

# 5. Scatter plot matrix
plt.figure(figsize=(12, 10))
scatter_columns = ['Defects', 'Avg LCOM', 'High Cohesion %', 'Very Low Cohesion %', 'Defect Density']
scatter_df = summary_df[scatter_columns]
pd.plotting.scatter_matrix(scatter_df, alpha=0.8, figsize=(12, 10), diagonal='kde')
plt.tight_layout()
plt.savefig('graphs/results/scatter_matrix.png', dpi=300)
print("Saved scatter matrix to graphs/results/scatter_matrix.png")

# Print key findings
print("\n=== Key Findings ===")
print(f"Correlation between Avg LCOM and Defects: {correlation:.2f}")

# Calculate correlation between Very Low Cohesion % and Defects
very_low_corr = summary_df['Very Low Cohesion %'].corr(summary_df['Defects'])
print(f"Correlation between Very Low Cohesion % and Defects: {very_low_corr:.2f}")

# Calculate correlation between High Cohesion % and Defects
high_corr = summary_df['High Cohesion %'].corr(summary_df['Defects'])
print(f"Correlation between High Cohesion % and Defects: {high_corr:.2f}")

# Calculate correlation between Defect Density and Avg LCOM
density_corr = summary_df['Defect Density'].corr(summary_df['Avg LCOM'])
print(f"Correlation between Defect Density and Avg LCOM: {density_corr:.2f}")

# Sort projects by defect count
highest_defects = summary_df.sort_values('Defects', ascending=False).iloc[0]
print(f"\nProject with highest defect count: {highest_defects['Project']} ({highest_defects['Defects']} defects)")
print(f"Average LCOM: {highest_defects['Avg LCOM']:.2f}")
print(f"Very Low Cohesion Classes: {highest_defects['Very Low Cohesion %']:.2f}%")

# Sort projects by average LCOM
highest_lcom = summary_df.sort_values('Avg LCOM', ascending=False).iloc[0]
print(f"\nProject with highest average LCOM: {highest_lcom['Project']} ({highest_lcom['Avg LCOM']:.2f})")
print(f"Defect count: {highest_lcom['Defects']}")
print(f"Very Low Cohesion Classes: {highest_lcom['Very Low Cohesion %']:.2f}%")

# Calculate linear regression for prediction

slope, intercept, r_value, p_value, std_err = stats.linregress(summary_df['Avg LCOM'], summary_df['Defects'])
print(f"\nLinear Regression: Defects = {slope:.2f} * LCOM + {intercept:.2f}")
print(f"R-squared: {r_value**2:.2f}")
print(f"P-value: {p_value:.4f}")

print("\nAnalysis complete. All visualizations saved to graphs/results/ directory.")
