# Dataset Directory

This directory contains all transaction datasets used for the Smart Expense Classifier project.

---

## 📁 Dataset Files Overview

### 1. Hugging Face Transaction Dataset

#### `huggingface_full_dataset.csv` 
**Size**: 4,501,043 records (211 MB)  
**Source**: [Hugging Face - mitulshah/transaction-categorization](https://huggingface.co/datasets/mitulshah/transaction-categorization)  
**Purpose**: Full production dataset for training robust models  
**Content**: 
- Global transactions from multiple countries
- Multiple currencies (USD, EUR, GBP, AUD, etc.)
- Real-world transaction descriptions
- 10 expense/income categories

**Columns**:
- `transaction_description` (string): Transaction text (e.g., "Starbucks Coffee")
- `category` (string): One of 10 categories
- `country` (string): Country code
- `currency` (string): Currency code

**Statistics**:
- Average description length: 19 characters
- Average words per transaction: 3.1
- Balanced distribution across categories
- No missing values

**Use Case**: Train final production model with maximum accuracy

---

#### `huggingface_sample_10k.csv`
**Size**: 10,000 records (470 KB)  
**Source**: Random sample from full HF dataset  
**Purpose**: Quick experiments and testing  
**Content**: Representative sample maintaining category distribution

**Why use this?**
- ✅ Fast training (seconds vs minutes)
- ✅ Perfect for development/testing
- ✅ Same structure as full dataset
- ✅ Good for demos and presentations

**Statistics**:
- Training time: ~10 seconds
- Accuracy: ~97% (similar to full dataset)
- Memory usage: <100 MB

---

### 2. Egyptian Arabic Dataset (Custom Generated) ⭐

#### `arabic_only_transactions.csv`
**Size**: 10,000 records (580 KB)  
**Source**: Custom synthetic data generator  
**Purpose**: Test multilingual NLP capabilities with Arabic text  
**Language**: 100% Arabic - No English or mixed languages

**Content**:
- Modern Standard Arabic (MSA): 45%
- Egyptian Colloquial Arabic: 55%
- Realistic imperfections (typos, incomplete text, ambiguous cases)
- Same 10 categories as English dataset

**Special Features**:
- Real Egyptian merchant names (البقالة, المطعم, الصيدلية)
- Authentic Arabic transaction patterns
- Quality variations: 55% clean, 45% realistic noise
- Suitable for Arabic NLP research

**Statistics**:
- Unique descriptions: 3,633 (36%)
- Duplication rate: 63.7% (realistic for recurring transactions)
- Average length: 16.3 characters
- No missing values

**Use Case**: 
- Multilingual model training
- Arabic text classification research
- Cross-language performance testing
- Egyptian market applications

---

#### `arabic_only_transactions.parquet`
**Size**: 70 KB (compressed)  
**Purpose**: Same data as CSV but in Parquet format  
**Benefits**:
- ✅ 8x smaller file size
- ✅ Faster loading (2-3x speed)
- ✅ Better memory efficiency
- ✅ Preserves data types

**When to use**: For production pipelines and large-scale processing

---

### 3. Pre-Split Arabic Training Sets

⚠️ **IMPORTANT**: These splits are created **AFTER preprocessing**, not before!

#### `arabic_only_train.csv`
**Size**: 7,000 records (400 KB) - 70%  
**Purpose**: Model training  
**Details**: 
- Preprocessed and ready for TF-IDF
- Stratified split (maintains category balance)
- Used for fitting the model

#### `arabic_only_validation.csv`
**Size**: 1,500 records (90 KB) - 15%  
**Purpose**: Hyperparameter tuning and model selection  
**Details**:
- Separate from training data
- Used during GridSearchCV
- Helps prevent overfitting

#### `arabic_only_test.csv`
**Size**: 1,500 records (90 KB) - 15%  
**Purpose**: Final evaluation only  
**Details**:
- Never used during training
- Final performance metric
- Reports final accuracy/F1

**Split Method**:
```python
# Data is preprocessed FIRST
df['processed'] = df['description'].apply(preprocess_text)

# THEN shuffled and split with stratification
train: 70% (7,000 records)
val:   15% (1,500 records)
test:  15% (1,500 records)
```

---

### 4. Old Mixed-Language Dataset (Legacy)

#### `arabic_transactions_clean.csv`
**Size**: 10,000 records (547 KB)  
**Status**: ⚠️ Legacy - Use `arabic_only_transactions.csv` instead  
**Content**: Mixed Arabic, English, and Arabizi (Franco-Arabic)

**Language Mix**:
- Modern Standard Arabic: 25%
- Egyptian Colloquial: 30%
- Mixed Arabic-English: 20%
- Arabizi (Franco-Arabic): 15%
- Pure English: 10%

**Why not use this?**
- Contains English which defeats the "Arabic-only" purpose
- Code-switching makes analysis complex
- Better to use pure Arabic or pure English

**Pre-split versions** (also legacy):
- `arabic_transactions_train.csv` (2,788 records)
- `arabic_transactions_validation.csv` (597 records)
- `arabic_transactions_test.csv` (599 records)
- `arabic_transactions_noisy_2pct.csv` (with 2% label noise)
- `arabic_transactions_noisy_5pct.csv` (with 5% label noise)
- `arabic_transactions_clean.parquet` (compressed)

---

## 🎯 Which Dataset to Use?

### For Learning & Development
✅ **Use**: `huggingface_sample_10k.csv`  
**Why**: Fast, representative, perfect for experiments

### For Production Model
✅ **Use**: `huggingface_full_dataset.csv`  
**Why**: Maximum accuracy, real-world performance

### For Arabic/Multilingual
✅ **Use**: `arabic_only_transactions.csv`  
**Why**: Pure Arabic, clean separation from English

### For Quick Testing
✅ **Use**: Pre-split files (`train.csv`, `val.csv`, `test.csv`)  
**Why**: Ready to use, no splitting needed

---

## 📊 Data Schema (All Datasets)

All CSV files follow this structure:

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `transaction_description` | string | Transaction text | "Starbucks Coffee" |
| `category` | string | Expense category | "Food & Dining" |
| `country` | string | Country code | "Egypt" |
| `currency` | string | Currency code | "EGP" |

---

## 🔄 Data Splitting Strategy

**IMPORTANT**: Split happens **AFTER** preprocessing, not before!

### ❌ Wrong Way (Split First):
```python
# DON'T DO THIS
X_train, X_test = train_test_split(df)  # Split raw data
X_train_processed = preprocess(X_train)  # Process separately
X_test_processed = preprocess(X_test)    # Different preprocessing!
```

### ✅ Right Way (Preprocess First):
```python
# DO THIS
df['processed'] = df['description'].apply(preprocess)  # Process all data together
X = df['processed']
y = df['category']
X_train, X_test, y_train, y_test = train_test_split(X, y)  # Then split
```

**Why?**
- Ensures consistent preprocessing across all sets
- Prevents data leakage
- Same tokenization and vocabulary
- Reproducible results

---

## 📈 Dataset Statistics Comparison

| Dataset | Records | Size | Avg Length | Unique Desc | Training Time |
|---------|---------|------|------------|-------------|---------------|
| HF Full | 4.5M | 211 MB | 19 chars | ~3M | 30-45 min |
| HF Sample | 10K | 470 KB | 19 chars | ~8K | 10-15 sec |
| Arabic Only | 10K | 580 KB | 16 chars | 3.6K | 10-15 sec |
| Arabic Mixed | 10K | 547 KB | 18 chars | 3.9K | 10-15 sec |

---

## 💾 Loading Data Examples

### Load Full Dataset
```python
import pandas as pd

# English dataset
df = pd.read_csv('data/huggingface_full_dataset.csv')
print(f"Loaded {len(df):,} transactions")
```

### Load Sample
```python
# Quick experiments
df = pd.read_csv('data/huggingface_sample_10k.csv')
```

### Load Arabic
```python
# Arabic-only dataset
df = pd.read_csv('data/arabic_only_transactions.csv')

# Or use Parquet (faster)
df = pd.read_parquet('data/arabic_only_transactions.parquet')
```

### Load Pre-Split Data
```python
# Load training set
train_df = pd.read_csv('data/arabic_only_train.csv')
val_df = pd.read_csv('data/arabic_only_validation.csv')
test_df = pd.read_csv('data/arabic_only_test.csv')

print(f"Train: {len(train_df):,}")
print(f"Val: {len(val_df):,}")
print(f"Test: {len(test_df):,}")
```

---

## 🔍 Data Quality Notes

### Hugging Face Dataset
- ✅ High quality, real transactions
- ✅ Balanced categories
- ✅ No missing values
- ✅ Global coverage

### Arabic Datasets
- ✅ Realistic language patterns
- ✅ Controlled quality variations
- ✅ Category balance maintained
- ⚠️ Synthetic (not real transactions)

---

## ⚙️ Preprocessing Pipeline

**Correct Order**:

1. **Load raw data**
2. **Preprocess ALL data together**
   - Lowercase
   - Remove punctuation
   - Remove numbers
   - Remove extra spaces
3. **THEN split into train/val/test**
4. **Apply TF-IDF on training set**
5. **Transform val/test using same TF-IDF**

```python
# Example: Correct preprocessing workflow
import pandas as pd
from sklearn.model_selection import train_test_split

# 1. Load
df = pd.read_csv('data/huggingface_sample_10k.csv')

# 2. Preprocess ALL data first
def preprocess_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-z\s]', ' ', text)
    text = ' '.join(text.split())
    return text

df['processed'] = df['transaction_description'].apply(preprocess_text)

# 3. NOW split (after preprocessing)
X = df['processed']
y = df['category']
X_train, X_temp, y_train, y_temp = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)
X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp
)

# 4. Now ready for TF-IDF and training
```

---

## 🚀 Quick Start Examples

### Example 1: Train on English Sample
```python
# Load
df = pd.read_csv('data/huggingface_sample_10k.csv')

# Preprocess ALL data first
df['processed'] = df['transaction_description'].apply(preprocess_text)

# Then split
from sklearn.model_selection import train_test_split
X = df['processed']
y = df['category']
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

# Now train
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(max_features=5000)),
    ('clf', LogisticRegression())
])
pipeline.fit(X_train, y_train)
```

### Example 2: Train on Arabic
```python
# Load Arabic
df = pd.read_csv('data/arabic_only_transactions.csv')

# Same process: preprocess first, then split
df['processed'] = df['transaction_description'].apply(preprocess_text)
X = df['processed']
y = df['category']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train
pipeline.fit(X_train, y_train)
```

### Example 3: Use Pre-Split (Already Preprocessed)
```python
# If data is already split and preprocessed
train_df = pd.read_csv('data/arabic_only_train.csv')
test_df = pd.read_csv('data/arabic_only_test.csv')

X_train = train_df['transaction_description']
y_train = train_df['category']
X_test = test_df['transaction_description']
y_test = test_df['category']

# Ready to train!
pipeline.fit(X_train, y_train)
```

---

## 📝 Data Generation Scripts

If you want to regenerate the Arabic datasets:

```bash
# Generate Arabic-only dataset
python generate_arabic_only_dataset.py
```

Output:
- `data/arabic_only_transactions.csv`
- `data/arabic_only_transactions.parquet`
- `data/arabic_only_train.csv`
- `data/arabic_only_validation.csv`
- `data/arabic_only_test.csv`

---

## 🎓 Best Practices

1. ✅ **Always preprocess before splitting**
2. ✅ **Use stratified split** to maintain category balance
3. ✅ **Set random seed** for reproducibility (42)
4. ✅ **Never train on test data**
5. ✅ **Keep validation separate** from test
6. ✅ **Document preprocessing steps**
7. ✅ **Apply same TF-IDF transform** to val/test

---

## 📚 References

- Hugging Face Dataset: https://huggingface.co/datasets/mitulshah/transaction-categorization
- Egyptian Arabic patterns: Generated using authentic merchant names and transaction structures
- Data split ratios: Industry standard 70/15/15
- Random seed: 42 (for reproducibility)

---

**Last Updated**: November 12, 2026  
**Total Datasets**: 4 main datasets + pre-split versions  
**Total Size**: ~220 MB (with full HF dataset)  
**Random Seed**: 42 (all splits)  
**Preprocessing**: Applied BEFORE splitting
