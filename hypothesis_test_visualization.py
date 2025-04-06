import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from scipy import stats


os.makedirs('graphs/results', exist_ok=True)


projects = {
    'Chart': {'name': 'jfreechart', 'defects': 26, 'csv': 'Charts.csv'},
    'Collections': {'name': 'commons-collections', 'defects': 28, 'csv': 'Collections.csv'},
    'Compress': {'name': 'commons-compress', 'defects': 47, 'csv': 'compress.csv'},
    'Lang': {'name': 'commons-lang', 'defects': 61, 'csv': 'Lang.csv'}
}


if os.path.exists('graphs/results/lcom_defects_summary.csv'):
    summary_df = pd.read_csv('graphs/results/lcom_defects_summary.csv')
    print("Loaded summary data from graphs/results/lcom_defects_summary.csv")
else:
    print("Summary data file not found. Please run analyze_lcom_defects.py first.")
    exit(1)


alpha = 0.05


slope, intercept, r_value, p_value, std_err = stats.linregress(summary_df['Avg LCOM'], summary_df['Defects'])


plt.figure(figsize=(12, 8))


scatter = plt.scatter(summary_df['Avg LCOM'], summary_df['Defects'], s=150, alpha=0.7, 
                     c=summary_df['Defect Density'], cmap='viridis', 
                     edgecolors='black', linewidths=1)

for i, row in summary_df.iterrows():
    plt.annotate(row['Project'], 
                 (row['Avg LCOM'], row['Defects']),
                 xytext=(7, 7),
                 textcoords='offset points',
                 fontsize=12,
                 fontweight='bold')

x_range = np.linspace(summary_df['Avg LCOM'].min() - 5, summary_df['Avg LCOM'].max() + 5, 100)
plt.plot(x_range, intercept + slope * x_range, 'r--', linewidth=2, 
         label=f'Regression line: y = {slope:.2f}x + {intercept:.2f}')


n = len(summary_df)
x_mean = summary_df['Avg LCOM'].mean()
t_val = stats.t.ppf(1 - alpha/2, n-2)
s_err = np.sqrt(np.sum((summary_df['Defects'] - (intercept + slope * summary_df['Avg LCOM']))**2) / (n-2))
s_x = np.sqrt(np.sum((summary_df['Avg LCOM'] - x_mean)**2))


se = s_err * np.sqrt(1/n + (x_range - x_mean)**2 / s_x**2)
plt.fill_between(x_range, 
                 intercept + slope * x_range - t_val * se,
                 intercept + slope * x_range + t_val * se,
                 alpha=0.2, color='r', label='95% Confidence Interval')

cbar = plt.colorbar(scatter)
cbar.set_label('Defect Density (Defects per Class)', fontsize=12)

stats_text = (
    f"Hypothesis Testing Results:\n"
    f"Null Hypothesis (H₀): No relationship between LCOM and defects\n"
    f"Alternative Hypothesis (H₁): Higher LCOM leads to more defects\n\n"
    f"Significance Level (α): {alpha:.2f}\n"
    f"p-value: {p_value:.4f}\n"
    f"R-squared: {r_value**2:.2f}\n\n"
    f"{'Reject H₀' if p_value < alpha else 'Fail to reject H₀'}"
)

plt.figtext(0.65, 0.01, stats_text, fontsize=9, 
            bbox=dict(facecolor='white', alpha=0.8, boxstyle='round,pad=0.5'))


plt.title('Hypothesis Test: Relationship Between Code Cohesion (LCOM) and Defects', fontsize=16)
plt.xlabel('Average LCOM (Higher = Lower Cohesion)', fontsize=14)
plt.ylabel('Number of Defects', fontsize=14)
plt.grid(True, alpha=0.3)
plt.legend(loc='upper right')


plt.tight_layout(rect=[0, 0.1, 1, 0.95]) 
plt.savefig('graphs/results/hypothesis_test_visualization.png', dpi=300, bbox_inches='tight')
print("Saved hypothesis test visualization to graphs/results/hypothesis_test_visualization.png")

print("\nHypothesis Test Results:")
print(f"Null Hypothesis (H₀): No significant relationship between code cohesion (LCOM) and defect counts")
print(f"Alternative Hypothesis (H₁): Codebases with lower cohesion (higher LCOM) tend to have higher defect counts")
print(f"Significance Level (α): {alpha:.2f}")
print(f"p-value: {p_value:.4f}")
print(f"R-squared: {r_value**2:.2f}")
print(f"Conclusion: {'Reject H₀' if p_value < alpha else 'Fail to reject H₀'}")
print(f"Interpretation: {'There is a statistically significant relationship between LCOM and defects' if p_value < alpha else 'There is not enough evidence to conclude a significant relationship between LCOM and defects'}")
