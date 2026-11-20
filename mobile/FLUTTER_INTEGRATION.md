
# Flutter Integration Guide

## Files Needed
Copy these files to your Flutter app's `assets/` folder:
- `tfidf_vectorizer.json` - TF-IDF vocabulary and parameters
- `classifier.json` - Logistic regression weights
- `model_metadata.json` - Model information

## Add to pubspec.yaml
```yaml
flutter:
  assets:
    - assets/tfidf_vectorizer.json
    - assets/classifier.json
    - assets/model_metadata.json
```

## Dependencies
Add to pubspec.yaml:
```yaml
dependencies:
  flutter:
    sdk: flutter
  ml_algo: ^16.0.0  # For ML algorithms
  # OR implement TF-IDF and LogReg manually
```

## Usage Example
```dart
// Load model
final tfidfJson = await rootBundle.loadString('assets/tfidf_vectorizer.json');
final classifierJson = await rootBundle.loadString('assets/classifier.json');

// Preprocess input
String text = "Starbucks Coffee";
text = preprocessText(text);

// Apply TF-IDF
List<double> features = applyTfidf(text, tfidfJson);

// Predict
String category = predict(features, classifierJson);
```

## Performance
- Model size: ~600 KB (all files)
- Inference time: ~10-50ms on mobile
- No internet required (fully offline)
