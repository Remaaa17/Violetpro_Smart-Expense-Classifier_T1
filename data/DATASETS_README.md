# 📊 Smart Expense Classifier - Datasets Documentation

## 📁 Final Dataset Inventory

After cleanup and optimization, we maintain **4 core datasets** for different training scenarios.

---

## ✅ Available Datasets

### 1️⃣ **HuggingFace Full Dataset (REAL)** 🌟
**File:** `data/raw/huggingface_full_dataset.csv`  
**Size:** 211 MB (4,501,043 records)

**Characteristics:**
- ✅ Real-world data from HuggingFace
- ✅ Perfectly balanced (10% per category)
- ✅ Multi-country: USA, UK, Australia, India, Canada
- ✅ Multi-currency: USD, GBP, AUD, INR, CAD
- ✅ 100% English language
- 📊 Balance ratio: 1.01x (near perfect)
- 🔢 Uniqueness: 30.8% (realistic repetition)
- 📏 Text length: 2-71 chars (avg: 19)

**Categories (perfectly distributed):**
- Utilities & Services: 451,842 (10.04%)
- Government & Legal: 451,108 (10.02%)
- Financial Services: 450,959 (10.02%)
- Income: 450,545 (10.01%)
- Charity & Donations: 450,133 (10.00%)
- Shopping & Retail: 449,941 (10.00%)
- Healthcare & Medical: 449,857 (9.99%)
- Entertainment & Recreation: 449,495 (9.99%)
- Transportation: 449,235 (9.98%)
- Food & Dining: 447,928 (9.95%)

**Use Cases:**
- Large-scale model training
- Benchmarking
- Production models
- Cross-lingual transfer learning baseline

**Sample Records:**
```
[Income] Wage
[Food & Dining] Arby's (Contactless)
[Healthcare & Medical] Occupational Therapy
```

---

### 2️⃣ **HuggingFace Sample 10K** ⚡
**File:** `data/raw/huggingface_sample_10k.csv`  
**Size:** 0.47 MB (10,000 records)

**Characteristics:**
- ✅ Random sample from full dataset
- ✅ Near-balanced (1.12x ratio)
- ✅ Lower duplicate rate (10.1%)
- 🔢 Uniqueness: 77.2% (high diversity)
- 📏 Text length: 2-59 chars (avg: 19)

**Categories (near-balanced):**
- Transportation: 1,065 (10.65%)
- Entertainment & Recreation: 1,044 (10.44%)
- Shopping & Retail: 1,007 (10.07%)
- Charity & Donations: 1,001 (10.01%)
- Government & Legal: 998 (9.98%)
- Income: 993 (9.93%)
- Healthcare & Medical: 992 (9.92%)
- Food & Dining: 977 (9.77%)
- Utilities & Services: 968 (9.68%)
- Financial Services: 955 (9.55%)

**Use Cases:**
- Quick experiments
- Prototyping
- Testing preprocessing pipelines
- Notebook demonstrations

**Sample Records:**
```
[Transportation] Exxon - CANADA Store
[Food & Dining] Dunkin' Donuts - USA Branch
[Entertainment & Recreation] Zoo - INDIA Store - Night
```

---

### 3️⃣ **Arabic Only Transactions** 🇪🇬
**File:** `data/raw/arabic_only_transactions.csv`  
**Size:** 0.58 MB (10,000 records)

**Characteristics:**
- ✅ 100% Pure Arabic (no English mixing)
- ⚠️ **IMBALANCED** (5.42x ratio) - **REALISTIC DISTRIBUTION**
- ✅ Egyptian dialect focus
- 🇪🇬 Country: Egypt only
- 💵 Currency: EGP only
- 🔢 Uniqueness: 36.3%
- 📏 Text length: 6-37 chars (avg: 16)

**Categories (realistic imbalance):**
- Food & Dining: 1,882 (18.82%) ⬆️ Most common
- Transportation: 1,548 (15.48%)
- Shopping & Retail: 1,399 (13.99%)
- Utilities & Services: 1,223 (12.23%)
- Entertainment & Recreation: 1,105 (11.05%)
- Healthcare & Medical: 879 (8.79%)
- Financial Services: 754 (7.54%)
- Income: 467 (4.67%)
- Charity & Donations: 396 (3.96%)
- Government & Legal: 347 (3.47%) ⬇️ Least common

**Why Imbalanced?**
This reflects real-world Egyptian transaction patterns where:
- People eat/shop more frequently
- Government transactions are less common
- This tests model robustness to class imbalance

**Use Cases:**
- Arabic-specific model training
- Testing model performance on imbalanced data
- Evaluating class imbalance handling
- Regional (Egyptian) expense classification

**Sample Records:**
```
[Healthcare & Medical] أشعة في معمل التحاليل
[Utilities & Services] سددت فاتورة شركة الغاز
[Food & Dining] شراء خبز من البقالة
```

---

