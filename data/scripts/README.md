# 🛠️ Data Generation Scripts

This folder contains scripts to generate and download datasets for the Smart Expense Classifier project.

---

## 📋 Available Scripts

### 1️⃣ **download_huggingface_data.py** 🌐
**Purpose:** Download real transaction data from HuggingFace

**Output:**
- `data/raw/huggingface_full_dataset.csv` (4.5M records)
- `data/raw/huggingface_sample_10k.csv` (10K sample)

**Usage:**
```bash
python data/scripts/download_huggingface_data.py
```

**Dataset:** `mitulshah/transaction-categorization`  
**Time:** ~2-5 minutes (depending on internet speed)

---

### 2️⃣ **generate_arabic_only_dataset.py** 🇪🇬
**Purpose:** Generate pure Arabic transaction dataset

**Output:**
- `data/raw/arabic_only_transactions.csv` (10K records)
- Train/validation/test splits

**Features:**
- 100% Pure Arabic (no English)
- Egyptian dialect focus
- Realistic imbalanced distribution
- Modern Standard Arabic + Egyptian Colloquial

**Usage:**
```bash
python data/scripts/generate_arabic_only_dataset.py
```

**Time:** ~10-30 seconds

---

### 3️⃣ **generate_balanced_arabic_diacritics.py** ✨
**Purpose:** Generate balanced Arabic dataset with mixed diacritics

**Output:**
- `data/raw/arabic_balanced_diacritics_clean.csv` (10K records)

**Features:**
- Perfectly balanced (1,000 records per category)
- Mixed diacritics: 30% none, 40% partial, 30% full
- Pure Arabic
- Egyptian context

**Usage:**
```bash
python data/scripts/generate_balanced_arabic_diacritics.py
```

**Time:** ~15-30 seconds

---

### 4️⃣ **generate_egyptian_dataset.py** 🇪🇬
**Purpose:** Generate mixed-language Egyptian transactions (legacy)

**Output:**
- Mixed Arabic/English transactions
- Multiple quality levels (clean, noisy, ambiguous)

**Features:**
- Egyptian Colloquial Arabic
- Arabic-English code-switching
- Arabizi (Franco-Arabic)
- Realistic noise and imperfections

**Usage:**
```bash
python data/scripts/generate_egyptian_dataset.py
```

**Note:** This is a legacy script. Use `generate_arabic_only_dataset.py` for pure Arabic data.

---

### 5️⃣ **generate_main_dataset.py** 📊
**Purpose:** Main dataset generation (if needed)

**Usage:**
```bash
python data/scripts/generate_main_dataset.py
```

---

## 🎯 Quick Start

### To get all datasets:
```bash
# 1. Download real HuggingFace data
python data/scripts/download_huggingface_data.py

# 2. Generate pure Arabic data (imbalanced - realistic)
python data/scripts/generate_arabic_only_dataset.py

# 3. Generate balanced Arabic with diacritics
python data/scripts/generate_balanced_arabic_diacritics.py
```

### Expected results:
```
data/raw/
├── huggingface_full_dataset.csv          (211 MB - 4.5M records)
├── huggingface_sample_10k.csv            (0.47 MB - 10K records)
├── arabic_only_transactions.csv          (0.58 MB - 10K records)
└── arabic_balanced_diacritics_clean.csv  (0.71 MB - 10K records)
```

---

## ⚙️ Requirements

All scripts require:
```bash
pip install pandas numpy datasets
```

For Arabic text processing (optional):
```bash
pip install arabic-reshaper python-bidi
```

---

## 📊 Output Summary

| Script | Output File | Size | Records | Language | Balanced |
|--------|------------|------|---------|----------|----------|
| download_huggingface | huggingface_full_dataset.csv | 211 MB | 4.5M | English | ✅ |
| download_huggingface | huggingface_sample_10k.csv | 0.47 MB | 10K | English | ✅ |
| generate_arabic_only | arabic_only_transactions.csv | 0.58 MB | 10K | Arabic | ❌ Imbalanced |
| generate_balanced_diacritics | arabic_balanced_diacritics_clean.csv | 0.71 MB | 10K | Arabic | ✅ |

---

## 🔧 Customization

### Change dataset size:
```python
# In generate_arabic_only_dataset.py
generate_dataset(n_records=20000)  # Generate 20K instead of 10K
```

### Change balance distribution:
```python
# In generate_balanced_arabic_diacritics.py
generate_balanced_dataset(records_per_category=1500)  # 1500 per category = 15K total
```

### Change diacritic distribution:
```python
# In generate_balanced_arabic_diacritics.py
diacritic_weights = [0.50, 0.30, 0.20]  # 50% none, 30% partial, 20% full
```

---

## 🗑️ Cleanup

These scripts do NOT create files outside `data/raw/` and `reports/`.

To clean generated data:
```bash
# Remove all generated datasets (keeps scripts)
rm data/raw/arabic_*.csv
rm data/raw/huggingface_*.csv
```

---

## 📝 Notes

- All scripts use `RANDOM_SEED = 42` for reproducibility
- Generated datasets are deterministic (same output each run)
- HuggingFace download requires internet connection
- Scripts save to `data/raw/` automatically
- Quality reports saved to `reports/` folder

---

**Last Updated:** November 2026  
**Maintained By:** Smart Expense Classifier Team
