# 💰 Smart Expense Classifier

An AI-powered transaction categorization system using Machine Learning to automatically classify financial transactions into 10 expense categories.

**VioletPro Internship Project | November 2026**

---

## 🎯 Project Overview

This project implements a complete machine learning pipeline for transaction categorization, achieving **97.5% accuracy** on the Hugging Face transaction dataset (4.5M records).

### Key Features

- ✅ **Complete ML Pipeline**: EDA → Preprocessing → Baseline → Model Comparison → Tuning
- ✅ **10 Categories**: Food, Transport, Shopping, Healthcare, Utilities, Financial, Income, Entertainment, Government, Charity
- ✅ **4 ML Models**: Logistic Regression, Naive Bayes, Linear SVM, Random Forest
- ✅ **Hyperparameter Tuning**: GridSearchCV optimization
- ✅ **Interactive Demo**: Streamlit web application
- ✅ **Arabic Support**: Egyptian Arabic dataset (10K records)

---

## 📊 Results Summary

| Model | Test Accuracy | Precision | Recall | F1-Score |
|-------|--------------|-----------|--------|----------|
| **Logistic Regression** | **97.43%** | 97.44% | 97.43% | 97.43% |
| Linear SVM | 97.40% | 97.42% | 97.40% | 97.40% |
| Random Forest | 97.35% | 97.37% | 97.35% | 97.36% |
| Naive Bayes | 97.13% | 97.19% | 97.13% | 97.15% |

**Final Model (Tuned Logistic Regression)**: **97.52%** accuracy

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Install all required packages
python -m pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('stopwords')"
```

**Or use the setup script:**

```bash
python setup_environment.py
```

### 2. Train the Model

```bash
# Run complete ML pipeline (trains on 100K sample)
python src/train_complete_pipeline.py
```

This will:
- Load and analyze the dataset
- Perform EDA with visualizations
- Train 4 different models
- Compare and select best model
- Tune hyperparameters with GridSearchCV
- Save final model and generate reports

**Output:**
- Models saved in `models/`
- Visualizations saved in `reports/`
- Metrics and confusion matrices

### 3. Run Streamlit Demo

```bash
# Launch interactive web app
streamlit run app/streamlit_app.py
```

Open browser at `http://localhost:8501`

---

## 📁 Project Structure

```
Smart-Expense-Classifier/
├── data/                                    # Datasets
│   ├── huggingface_full_dataset.csv         # 4.5M transactions
│   ├── huggingface_sample_10k.csv           # 10K sample
│   ├── arabic_only_transactions.csv         # Egyptian Arabic (10K)
│   └── README.md                            # Data documentation
│
├── notebooks/                               # Jupyter notebooks
│   └── 01_Complete_ML_Pipeline.ipynb        # Full pipeline notebook
│
├── src/                                     # Source code
│   ├── train_complete_pipeline.py           # Main training script
│   └── predict.py                           # Prediction function
│
├── models/                                  # Trained models
│   ├── final_expense_classifier.joblib      # Best model
│   ├── baseline_model_tfidf_logreg.joblib   # Baseline
│   ├── best_model_tuned.joblib              # Tuned model
│   └── model_metadata.json                  # Model info
│
├── reports/                                 # Visualizations & reports
│   ├── 01_eda_analysis.png                  # EDA charts
│   ├── 02_model_comparison.png              # Model comparison
│   ├── 03_final_confusion_matrix.png        # Confusion matrix
│   ├── model_comparison_results.csv         # Detailed metrics
│   └── data_quality_summary.txt             # Dataset stats
│
├── app/                                     # Streamlit demo
│   └── streamlit_app.py                     # Web application
│
├── requirements.txt                         # Python dependencies
├── setup_environment.py                     # Environment setup script
└── README.md                                # This file
```

---

## 🔬 Technical Implementation

### 1. Exploratory Data Analysis (EDA)

- **Class Distribution**: Balanced across 10 categories
- **Text Length Analysis**: Avg 19 characters, 3 words
- **Common Words**: Category-specific vocabulary analysis
- **Visualizations**: Bar charts, histograms, box plots

### 2. Text Preprocessing

```python
def preprocess_text(text):
    # Convert to lowercase
    text = str(text).lower()
    
    # Remove punctuation and numbers
    text = re.sub(r'[^a-z\s]', ' ', text)
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text
```

