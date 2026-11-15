"""
Quick analysis script for Egyptian Arabic dataset
"""
import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv('data/arabic_transactions_clean.csv')

# Calculate description lengths
df['desc_len'] = df['transaction_description'].str.len()

# Create visualizations
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Length distribution
df['desc_len'].hist(bins=20, ax=axes[0], color='skyblue', edgecolor='black')
axes[0].set_title('Transaction Description Length Distribution', fontsize=12, fontweight='bold')
axes[0].set_xlabel('Characters')
axes[0].set_ylabel('Frequency')
axes[0].grid(alpha=0.3)

# Category distribution
top_cats = df['category'].value_counts()
top_cats.plot(kind='barh', ax=axes[1], color='lightcoral')
axes[1].set_title('Category Distribution (All 10 Categories)', fontsize=12, fontweight='bold')
axes[1].set_xlabel('Count')
axes[1].grid(alpha=0.3, axis='x')

plt.tight_layout()
plt.savefig('reports/egyptian_dataset_analysis.png', dpi=150, bbox_inches='tight')
print('✅ Analysis chart saved: reports/egyptian_dataset_analysis.png')

# Print summary statistics
print('\n' + '='*60)
print('EGYPTIAN DATASET SUMMARY')
print('='*60)
print(f'Total records: {len(df):,}')
print(f'Unique descriptions: {df["transaction_description"].nunique():,}')
print(f'Duplication rate: {(1 - df["transaction_description"].nunique()/len(df))*100:.1f}%')
print(f'Average length: {df["desc_len"].mean():.1f} characters')
print(f'Min length: {df["desc_len"].min()} characters')
print(f'Max length: {df["desc_len"].max()} characters')
print(f'Categories: {df["category"].nunique()}')
print('\nCategory breakdown:')
for cat, count in df['category'].value_counts().items():
    pct = (count / len(df)) * 100
    print(f'  {cat:30s}: {count:5,} ({pct:5.1f}%)')
print('='*60)

# Sample transactions from each category
print('\n' + '='*60)
print('SAMPLE TRANSACTIONS (3 per category)')
print('='*60)
for cat in sorted(df['category'].unique()):
    print(f'\n{cat}:')
    samples = df[df['category'] == cat]['transaction_description'].sample(min(3, len(df[df['category'] == cat])), random_state=42)
    for i, desc in enumerate(samples, 1):
        print(f'  {i}. {desc}')
print('='*60)
