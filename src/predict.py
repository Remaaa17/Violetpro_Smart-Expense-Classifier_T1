
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
    text = re.sub(r'[^a-z\s]', ' ', text)
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
