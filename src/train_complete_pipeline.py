"""
Complete ML Pipeline for Smart Expense Classifier
Implements all requirements: EDA, preprocessing, baseline, model comparison,
evaluation, tuning, and model saving with prediction function.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import re
import time
import os
import json
import joblib
from collections import Counter

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix, ConfusionMatrixDisplay
)

# Settings
warnings.filterwarnings('ignore')
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette('husl')
RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)

# Create directories
os.makedirs('models', exist_ok=True)
os.makedirs('reports', exist_ok=True)


def preprocess_text(text):
    """Preprocess transaction description text"""
    if pd.isna(text):
        return ""
    text = str(text).lower()
    text = re.sub(r'[^a-z\s]', ' ', text)
    text = ' '.join(text.split())
    return text


def load_data(sample_size=100000):
    """Load Hugging Face dataset"""
    print("="*70)
    print("LOADING DATASET")
    print("="*70)
    
    start_time = time.time()
    df = pd.read_csv('data/huggingface_full_dataset.csv', nrows=sample_size)
    
    print(f"✅ Loaded {len(df):,} records in {time.time() - start_time:.2f}s")
    print(f"Columns: {df.columns.tolist()}")
    print(f"Shape: {df.shape}")
    
    return df


def perform_eda(df):
    """Exploratory Data Analysis"""
    print("\n" + "="*70)
    print("EXPLORATORY DATA ANALYSIS")
    print("="*70)
    
    # Basic stats
    print(f"\nDataset Info:")
    print(f"Total records: {len(df):,}")
    print(f"Missing values: {df.isnull().sum().sum()}")
    print(f"Unique categories: {df['category'].nunique()}")
    
    # Text length
    df['text_length'] = df['transaction_description'].str.len()
    df['word_count'] = df['transaction_description'].str.split().str.len()
    
    print(f"\nText Statistics:")
    print(f"Avg length: {df['text_length'].mean():.1f} characters")
    print(f"Avg words: {df['word_count'].mean():.1f} words")
    
    # Category distribution
    print(f"\nCategory Distribution:")
    for cat, count in df['category'].value_counts().items():
        pct = (count / len(df)) * 100
        print(f"  {cat:30s}: {count:6,} ({pct:5.2f}%)")
    
    # Visualization
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # Category distribution
    df['category'].value_counts().plot(kind='barh', ax=axes[0, 0], color='skyblue')
    axes[0, 0].set_title('Category Distribution', fontweight='bold')
    axes[0, 0].set_xlabel('Count')
    axes[0, 0].grid(alpha=0.3, axis='x')
    
    # Text length distribution
    df['text_length'].hist(bins=50, ax=axes[0, 1], color='lightcoral', edgecolor='black')
    axes[0, 1].set_title('Character Length Distribution', fontweight='bold')
    axes[0, 1].set_xlabel('Characters')
    axes[0, 1].set_ylabel('Frequency')
    axes[0, 1].axvline(df['text_length'].mean(), color='red', linestyle='--', 
                       label=f"Mean: {df['text_length'].mean():.1f}")
    axes[0, 1].legend()
    axes[0, 1].grid(alpha=0.3)
    
    # Word count distribution
    df['word_count'].hist(bins=30, ax=axes[1, 0], color='lightgreen', edgecolor='black')
    axes[1, 0].set_title('Word Count Distribution', fontweight='bold')
    axes[1, 0].set_xlabel('Words')
    axes[1, 0].set_ylabel('Frequency')
    axes[1, 0].axvline(df['word_count'].mean(), color='green', linestyle='--',
                       label=f"Mean: {df['word_count'].mean():.1f}")
    axes[1, 0].legend()
    axes[1, 0].grid(alpha=0.3)
    
    # Category pie chart
    df['category'].value_counts().plot(kind='pie', ax=axes[1, 1], autopct='%1.1f%%', startangle=90)
    axes[1, 1].set_title('Category Distribution (%)', fontweight='bold')
    axes[1, 1].set_ylabel('')
    
    plt.tight_layout()
    plt.savefig('reports/01_eda_analysis.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    print("\n✅ EDA complete! Visualizations saved.")
    
    return df


def prepare_data(df):
    """Preprocess and split data"""
    print("\n" + "="*70)
    print("DATA PREPARATION")
    print("="*70)
    
    # Preprocess text
    print("Preprocessing text...")
    df['processed_text'] = df['transaction_description'].apply(preprocess_text)
    
    # Show examples
    print("\nPreprocessing Examples:")
    for i in range(3):
        print(f"  Original : {df['transaction_description'].iloc[i]}")
        print(f"  Processed: {df['processed_text'].iloc[i]}")
    
    # Split data
    X = df['processed_text']
    y = df['category']
    
    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y, test_size=0.30, random_state=RANDOM_STATE, stratify=y
    )
    
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=0.50, random_state=RANDOM_STATE, stratify=y_temp
    )
    
    print(f"\nDataset Split:")
    print(f"  Training  : {len(X_train):6,} ({len(X_train)/len(X)*100:.1f}%)")
    print(f"  Validation: {len(X_val):6,} ({len(X_val)/len(X)*100:.1f}%)")
    print(f"  Test      : {len(X_test):6,} ({len(X_test)/len(X)*100:.1f}%)")
    
    print("\n✅ Data preparation complete!")
    
    return X_train, X_val, X_test, y_train, y_val, y_test


def train_baseline(X_train, X_val, X_test, y_train, y_val, y_test):
    """Train baseline model: TF-IDF + Logistic Regression"""
    print("\n" + "="*70)
    print("BASELINE MODEL: TF-IDF + Logistic Regression")
    print("="*70)
    
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 2),
            min_df=2,
            max_df=0.9,
            stop_words='english'
        )),
        ('clf', LogisticRegression(
            max_iter=1000,
            random_state=RANDOM_STATE,
            n_jobs=-1
        ))
    ])
    
    start_time = time.time()
    pipeline.fit(X_train, y_train)
    training_time = time.time() - start_time
    
    train_score = pipeline.score(X_train, y_train)
    val_score = pipeline.score(X_val, y_val)
    test_score = pipeline.score(X_test, y_test)
    
    print(f"✅ Training completed in {training_time:.2f}s")
    print(f"\nPerformance:")
    print(f"  Training Accuracy  : {train_score:.4f}")
    print(f"  Validation Accuracy: {val_score:.4f}")
    print(f"  Test Accuracy      : {test_score:.4f}")
    
    # Save baseline model
    joblib.dump(pipeline, 'models/baseline_model_tfidf_logreg.joblib')
    print("\n✅ Baseline model saved!")
    
    return pipeline


def compare_models(X_train, X_val, X_test, y_train, y_val, y_test):
    """Compare multiple models"""
    print("\n" + "="*70)
    print("MODEL COMPARISON")
    print("="*70)
    
    models = {
        'Logistic Regression': Pipeline([
            ('tfidf', TfidfVectorizer(max_features=5000, ngram_range=(1, 2), stop_words='english')),
            ('clf', LogisticRegression(max_iter=1000, random_state=RANDOM_STATE, n_jobs=-1))
        ]),
        'Naive Bayes': Pipeline([
            ('tfidf', TfidfVectorizer(max_features=5000, ngram_range=(1, 2), stop_words='english')),
            ('clf', MultinomialNB())
        ]),
        'Linear SVM': Pipeline([
            ('tfidf', TfidfVectorizer(max_features=5000, ngram_range=(1, 2), stop_words='english')),
            ('clf', LinearSVC(max_iter=1000, random_state=RANDOM_STATE))
        ]),
        'Random Forest': Pipeline([
            ('tfidf', TfidfVectorizer(max_features=3000, ngram_range=(1, 2), stop_words='english')),
            ('clf', RandomForestClassifier(n_estimators=100, random_state=RANDOM_STATE, n_jobs=-1))
        ])
    }
    
    results = []
    
    for name, pipeline in models.items():
        print(f"\nTraining {name}...")
        
        start_time = time.time()
        pipeline.fit(X_train, y_train)
        training_time = time.time() - start_time
        
        y_pred_test = pipeline.predict(X_test)
        
        test_acc = accuracy_score(y_test, y_pred_test)
        test_precision = precision_score(y_test, y_pred_test, average='weighted', zero_division=0)
        test_recall = recall_score(y_test, y_pred_test, average='weighted', zero_division=0)
        test_f1 = f1_score(y_test, y_pred_test, average='weighted', zero_division=0)
        
        results.append({
            'Model': name,
            'Test Acc': test_acc,
            'Precision': test_precision,
            'Recall': test_recall,
            'F1-Score': test_f1,
            'Time (s)': training_time
        })
        
        print(f"  ✅ {name}: Test Acc={test_acc:.4f}, Time={training_time:.2f}s")
    
    results_df = pd.DataFrame(results).sort_values('Test Acc', ascending=False).reset_index(drop=True)
    
    print("\n" + "="*70)
    print("RESULTS")
    print("="*70)
    print(results_df.to_string(index=False))
    
    results_df.to_csv('reports/model_comparison_results.csv', index=False)
    
    # Visualize
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    results_df.plot(x='Model', y='Test Acc', kind='barh', ax=axes[0], color='steelblue', legend=False)
    axes[0].set_title('Test Accuracy Comparison', fontweight='bold')
    axes[0].set_xlabel('Accuracy')
    axes[0].grid(alpha=0.3, axis='x')
    
    metrics_df = results_df[['Model', 'Precision', 'Recall', 'F1-Score']].set_index('Model')
    metrics_df.plot(kind='barh', ax=axes[1], width=0.8)
    axes[1].set_title('Metrics Comparison', fontweight='bold')
    axes[1].set_xlabel('Score')
    axes[1].legend(loc='lower right')
    axes[1].grid(alpha=0.3, axis='x')
    
    plt.tight_layout()
    plt.savefig('reports/02_model_comparison.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    print("\n✅ Model comparison complete!")
    
    return results_df, models


def tune_best_model(best_model_name, models, X_train, X_test, y_train, y_test):
    """Hyperparameter tuning with GridSearchCV"""
    print("\n" + "="*70)
    print(f"HYPERPARAMETER TUNING: {best_model_name}")
    print("="*70)
    
    base_pipeline = models[best_model_name]
    
    if best_model_name == 'Logistic Regression':
        param_grid = {
            'tfidf__max_features': [3000, 5000, 7000],
            'tfidf__ngram_range': [(1, 1), (1, 2)],
            'clf__C': [0.1, 1.0, 10.0]
        }
    elif best_model_name == 'Linear SVM':
        param_grid = {
            'tfidf__max_features': [3000, 5000, 7000],
            'tfidf__ngram_range': [(1, 1), (1, 2)],
            'clf__C': [0.1, 1.0, 10.0]
        }
    elif best_model_name == 'Naive Bayes':
        param_grid = {
            'tfidf__max_features': [3000, 5000, 7000],
            'tfidf__ngram_range': [(1, 1), (1, 2)],
            'clf__alpha': [0.1, 0.5, 1.0]
        }
    else:
        param_grid = {
            'tfidf__max_features': [2000, 3000],
            'tfidf__ngram_range': [(1, 1), (1, 2)],
            'clf__n_estimators': [100, 200]
        }
    
    grid_search = GridSearchCV(
        base_pipeline,
        param_grid,
        cv=3,
        scoring='accuracy',
        n_jobs=-1,
        verbose=1
    )
    
    start_time = time.time()
    grid_search.fit(X_train, y_train)
    tuning_time = time.time() - start_time
    
    print(f"\n✅ GridSearchCV completed in {tuning_time:.2f}s")
    print(f"\nBest Parameters: {grid_search.best_params_}")
    print(f"Best CV Score: {grid_search.best_score_:.4f}")
    
    tuned_model = grid_search.best_estimator_
    test_score = tuned_model.score(X_test, y_test)
    
    print(f"Test Accuracy (Tuned): {test_score:.4f}")
    
    joblib.dump(tuned_model, 'models/best_model_tuned.joblib')
    print("\n✅ Tuned model saved!")
    
    return tuned_model, grid_search.best_params_, test_score


def evaluate_final_model(model, X_test, y_test):
    """Final evaluation with detailed metrics and confusion matrix"""
    print("\n" + "="*70)
    print("FINAL MODEL EVALUATION")
    print("="*70)
    
    y_pred = model.predict(X_test)
    
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    rec = recall_score(y_test, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
    
    print(f"\nTest Set Metrics:")
    print(f"  Accuracy : {acc:.4f}")
    print(f"  Precision: {prec:.4f}")
    print(f"  Recall   : {rec:.4f}")
    print(f"  F1-Score : {f1:.4f}")
    
    print(f"\nClassification Report:")
    print(classification_report(y_test, y_pred, zero_division=0))
    
    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=model.classes_)
    
    fig, ax = plt.subplots(figsize=(12, 10))
    disp.plot(ax=ax, cmap='Greens', values_format='d')
    plt.title('Final Confusion Matrix', fontsize=14, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('reports/03_final_confusion_matrix.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    print("\n✅ Evaluation complete! Confusion matrix saved.")
    
    return {'accuracy': acc, 'precision': prec, 'recall': rec, 'f1_score': f1}


def save_final_model(model, best_model_name, metrics, params):
    """Save final model with metadata"""
    model_path = 'models/final_expense_classifier.joblib'
    joblib.dump(model, model_path)
    
    metadata = {
        'model_name': best_model_name,
        'test_metrics': metrics,
        'best_parameters': params,
        'categories': list(model.classes_),
        'random_state': RANDOM_STATE
    }
    
    with open('models/model_metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"\n✅ Final model saved: {model_path}")
    print(f"✅ Metadata saved: models/model_metadata.json")


def create_predict_function():
    """Create and test prediction function"""
    print("\n" + "="*70)
    print("PREDICTION FUNCTION")
    print("="*70)
    
    code = '''
def predict(text, model_path='models/final_expense_classifier.joblib'):
    """
    Predict category and confidence for transaction description
    
    Args:
        text (str): Transaction description
        model_path (str): Path to saved model
    
    Returns:
        dict: category, confidence, and top_3 predictions
    """
    import joblib
    import numpy as np
    import re
    
    # Load model
    model = joblib.load(model_path)
    
    # Preprocess
    text = str(text).lower()
    text = re.sub(r'[^a-z\\s]', ' ', text)
    text = ' '.join(text.split())
    
    # Predict
    prediction = model.predict([text])[0]
    probabilities = model.predict_proba([text])[0]
    confidence = max(probabilities)
    
    # Top 3
    top_3_idx = np.argsort(probabilities)[-3:][::-1]
    top_3 = [(model.classes_[i], float(probabilities[i])) for i in top_3_idx]
    
    return {
        'category': prediction,
        'confidence': float(confidence),
        'top_3': top_3
    }
'''
    
    with open('src/predict.py', 'w') as f:
        f.write(code)
    
    print("✅ Prediction function saved: src/predict.py")
    
    # Test it
    from src.predict import predict
    
    print("\nTesting prediction function:")
    test_examples = [
        "Starbucks Coffee",
        "Uber ride",
        "Amazon purchase",
        "Doctor visit",
        "Electric bill"
    ]
    
    for example in test_examples:
        result = predict(example)
        print(f"\n  Text: {example}")
        print(f"  Category: {result['category']}")
        print(f"  Confidence: {result['confidence']:.2%}")
    
    print("\n✅ Prediction function working!")


def main():
    """Main pipeline execution"""
    print("\n" + "="*70)
    print("SMART EXPENSE CLASSIFIER - COMPLETE ML PIPELINE")
    print("="*70)
    
    # 1. Load data
    df = load_data(sample_size=100000)
    
    # 2. EDA
    df = perform_eda(df)
    
    # 3. Prepare data
    X_train, X_val, X_test, y_train, y_val, y_test = prepare_data(df)
    
    # 4. Train baseline
    baseline_model = train_baseline(X_train, X_val, X_test, y_train, y_val, y_test)
    
    # 5. Compare models
    results_df, models = compare_models(X_train, X_val, X_test, y_train, y_val, y_test)
    
    # 6. Tune best model
    best_model_name = results_df.iloc[0]['Model']
    tuned_model, best_params, test_score = tune_best_model(
        best_model_name, models, X_train, X_test, y_train, y_test
    )
    
    # 7. Final evaluation
    final_metrics = evaluate_final_model(tuned_model, X_test, y_test)
    
    # 8. Save final model
    save_final_model(tuned_model, best_model_name, final_metrics, best_params)
    
    # 9. Create prediction function
    create_predict_function()
    
    # Summary
    print("\n" + "="*70)
    print("PIPELINE COMPLETE!")
    print("="*70)
    print(f"✅ Best Model: {best_model_name}")
    print(f"✅ Test Accuracy: {final_metrics['accuracy']:.4f}")
    print(f"✅ F1-Score: {final_metrics['f1_score']:.4f}")
    print(f"✅ Models saved in: models/")
    print(f"✅ Reports saved in: reports/")
    print(f"\n📋 Next: Create Streamlit demo app!")
    print("="*70)


if __name__ == "__main__":
    main()
