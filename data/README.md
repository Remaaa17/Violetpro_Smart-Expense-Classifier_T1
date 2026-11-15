# Dataset Directory

This directory contains all transaction datasets for the Smart Expense Classifier project.

**Structure**:
- `raw/` - Original, unprocessed datasets
- `processed/` - Preprocessed and split datasets (train/val/test)

---

##  Folder Structure

```
data/
 raw/                          # Original datasets
    huggingface_full_dataset.csv
    huggingface_sample_10k.csv
    arabic_only_transactions.csv
    arabic_only_transactions.parquet
    arabic_transactions_clean.csv
    arabic_transactions_clean.parquet

 processed/                    # Preprocessed & split datasets
    arabic_only_train.csv
    arabic_only_validation.csv
    arabic_only_test.csv
    arabic_transactions_train.csv
    arabic_transactions_validation.csv
    arabic_transactions_test.csv
    arabic_transactions_noisy_2pct.csv
    arabic_transactions_noisy_5pct.csv

 README.md                     # This file
```

---

##  RAW Datasets (`data/raw/`)

### 1. `huggingface_full_dataset.csv`

**Size**: 4,501,043 records (211 MB)  
**Source**: [Hugging Face - mitulshah/transaction-categorization](https://huggingface.co/datasets/mitulshah/transaction-categorization)  
**Purpose**: Full production dataset for maximum accuracy  

**Description**:
- Real-world transaction data
- Global coverage (multiple countries & currencies)
- 10 expense/income categories
- Balanced distribution

**Columns**:
- `transaction_description` - Transaction text
- `category` - Expense category
- `country` - Country code
- `currency` - Currency code

**Statistics**:
- Avg description length: 19 characters
- Avg words: 3.1 per transaction
- No missing values
- Training time: 30-45 minutes

**When to use**: Final production model, maximum performance

---

### 2. `huggingface_sample_10k.csv`

**Size**: 10,000 records (470 KB)  
**Source**: Random sample from full HF dataset  
**Purpose**: Quick experiments and development  

**Description**:
- Representative sample maintaining category balance
- Same structure as full dataset
- Fast training for testing

**Statistics**:
- Training time: ~10 seconds
- Expected accuracy: ~97%
- Memory usage: <100 MB

**When to use**: 
-  Development and testing
-  Quick experiments
-  Demos and presentations
-  Learning the pipeline

---

### 3. `arabic_only_transactions.csv` 

**Size**: 10,000 records (580 KB)  
**Source**: Custom synthetic data generator  
**Purpose**: Multilingual NLP with pure Arabic  

**Description**:
- 100% Arabic text (no English or mixed)
- Modern Standard Arabic (MSA): 45%
- Egyptian Colloquial Arabic: 55%
- Real Egyptian merchant names
- Same 10 categories

**Special Features**:
- Authentic Arabic patterns
- Realistic imperfections (typos, incomplete text)
- Quality variations: 55% clean, 45% noisy
- Merchant names: البقالة، المطعم، الصيدلية

**Statistics**:
- Unique descriptions: 3,633 (36%)
- Duplication rate: 63.7% (realistic)
- Avg length: 16.3 characters
- No missing values

**When to use**:
-  Arabic NLP research
-  Multilingual model testing
-  Egyptian market applications
-  Cross-language evaluation

---

### 4. `arabic_only_transactions.parquet`

**Size**: 70 KB (compressed)  
**Purpose**: Same as CSV but compressed format  

**Benefits**:
- 8x smaller file size
- 2-3x faster loading
- Better memory efficiency
- Preserves data types

**When to use**: Production pipelines, large-scale processing

---

### 5. `arabic_transactions_clean.csv` (Legacy)

**Size**: 10,000 records (547 KB)  
**Status**:  Legacy - Use `arabic_only_transactions.csv` instead  

**Description**:
- Mixed language dataset
- Contains Arabic, English, and Arabizi
- Language distribution:
  - MSA: 25%
  - Egyptian Colloquial: 30%
  - Mixed Arabic-English: 20%
  - Arabizi: 15%
  - English: 10%

**Why not use?**:
- Language mixing complicates analysis
- Defeats "Arabic-only" purpose
- Better alternatives available

---

### 6. `arabic_transactions_clean.parquet` (Legacy)

**Size**: 70 KB  
**Purpose**: Compressed version of mixed-language dataset  
**Status**: Legacy - use pure Arabic or English instead

---

##  PROCESSED Datasets (`data/processed/`)

 **IMPORTANT**: All processed files are created **AFTER** preprocessing the raw data!

**Processing Steps Applied**:
1. Lowercase conversion
2. Punctuation removal
3. Number removal
4. Extra space removal
5. Then split into train/val/test

---

### Arabic-Only Splits (Primary)

#### `arabic_only_train.csv`
**Size**: 7,000 records (400 KB) - 70%  
**Purpose**: Model training  
**Details**: Preprocessed, stratified split, ready for TF-IDF

#### `arabic_only_validation.csv`
**Size**: 1,500 records (90 KB) - 15%  
**Purpose**: Hyperparameter tuning  
**Details**: Used during GridSearchCV, separate from training

#### `arabic_only_test.csv`
**Size**: 1,500 records (90 KB) - 15%  
**Purpose**: Final evaluation only  
**Details**: Never used during training, reports final metrics

---

### Mixed-Language Splits (Legacy)

#### `arabic_transactions_train.csv`
**Size**: 2,788 records (155 KB) - 70%  
**Status**: Legacy  
**Note**: From old mixed-language dataset

#### `arabic_transactions_validation.csv`
**Size**: 597 records (33 KB) - 15%  
**Status**: Legacy

#### `arabic_transactions_test.csv`
**Size**: 599 records (33 KB) - 15%  
**Status**: Legacy

---

### Label Noise Experiments

#### `arabic_transactions_noisy_2pct.csv`
**Size**: 2,788 records (204 KB)  
**Purpose**: Test model robustness  
**Details**: Training data with 2% corrupted labels (55 errors)

#### `arabic_transactions_noisy_5pct.csv`
**Size**: 2,788 records (204 KB)  
**Purpose**: Test model robustness  
**Details**: Training data with 5% corrupted labels (139 errors)

**Use Case**: Evaluate how well the model handles noisy/incorrect labels

---

##  Correct Workflow: Preprocess THEN Split

###  WRONG: Split First
```python
# DON'T DO THIS
df = pd.read_csv('data/raw/huggingface_sample_10k.csv')
X_train, X_test = train_test_split(df)  # Split raw
X_train['processed'] = preprocess(X_train)  # Separate preprocessing
X_test['processed'] = preprocess(X_test)    # Different processing!
```

###  CORRECT: Preprocess First
```python
# DO THIS
df = pd.read_csv('data/raw/huggingface_sample_10k.csv')

# 1. Preprocess ALL data together
df['processed'] = df['transaction_description'].apply(preprocess_text)

# 2. THEN split
X = df['processed']
y = df['category']
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

# Now ready for training
```

**Why?**
-  Consistent preprocessing across all sets
-  No data leakage
-  Same vocabulary and tokenization
-  Reproducible results

---

##  Usage Examples

### Load Raw Data for Training

```python
import pandas as pd
from sklearn.model_selection import train_test_split

# Load raw data
df = pd.read_csv('data/raw/huggingface_sample_10k.csv')

# Preprocess
def preprocess_text(text):
    import re
    text = str(text).lower()
    text = re.sub(r'[^a-z\s]', ' ', text)
    text = ' '.join(text.split())
    return text

df['processed'] = df['transaction_description'].apply(preprocess_text)

# Split
X = df['processed']
y = df['category']
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

# Train
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(max_features=5000)),
    ('clf', LogisticRegression())
])
pipeline.fit(X_train, y_train)
```

---

### Load Pre-Split Processed Data

```python
# If you want to use already split data
train_df = pd.read_csv('data/processed/arabic_only_train.csv')
val_df = pd.read_csv('data/processed/arabic_only_validation.csv')
test_df = pd.read_csv('data/processed/arabic_only_test.csv')

X_train = train_df['transaction_description']
y_train = train_df['category']
X_val = val_df['transaction_description']
y_val = val_df['category']
X_test = test_df['transaction_description']
y_test = test_df['category']

# Note: These are already preprocessed
# Ready to train directly
```

---

### Load Arabic Dataset

```python
# CSV format
df = pd.read_csv('data/raw/arabic_only_transactions.csv')

# Or Parquet (faster)
df = pd.read_parquet('data/raw/arabic_only_transactions.parquet')

# Preprocess and split same as English
df['processed'] = df['transaction_description'].apply(preprocess_text)
# ... then split
```

---

##  Dataset Comparison

| Dataset | Location | Records | Size | Purpose | Training Time |
|---------|----------|---------|------|---------|---------------|
| HF Full | raw/ | 4.5M | 211 MB | Production | 30-45 min |
| HF Sample | raw/ | 10K | 470 KB | Development | 10-15 sec |
| Arabic Only | raw/ | 10K | 580 KB | Multilingual | 10-15 sec |
| Arabic Mixed | raw/ | 10K | 547 KB | Legacy | 10-15 sec |

---

##  Which Dataset to Use?

### For Development & Learning
 **Use**: `data/raw/huggingface_sample_10k.csv`  
- Fast training (~10 seconds)
- Representative sample
- Perfect for experiments

### For Production
 **Use**: `data/raw/huggingface_full_dataset.csv`  
- Maximum accuracy
- Full 4.5M records
- Real-world performance

### For Arabic NLP
 **Use**: `data/raw/arabic_only_transactions.csv`  
- Pure Arabic text
- Egyptian dialect
- Multilingual research

### For Quick Testing
 **Use**: `data/processed/arabic_only_*.csv`  
- Already preprocessed
- Already split
- Ready to train

---

##  Data Quality

### All Datasets Include:
-  No missing values
-  Balanced category distribution
-  Consistent schema (4 columns)
-  UTF-8 encoding

### Quality Checks:
```python
import pandas as pd

# Load and check
df = pd.read_csv('data/raw/huggingface_sample_10k.csv')

print(f"Shape: {df.shape}")
print(f"Missing: {df.isnull().sum().sum()}")
print(f"Categories: {df['category'].nunique()}")
print(f"\nCategory distribution:")
print(df['category'].value_counts())
```

---

##  Regenerating Processed Data

If you need to regenerate the processed splits:

```bash
# Generate Arabic datasets
python generate_arabic_only_dataset.py
```

This creates:
- `data/raw/arabic_only_transactions.csv`
- `data/raw/arabic_only_transactions.parquet`
- `data/processed/arabic_only_train.csv`
- `data/processed/arabic_only_validation.csv`
- `data/processed/arabic_only_test.csv`

---

##  Best Practices

1.  **Always start with raw data**
2.  **Preprocess ALL data before splitting**
3.  **Use stratified split** for category balance
4.  **Set random seed** (42) for reproducibility
5.  **Keep test data separate** - never train on it
6.  **Use processed splits** only for quick testing
7.  **Document preprocessing steps**

---

##  Schema Reference

All datasets use this schema:

```python
{
    'transaction_description': str,  # Transaction text
    'category': str,                 # One of 10 categories
    'country': str,                  # Country code
    'currency': str                  # Currency code
}
```

**10 Categories**:
1. Food & Dining
2. Transportation
3. Shopping & Retail
4. Entertainment & Recreation
5. Healthcare & Medical
6. Utilities & Services
7. Financial Services
8. Income
9. Government & Legal
10. Charity & Donations

---

##  Quick Start Commands

```bash
# List raw datasets
ls data/raw/

# List processed datasets
ls data/processed/

# Check file sizes
du -sh data/raw/*
du -sh data/processed/*
```

---

##  Notes

- **Large File**: `huggingface_full_dataset.csv` is 211 MB (excluded from Git via .gitignore)
- **Parquet Files**: Use for production (faster, smaller)
- **Random Seed**: All splits use seed=42
- **Preprocessing**: Applied before splitting
- **UTF-8 Encoding**: All files use UTF-8

---

**Last Updated**: November 12, 2026  
**Structure**: raw/ + processed/  
**Total Raw Datasets**: 6 files  
**Total Processed Datasets**: 8 files  
**Random Seed**: 42