### 3. Feature Engineering

**TF-IDF Vectorization:**
- Max features: 5000
- N-grams: (1, 2) - unigrams and bigrams
- Min document frequency: 2
- Max document frequency: 0.9
- Stop words: English

### 4. Models Compared

1. **Logistic Regression** (Winner)
   - L2 regularization
   - Max iterations: 1000
   - Multi-class: auto

2. **Naive Bayes**
   - MultinomialNB
   - Fast training
   - Probabilistic

3. **Linear SVM**
   - LinearSVC
   - Hinge loss
   - L2 penalty

4. **Random Forest**
   - 100 estimators
   - Max features: auto
   - Parallel processing

### 5. Hyperparameter Tuning

**GridSearchCV Parameters:**
```python
param_grid = {
    'tfidf__max_features': [3000, 5000, 7000],
    'tfidf__ngram_range': [(1, 1), (1, 2)],
    'clf__C': [0.1, 1.0, 10.0]
}
```

**Best Parameters:**
- `tfidf__max_features`: 3000
- `tfidf__ngram_range`: (1, 1)
- `clf__C`: 10.0

### 6. Evaluation Metrics

- **Accuracy**: Overall correctness
- **Precision**: Positive prediction accuracy
- **Recall**: True positive detection rate
- **F1-Score**: Harmonic mean of precision and recall
- **Confusion Matrix**: Per-category performance

---

## 💻 Usage Examples

### Command Line Prediction

```python
from src.predict import predict

# Single prediction
result = predict("Starbucks coffee")
print(f"Category: {result['category']}")
print(f"Confidence: {result['confidence']:.2%}")

# Example output:
# Category: Food & Dining
# Confidence: 98.50%
```

### Batch Prediction

```python
import pandas as pd
from src.predict import predict

# Load transactions
df = pd.read_csv('transactions.csv')

# Predict for all
predictions = []
for desc in df['transaction_description']:
    result = predict(desc)
    predictions.append(result['category'])

df['category'] = predictions
df.to_csv('predictions.csv', index=False)
```

### Streamlit Web App

1. Launch app: `streamlit run app/streamlit_app.py`
2. Enter transaction description
3. View prediction with confidence score
4. See top 3 category probabilities
5. Upload CSV for batch prediction

---

## 📈 Model Performance

### Confusion Matrix

The model shows strong performance across all categories with minimal confusion:

- **Perfect Categories**: Charity & Donations, Entertainment & Recreation (100% precision/recall)
- **Strong Categories**: Financial Services, Food & Dining, Transportation (>98%)
- **Good Categories**: Income, Shopping (>94%)

### Category-Specific Performance

| Category | Precision | Recall | F1-Score | Support |
|----------|-----------|--------|----------|---------|
| Charity & Donations | 1.00 | 1.00 | 1.00 | 1,481 |
| Entertainment & Recreation | 1.00 | 1.00 | 1.00 | 1,509 |
| Financial Services | 0.99 | 0.99 | 0.99 | 1,511 |
| Food & Dining | 0.98 | 0.97 | 0.98 | 1,491 |
| Government & Legal | 0.97 | 0.98 | 0.97 | 1,480 |
| Healthcare & Medical | 0.98 | 0.96 | 0.97 | 1,499 |
| Income | 0.94 | 0.98 | 0.96 | 1,517 |
| Shopping & Retail | 0.94 | 0.94 | 0.94 | 1,493 |
| Transportation | 0.98 | 0.95 | 0.97 | 1,499 |
| Utilities & Services | 0.97 | 0.98 | 0.97 | 1,520 |

---

## 🌍 Arabic Dataset

A custom Egyptian Arabic dataset (10K records) was generated with:

- **Language Styles**: Modern Standard Arabic (45%), Egyptian Colloquial (55%)
- **Quality Distribution**: 55% clean, 45% realistic imperfections
- **Categories**: Same 10 categories as English dataset
- **Use Case**: Test multilingual classification capabilities

**Files:**
- `data/arabic_only_transactions.csv` - Full dataset
- `data/arabic_only_train.csv` - Training (70%)
- `data/arabic_only_validation.csv` - Validation (15%)
- `data/arabic_only_test.csv` - Test (15%)

