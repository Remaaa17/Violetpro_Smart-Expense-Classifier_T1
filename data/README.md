# Dataset Directory

This directory contains all transaction datasets used for the Smart Expense Classifier project.

## 📁 Files Overview

### Hugging Face Datasets
- **`huggingface_full_dataset.csv`** (4,501,043 records) - Full HF dataset
- **`huggingface_sample_10k.csv`** (10,000 records) - HF sample

### Egyptian Arabic Dataset (Primary Dataset) ⭐
- **`arabic_transactions_clean.csv`** ⭐ **Main Dataset** (10,000 records)
  - Country: Egypt (fixed)
  - Currency: EGP (fixed)
  - Categories: 10
  - Languages: 5 styles (MSA, Egyptian colloquial, mixed, Arabizi, English)
  - Quality: 55% clean, 45% realistic imperfections

- **`arabic_transactions_clean.parquet`** - Parquet format (faster loading)

### Pre-Split Training Sets
- **`arabic_transactions_train.csv`** (2,788 records - 70%)
- **`arabic_transactions_validation.csv`** (597 records - 15%)
- **`arabic_transactions_test.csv`** (599 records - 15%)

### Label Noise Experiments
- **`arabic_transactions_noisy_2pct.csv`** - Training data with 2% corrupted labels (55 errors)
- **`arabic_transactions_noisy_5pct.csv`** - Training data with 5% corrupted labels (139 errors)

## 🎯 Recommended Usage

### For Model Training
```python
import pandas as pd

# Option 1: Use pre-split data
train = pd.read_csv('data/arabic_transactions_train.csv')
val = pd.read_csv('data/arabic_transactions_validation.csv')
test = pd.read_csv('data/arabic_transactions_test.csv')

# Option 2: Load full dataset and split yourself
df = pd.read_csv('data/arabic_transactions_clean.csv')
# ... custom split logic
```

### For Robustness Testing
```python
# Train on noisy data, test on clean data
train_noisy = pd.read_csv('data/arabic_transactions_noisy_5pct.csv')
test_clean = pd.read_csv('data/arabic_transactions_test.csv')
```

### For Large-Scale Experiments
```python
# Use Hugging Face full dataset
df_large = pd.read_csv('data/huggingface_full_dataset.csv')
# Warning: 4.5M records, may require significant RAM
```

## 📊 Schema

All datasets follow this structure:

| Column | Type | Description |
|--------|------|-------------|
| `transaction_description` | string | Transaction text in various languages |
| `category` | string | One of 10 predefined categories |
| `country` | string | Country code (Egypt for Egyptian dataset) |
| `currency` | string | Currency code (EGP for Egyptian dataset) |

## 🗂️ Subdirectories

- **`raw/`** - Raw, unprocessed data (if any)
- **`processed/`** - Preprocessed/transformed datasets

## 📈 Statistics

### Egyptian Dataset Quality
- **Total Records:** 10,000
- **Unique Descriptions:** 3,984 (40%)
- **Average Length:** 17.9 characters
- **Categories:** 10 (balanced distribution)
- **Missing Values:** 0%

### Category Distribution
1. Food & Dining: 1,780 (17.8%)
2. Transportation: 1,545 (15.4%)
3. Shopping & Retail: 1,387 (13.9%)
4. Utilities & Services: 1,183 (11.8%)
5. Entertainment & Recreation: 1,169 (11.7%)
6. Healthcare & Medical: 870 (8.7%)
7. Financial Services: 788 (7.9%)
8. Income: 490 (4.9%)
9. Charity & Donations: 407 (4.1%)
10. Government & Legal: 381 (3.8%)

## 🔍 Data Quality

The Egyptian dataset includes controlled imperfections:
- 55% clean/perfect text
- 15% spelling errors
- 15% mixed language artifacts
- 10% ambiguous categories
- 5% incomplete descriptions

This distribution reflects real-world transaction data quality.

## 🚀 Quick Start

```python
# Load and explore
import pandas as pd

df = pd.read_csv('data/arabic_transactions_clean.csv')

print(f"Records: {len(df):,}")
print(f"Categories: {df['category'].nunique()}")
print(f"\nSample:\n{df.sample(5)}")
print(f"\nCategory counts:\n{df['category'].value_counts()}")
```

## 📚 Documentation

For detailed information about the Egyptian dataset:
- See **`../EGYPTIAN_DATASET_DETAILS.md`** for comprehensive documentation
- Run **`../analyze_egyptian_dataset.py`** for analysis and visualizations
- Check **`../reports/data_quality_summary.txt`** for quality metrics

## ⚠️ Important Notes

1. **Random Seed:** All datasets use `random_state=42` for reproducibility
2. **Encoding:** UTF-8 encoding for Arabic text
3. **Splits:** Pre-split files use stratified sampling (maintains category balance)
4. **Noise:** Label noise is applied only to training data, never test/validation

## 🎓 Citation

If using the Egyptian dataset in research:
```
Egyptian Arabic Financial Transaction Dataset (2026)
Smart Expense Classifier Project - VioletPro Internship
10,000 synthetic transactions with linguistic variations
Random Seed: 42
```

---

**Last Updated:** November 12, 2026  
**Maintained By:** Smart Expense Classifier Team
