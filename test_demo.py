"""
Test script for the demo app functionality
"""

import joblib
import re
import pandas as pd

def preprocess_text(text):
    """Preprocess transaction description"""
    text = str(text).lower()
    text = re.sub(r'[^a-z\s]', ' ', text)
    text = ' '.join(text.split())
    return text

def test_model():
    """Test if model loads and predicts correctly"""
    print("="*70)
    print("TESTING SMART EXPENSE CLASSIFIER DEMO")
    print("="*70)
    
    # Load model
    print("\n1. Loading model...")
    try:
        model = joblib.load('models/final_expense_classifier.joblib')
        print("   Model loaded successfully!")
        print(f"   Model type: {type(model)}")
        print(f"   Number of categories: {len(model.classes_)}")
    except Exception as e:
        print(f"   ERROR: {e}")
        return False
    
    # Test predictions
    print("\n2. Testing predictions...")
    test_cases = [
        ("Starbucks coffee", "Food & Dining"),
        ("Uber ride", "Transportation"),
        ("Amazon electronics", "Shopping & Retail"),
        ("Netflix subscription", "Entertainment & Recreation"),
        ("Doctor visit", "Healthcare & Medical"),
        ("Electric bill", "Utilities & Services"),
        ("Monthly salary", "Income"),
        ("Bank fees", "Financial Services"),
        ("Charity donation", "Charity & Donations"),
        ("Tax payment", "Government & Legal")
    ]
    
    correct = 0
    total = len(test_cases)
    
    for text, expected in test_cases:
        processed = preprocess_text(text)
        prediction = model.predict([processed])[0]
        proba = model.predict_proba([processed])[0]
        confidence = max(proba)
        
        is_correct = prediction == expected
        if is_correct:
            correct += 1
        
        status = "✓" if is_correct else "✗"
        print(f"\n   {status} Input: {text}")
        print(f"     Expected: {expected}")
        print(f"     Predicted: {prediction}")
        print(f"     Confidence: {confidence:.1%}")
    
    accuracy = (correct / total) * 100
    print(f"\n3. Test Results:")
    print(f"   Correct: {correct}/{total}")
    print(f"   Accuracy: {accuracy:.1f}%")
    
    # Test preprocessing
    print("\n4. Testing preprocessing...")
    test_text = "Starbucks Coffee @ $5.99!"
    processed = preprocess_text(test_text)
    print(f"   Original: {test_text}")
    print(f"   Processed: {processed}")
    
    # Test batch prediction
    print("\n5. Testing batch prediction...")
    test_df = pd.DataFrame({
        'transaction_description': [
            'Starbucks coffee',
            'Uber ride',
            'Amazon purchase',
            'Netflix',
            'Doctor appointment'
        ]
    })
    
    predictions = []
    confidences = []
    
    for desc in test_df['transaction_description']:
        processed = preprocess_text(desc)
        pred = model.predict([processed])[0]
        proba = model.predict_proba([processed])[0]
        conf = max(proba)
        predictions.append(pred)
        confidences.append(conf)
    
    test_df['category'] = predictions
    test_df['confidence'] = [f"{c:.1%}" for c in confidences]
    
    print(test_df.to_string(index=False))
    
    print("\n" + "="*70)
    print("DEMO TEST COMPLETE!")
    print("="*70)
    print("\nNext steps:")
    print("1. Run the Streamlit app: streamlit run app/demo_app.py")
    print("2. Open browser at: http://localhost:8501")
    print("3. Test with different transaction descriptions")
    print("4. Try batch upload with a CSV file")
    print("="*70)
    
    return True

if __name__ == "__main__":
    test_model()