---

## 📚 Dataset Information

### Hugging Face Dataset

- **Source**: [mitulshah/transaction-categorization](https://huggingface.co/datasets/mitulshah/transaction-categorization)
- **Size**: 4,501,043 transactions
- **Countries**: Global (multiple currencies)
- **Categories**: 10 expense/income types

### Sample Data

```csv
transaction_description,category,country,currency
Starbucks Coffee,Food & Dining,USA,USD
Uber ride to airport,Transportation,USA,USD
Amazon Electronics,Shopping & Retail,USA,USD
Doctor appointment,Healthcare & Medical,USA,USD
```

---

## 🛠️ Development

### Requirements

- Python 3.8+
- pandas >= 2.0.0
- numpy >= 1.24.0
- scikit-learn >= 1.3.0
- matplotlib >= 3.7.0
- seaborn >= 0.12.0
- nltk >= 3.8.0
- streamlit >= 1.28.0
- plotly >= 5.17.0
- jupyter >= 1.0.0

### Running Jupyter Notebook

```bash
# Start Jupyter
jupyter notebook

# Open notebook
notebooks/01_Complete_ML_Pipeline.ipynb
```

### Training on Full Dataset

By default, scripts use 100K sample for faster processing. To train on full 4.5M:

```python
# In src/train_complete_pipeline.py
df = load_data(sample_size=None)  # Load all records
```

**Note**: Full dataset training takes ~30-45 minutes and requires ~8GB RAM.

---

## 📊 Reports & Visualizations

All reports are automatically generated in `reports/`:

1. **EDA Analysis** (`01_eda_analysis.png`)
   - Category distribution
   - Text length histogram
   - Word count distribution
   - Category-wise length box plots

2. **Model Comparison** (`02_model_comparison.png`)
   - Test accuracy comparison
   - Precision, Recall, F1 comparison
   - Training time comparison
   - Train/Val/Test accuracy trends

3. **Confusion Matrix** (`03_final_confusion_matrix.png`)
   - Detailed per-category performance
   - Misclassification patterns

4. **Metrics CSV** (`model_comparison_results.csv`)
   - Detailed numeric results
   - All evaluation metrics

---

## 🎯 Future Improvements

1. **Model Enhancements**
   - Deep Learning: LSTM, BERT, Transformers
   - Ensemble methods: Voting, Stacking
   - Active learning for edge cases

2. **Feature Engineering**
   - Amount-based features
   - Temporal patterns (day, month, season)
   - Merchant embeddings

3. **Deployment**
   - REST API (FastAPI/Flask)
   - Docker containerization
   - Cloud deployment (AWS/GCP/Azure)
   - Real-time prediction service

4. **Data Expansion**
   - More languages (Spanish, French, German)
   - Multi-currency support
   - Historical transaction patterns

5. **UI/UX**
   - Mobile app
   - Browser extension
   - Bank integration APIs

---

## 📝 License

This project was developed as part of the VioletPro internship program (2026).

---

## 👤 Author

**VioletPro Internship Program**  
**Location**: Tyre, Lebanon  
**Date**: November 2026

---

## 🙏 Acknowledgments

- **Hugging Face** for the transaction dataset
- **scikit-learn** for ML tools
- **Streamlit** for the demo framework
- **VioletPro** for the internship opportunity

---

## 📞 Support

For questions or issues:
1. Check the documentation in `reports/`
2. Review example notebooks in `notebooks/`
3. Examine training logs in terminal output

---

## ✅ Project Checklist

- [x] EDA with class distribution, text length, common words
- [x] Text preprocessing (lowercase, punctuation, stop words)
- [x] Baseline model (TF-IDF + Logistic Regression)
- [x] Model comparison (4 models: LogReg, NB, SVM, RF)
- [x] Evaluation metrics (Accuracy, Precision, Recall, F1, Confusion Matrix)
- [x] Hyperparameter tuning (GridSearchCV)
- [x] Model saving (joblib) with predict() function
- [x] Streamlit demo app
- [x] Arabic dataset generation
- [x] Complete documentation
- [x] Git version control

**Status**: ✅ **Complete** - Ready for presentation!

---

**Last Updated**: November 12, 2026  
**Version**: 1.0.0  
**Test Accuracy**: 97.52%
