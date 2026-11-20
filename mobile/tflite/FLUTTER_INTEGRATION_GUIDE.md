
# TensorFlow Lite Integration Guide for Flutter

## Prerequisites
Add to your `pubspec.yaml`:

```yaml
dependencies:
  tflite_flutter: ^0.10.0
  tflite_flutter_helper: ^0.3.1
```

## Model Files Required
Place in `assets/` folder:
- `english_model.tflite`
- `english_vocabulary.json`
- `arabic_model.tflite`
- `arabic_vocabulary.json`

## Update pubspec.yaml Assets
```yaml
flutter:
  assets:
    - assets/english_model.tflite
    - assets/english_vocabulary.json
    - assets/arabic_model.tflite
    - assets/arabic_vocabulary.json
    - assets/logo.png
```

## Dart Code Example

```dart
import 'package:tflite_flutter/tflite_flutter.dart';
import 'dart:convert';
import 'package:flutter/services.dart';

class TFLiteExpenseClassifier {
  Interpreter? _interpreter;
  Map<String, dynamic>? _vocabulary;
  List<String>? _classes;
  
  Future<void> loadModel(bool isArabic) async {
    try {
      // Load TFLite model
      final modelFile = isArabic 
          ? 'assets/arabic_model.tflite'
          : 'assets/english_model.tflite';
      
      _interpreter = await Interpreter.fromAsset(modelFile);
      
      // Load vocabulary
      final vocabFile = isArabic
          ? 'assets/arabic_vocabulary.json'
          : 'assets/english_vocabulary.json';
      
      final vocabJson = await rootBundle.loadString(vocabFile);
      _vocabulary = json.decode(vocabJson);
      _classes = List<String>.from(_vocabulary!['classes']);
      
      print('Model loaded: $modelFile');
    } catch (e) {
      print('Error loading model: $e');
    }
  }
  
  Map<String, dynamic> predict(String text) {
    // 1. Preprocess text (same as before)
    String processed = preprocessText(text);
    
    // 2. Convert to TF-IDF features
    List<double> features = applyTfidf(processed);
    
    // 3. Prepare input tensor
    var input = [features];
    var output = List.filled(_classes!.length, 0.0).reshape([1, _classes!.length]);
    
    // 4. Run inference
    _interpreter!.run(input, output);
    
    // 5. Get probabilities
    List<double> probabilities = output[0];
    
    // 6. Find top prediction
    int maxIndex = 0;
    double maxProb = probabilities[0];
    for (int i = 1; i < probabilities.length; i++) {
      if (probabilities[i] > maxProb) {
        maxProb = probabilities[i];
        maxIndex = i;
      }
    }
    
    return {
      'category': _classes![maxIndex],
      'confidence': maxProb,
      'top3': getTop3(probabilities)
    };
  }
  
  // Preprocessing and TF-IDF remain the same as before
  String preprocessText(String text) {
    // Same implementation as ml_model.dart
  }
  
  List<double> applyTfidf(String text) {
    // Same implementation as ml_model.dart
  }
}
```

## Performance Comparison

### JSON Approach (Current):
- Inference time: ~20-50ms
- Model size: ~200KB (JSON)
- Dependencies: None
- Accuracy: Same as training

### TFLite Approach:
- Inference time: ~5-15ms (3-5x faster)
- Model size: ~150KB (TFLite)
- Dependencies: tflite_flutter package
- Accuracy: Same as training
- Benefits: Optimized, hardware acceleration

## When to Use TFLite vs JSON

**Use JSON (Current):**
- Simple deployment
- No additional dependencies
- Performance is acceptable
- Easy to debug

**Use TFLite:**
- Need maximum performance
- Processing many predictions
- Want hardware acceleration
- Professional production app

## Note
The current JSON implementation is perfectly fine for this project!
TFLite is an optimization, not a necessity.
