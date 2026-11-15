"""
Train Baseline Model: TF-IDF + Logistic Regression
Quick script to reach Day 5-6 milestone
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix
)
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set random seed for reproducibility
RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)


def load_data(filepath='data/combined_transactions.csv'):
    """Load transaction data"""
    print("="*70)
    print("📂 LOADING DATA")
    print("="*70)
    df = pd.read_csv(filepath)
    print(f"✅ Loaded {len(df)} transactions")
    print(f"   Categories: {df['category'].nunique()}")
    print(f"\n📊 Category Distribution:")
    print(df['category'].value_counts())
    return df


def split_data(df):
    """Split data into train/val/test sets"""
    print("\n" + "="*70)
    print("🔀 SPLITTING DATA")
    print("="*70)
    
    X = df['description']
    y = df['category']
    
    # Split: 70% train, 15% validation, 15% test
    X_temp, X_test, y_temp, y_test = train_test_split(
        X, y, test_size=0.15, stratify=y, random_state=RANDOM_STATE
    )
    
    X_train, X_val, y_train, y_val = train_test_split(
        X_temp, y_temp, test_size=0.176, stratify=y_temp, random_state=RANDOM_STATE
    )
    
    print(f"Training:   {len(X_train):>5} samples ({len(X_train)/len(X)*100:.1f}%)")
    print(f"Validation: {len(X_val):>5} samples ({len(X_val)/len(X)*100:.1f}%)")
    print(f"Test:       {len(X_test):>5} samples ({len(X_test)/len(X)*100:.1f}%)")
    print(f"Total:      {len(X):>5} samples")
    
    return X_train, X_val, X_test, y_train, y_val, y_test


def create_pipeline():
    """Create ML pipeline"""
    print("\n" + "="*70)
    print("🔧 CREATING PIPELINE")
    print("="*70)
    
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(
            max_features=1000,
            ngram_range=(1, 2),
            min_df=2,
            max_df=0.9,
            lowercase=True,
            strip_accents='unicode'
        )),
        ('clf', LogisticRegression(
            max_iter=1000,
            random_state=RANDOM_STATE,
            solver='lbfgs'
        ))
    ])
    
    print("✅ Pipeline created:")
    print("   1. TF-IDF Vectorizer (max_features=1000, ngram=(1,2))")
    print("   2. Logistic Regression (multinomial)")
    
    return pipeline


def train_model(pipeline, X_train, y_train):
    """Train the model"""
    print("\n" + "="*70)
    print("🎓 TRAINING MODEL")
    print("="*70)
    print("Training in progress...")
    
    pipeline.fit(X_train, y_train)
    
    print("✅ Training complete!")
    return pipeline


def evaluate_model(pipeline, X_train, y_train, X_val, y_val, X_test, y_test):
    """Evaluate model performance"""
    print("\n" + "="*70)
    print("📊 EVALUATING MODEL")
    print("="*70)
    
    # Predictions
    y_train_pred = pipeline.predict(X_train)
    y_val_pred = pipeline.predict(X_val)
    y_test_pred = pipeline.predict(X_test)
    
    # Calculate metrics
    sets = [('Training', y_train, y_train_pred),
            ('Validation', y_val, y_val_pred),
            ('Test', y_test, y_test_pred)]
    
    results = {}
    
    for set_name, y_true, y_pred in sets:
        acc = accuracy_score(y_true, y_pred)
        prec = precision_score(y_true, y_pred, average='weighted', zero_division=0)
        rec = recall_score(y_true, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_true, y_pred, average='weighted', zero_division=0)
        
        results[set_name] = {
            'accuracy': acc,
            'precision': prec,
            'recall': rec,
            'f1_score': f1
        }
        
        print(f"\n{set_name} Set:")
        print(f"  Accuracy:  {acc:.4f} ({acc*100:.2f}%)")
        print(f"  Precision: {prec:.4f}")
        print(f"  Recall:    {rec:.4f}")
        print(f"  F1-Score:  {f1:.4f}")
    
    # Detailed classification report
    print("\n" + "="*70)
    print("DETAILED CLASSIFICATION REPORT (Test Set)")
    print("="*70)
    print(classification_report(y_test, y_test_pred))
    
    return results, y_test, y_test_pred


def plot_confusion_matrix(y_true, y_pred, categories):
    """Plot confusion matrix"""
    print("\n📊 Generating confusion matrix...")
    
    cm = confusion_matrix(y_true, y_pred, labels=categories)
    
    plt.figure(figsize=(12, 10))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=categories, yticklabels=categories,
                cbar_kws={'label': 'Count'})
    plt.title('Confusion Matrix - Baseline Model (TF-IDF + LogReg)',
              fontsize=16, fontweight='bold', pad=20)
    plt.ylabel('True Category', fontsize=12)
    plt.xlabel('Predicted Category', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    
    os.makedirs('models', exist_ok=True)
    plt.savefig('models/confusion_matrix_baseline.png', dpi=300, bbox_inches='tight')
    print("✅ Saved: models/confusion_matrix_baseline.png")
    plt.close()


def save_model(pipeline, results):
    """Save model and results"""
    print("\n" + "="*70)
    print("💾 SAVING MODEL")
    print("="*70)
    
    os.makedirs('models', exist_ok=True)
    
    # Save pipeline
    model_path = 'models/baseline_model.joblib'
    joblib.dump(pipeline, model_path)
    print(f"✅ Model saved: {model_path}")
    
    # Save metrics
    results_df = pd.DataFrame(results).T
    results_df.to_csv('models/baseline_metrics.csv')
    print(f"✅ Metrics saved: models/baseline_metrics.csv")
    
    return model_path


def test_predictions(pipeline):
    """Test on sample descriptions"""
    print("\n" + "="*70)
    print("🧪 TESTING PREDICTIONS")
    print("="*70)
    
    test_samples = [
        "Uber ride to downtown",
        "Starbucks coffee",
        "Netflix subscription",
        "CVS Pharmacy medicine",
        "Electric bill payment",
        "Amazon purchase",
        "Rent payment",
        "Online course Udemy",
        "مطعم ستاربكس",  # Arabic: Starbucks restaurant
        "رحلة أوبر",      # Arabic: Uber ride
        "اشتراك نتفليكس",  # Arabic: Netflix subscription
    ]
    
    print("\nSample Predictions:\n")
    for i, sample in enumerate(test_samples, 1):
        pred = pipeline.predict([sample])[0]
        proba = pipeline.predict_proba([sample])[0]
        confidence = max(proba) * 100
        print(f"{i:>2}. \"{sample}\"")
        print(f"    → {pred} ({confidence:.1f}% confidence)\n")


def main():
    """Main execution"""
    print("\n" + "🚀"*35)
    print("   BASELINE MODEL TRAINING - DAY 5-6")
    print("   VioletPro Internship Task")
    print("🚀"*35 + "\n")
    
    # Load data
    df = load_data('data/combined_transactions.csv')
    
    # Split data
    X_train, X_val, X_test, y_train, y_val, y_test = split_data(df)
    
    # Create pipeline
    pipeline = create_pipeline()
    
    # Train model
    pipeline = train_model(pipeline, X_train, y_train)
    
    # Evaluate
    results, y_test_true, y_test_pred = evaluate_model(
        pipeline, X_train, y_train, X_val, y_val, X_test, y_test
    )
    
    # Plot confusion matrix
    categories = sorted(df['category'].unique())
    plot_confusion_matrix(y_test_true, y_test_pred, categories)
    
    # Save model
    model_path = save_model(pipeline, results)
    
    # Test predictions
    test_predictions(pipeline)
    
    # Final summary
    print("\n" + "="*70)
    print("✅ BASELINE MODEL COMPLETE!")
    print("="*70)
    
    test_acc = results['Test']['accuracy']
    test_f1 = results['Test']['f1_score']
    
    print(f"\n📊 Final Results:")
    print(f"   Test Accuracy: {test_acc:.4f} ({test_acc*100:.2f}%)")
    print(f"   Test F1-Score: {test_f1:.4f}")
    
    print(f"\n📁 Files Created:")
    print(f"   ✅ {model_path}")
    print(f"   ✅ models/baseline_metrics.csv")
    print(f"   ✅ models/confusion_matrix_baseline.png")
    
    print(f"\n🎯 Milestone Reached:")
    print(f"   ✅ Day 5-6 Complete: Baseline Model Built & Evaluated")
    
    print(f"\n📝 Next Steps (Day 7-9):")
    print(f"   1. Compare with other models (Naive Bayes, Random Forest, SVM)")
    print(f"   2. Hyperparameter tuning with GridSearchCV")
    print(f"   3. Build Streamlit demo app")
    
    print("\n" + "🎉"*35)
    print("   READY FOR TODAY'S REPORT!")
    print("🎉"*35 + "\n")


if __name__ == "__main__":
    main()