### 4️⃣ **Arabic Balanced with Diacritics** ✨ **NEW**
**File:** `data/raw/arabic_balanced_diacritics_clean.csv`  
**Size:** 0.71 MB (10,000 records)

**Characteristics:**
- ✅ 100% Arabic
- ✅ Perfectly balanced (1.00x ratio)
- ✅ **Mixed diacritics (Tashkeel):**
  - 30% no diacritics (clean)
  - 40% partial diacritics (realistic)
  - 30% full diacritics (formal)
- 🇪🇬 Country: Egypt only
- 💵 Currency: EGP only
- 🔢 Uniqueness: 20.2% (high repetition - realistic)
- 📏 Text length: 7-63 chars (avg: 24)

**Categories (perfectly balanced):**
- All categories: exactly 1,000 records each (10.00%)

**Diacritic Examples:**
```
No diacritics:     دفعت للبنك الصراف الآلي
Partial:           دفعتُ للبنك الصراف الآلي
Full:              دَفَعْتُ لِلْبَنْكِ الصَّرَّافِ الآلِيِّ
```

**Use Cases:**
- Testing impact of Arabic diacritics on classification
- Evaluating preprocessing (diacritic removal)
- Comparing model performance with/without normalization
- Formal Arabic document classification

**Sample Records:**
```
[Financial Services] دفعت للبنك الصراف الآلي
[Healthcare & Medical] كشف عند المستشفى
[Transportation] رحلة تَاكْسِي أَبْيَضْ
```

---

## 🗑️ Removed Datasets

The following datasets were removed to avoid redundancy and confusion:

### ❌ Deleted:
1. **`arabic_transactions_clean.csv`**
   - Reason: Mixed Arabic/English (76% Arabic) - redundant with arabic_only
   - Use arabic_only_transactions.csv for pure Arabic instead

2. **`arabic_balanced_diacritics.csv`** (with metadata column)
   - Reason: Contains extra "diacritic_type" column
   - Use arabic_balanced_diacritics_clean.csv instead

3. **All `.parquet` files**
   - Reason: Standardizing on CSV format for consistency

4. **All files in `data/processed/`**
   - Reason: Train/validation/test splits should be created AFTER preprocessing in notebooks to avoid data leakage
   - Files removed:
     - arabic_only_train/validation/test.csv
     - arabic_transactions_train/validation/test.csv

---

## 📚 Usage Guidelines

### For Training English Models:
```python
# Large-scale training
df = pd.read_csv('data/raw/huggingface_full_dataset.csv')

# Quick experiments
df = pd.read_csv('data/raw/huggingface_sample_10k.csv')
```

### For Training Arabic Models:
```python
# Realistic (imbalanced) Arabic data
df = pd.read_csv('data/raw/arabic_only_transactions.csv')

# Testing diacritics effect (balanced)
df = pd.read_csv('data/raw/arabic_balanced_diacritics_clean.csv')
```

### Train/Val/Test Split:
**⚠️ IMPORTANT:** Always split AFTER preprocessing to avoid data leakage!

```python
# 1. Load data
df = pd.read_csv('data/raw/your_dataset.csv')

# 2. Preprocess
df['processed_text'] = df['transaction_description'].apply(preprocess_function)

# 3. THEN split
from sklearn.model_selection import train_test_split

X = df['processed_text']
y = df['category']

X_temp, X_test, y_temp, y_test = train_test_split(
    X, y, test_size=0.15, stratify=y, random_state=42
)

X_train, X_val, y_train, y_val = train_test_split(
    X_temp, y_temp, test_size=0.176, stratify=y_temp, random_state=42
)

# Result: 70% train, 15% val, 15% test
```

---

## 📊 Dataset Comparison Summary

| Dataset | Records | Language | Balanced | Uniqueness | Use Case |
|---------|---------|----------|----------|------------|----------|
| HuggingFace Full | 4.5M | English | ✅ Yes (1.01x) | 30.8% | Large-scale training |
| HuggingFace Sample | 10K | English | ✅ Yes (1.12x) | 77.2% | Quick experiments |
| Arabic Only | 10K | Arabic (100%) | ❌ No (5.42x) | 36.3% | Realistic Arabic |
| Arabic Diacritics | 10K | Arabic (100%) | ✅ Yes (1.00x) | 20.2% | Diacritics testing |

---

## 🔄 Regenerating Datasets

If you need to regenerate the synthetic Arabic datasets:

```bash
# Generate Arabic only dataset
python data/scripts/generate_arabic_only_dataset.py

# Generate balanced diacritics dataset
python data/scripts/generate_balanced_arabic_diacritics.py
```

To re-download HuggingFace data:
```bash
python download_huggingface_data.py
```

---

## 📝 Notes

- All datasets use the same 10 categories
- Country/Currency columns are fixed per dataset
- No missing values in any dataset
- Duplicates vary by dataset (realistic)
- All text is in `transaction_description` column
- Labels are in `category` column

---

**Last Updated:** November 2026  
**Maintained By:** Smart Expense Classifier Team
