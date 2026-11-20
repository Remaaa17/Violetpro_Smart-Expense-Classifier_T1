# Smart Expense Classifier - Flutter App

A mobile demo app showcasing the Smart Expense Classifier ML model running entirely offline on-device.

## Features

- ✅ **On-Device ML**: Model runs completely offline, no internet required
- ✅ **Bilingual Support**: English and Arabic transaction classification
- ✅ **Real-time Predictions**: Instant classification with confidence scores
- ✅ **10 Categories**: Classifies transactions into 10 expense categories
- ✅ **97.52% Accuracy**: Production-grade ML model
- ✅ **Sample Transactions**: Built-in examples for testing
- ✅ **Beautiful UI**: Material Design 3 with category-specific colors

## Screenshots

![App Screenshot - Coming Soon]

## Categories

1. 🍽️ Food & Dining
2. 🚗 Transportation
3. 🛍️ Shopping & Retail
4. 🎬 Entertainment & Recreation
5. 🏥 Healthcare & Medical
6. 🔧 Utilities & Services
7. 🏦 Financial Services
8. 💰 Income
9. ⚖️ Government & Legal
10. ❤️ Charity & Donations

## Installation

### Prerequisites
- Flutter SDK (3.0.0 or higher)
- Dart SDK
- Android Studio / VS Code with Flutter extensions

### Setup

1. **Clone the repository** (if not already done):
   ```bash
   cd C:\Users\Cairo Lap\violetpro_Internship\Smart-Expense-Classifier
   ```

2. **Navigate to Flutter app**:
   ```bash
   cd flutter_expense_app
   ```

3. **Install dependencies**:
   ```bash
   flutter pub get
   ```

4. **Verify assets are in place**:
   Make sure these files exist in `assets/`:
   - `tfidf_vectorizer.json`
   - `classifier.json`
   - `model_metadata.json`
   - `tfidf_vectorizer_arabic.json`
   - `classifier_arabic.json`

5. **Run the app**:
   ```bash
   flutter run
   ```

## Usage

### 1. Launch the App
Open the app on your device or emulator.

### 2. Choose Language
Use the toggle switch to select English or Arabic model.

### 3. Enter Transaction
Type a transaction description, for example:
- English: "Starbucks Coffee"
- Arabic: "شراء من السوبرماركت"

### 4. Classify
Press the "Classify" button to get instant prediction.

### 5. View Results
- Main predicted category with confidence
- Top 3 predictions with confidence bars
- Category-specific icon and color

### 6. Try Samples
Press "Sample" button to test with random examples.

## How It Works

### Architecture

```
User Input (Text)
      ↓
Preprocessing (Lowercase, clean)
      ↓
TF-IDF Vectorization (555 features)
      ↓
Logistic Regression Model
      ↓
Softmax Activation
      ↓
Category + Confidence (%)
```

### Model Details

- **Algorithm**: TF-IDF + Logistic Regression
- **Input**: Transaction description (text)
- **Output**: Category + confidence score
- **Features**: 555 TF-IDF features (unigrams)
- **Model Size**: ~600 KB (all files)
- **Inference Time**: 10-50ms on mobile
- **Accuracy**: 97.52% (English), 95.80% (Arabic)

### Text Preprocessing

```dart
1. Convert to lowercase
2. Remove punctuation and numbers
3. Remove extra spaces
4. Split into words
```

### Feature Extraction

```dart
1. Count word frequencies (TF)
2. Apply IDF weights from trained model
3. Normalize vector (L2 norm)
4. Create 555-dimensional feature vector
```

### Classification

```dart
1. Matrix multiplication (features × weights)
2. Add bias/intercept
3. Apply softmax for probabilities
4. Select category with highest probability
```

## File Structure

```
flutter_expense_app/
├── lib/
│   ├── main.dart           - Main UI and app logic
│   └── ml_model.dart       - ML model implementation
├── assets/
│   ├── tfidf_vectorizer.json           - English TF-IDF
│   ├── classifier.json                 - English classifier
│   ├── model_metadata.json             - Model info
│   ├── tfidf_vectorizer_arabic.json    - Arabic TF-IDF
│   └── classifier_arabic.json          - Arabic classifier
├── pubspec.yaml            - Dependencies
└── README.md               - This file
```

## Dependencies

```yaml
dependencies:
  flutter:
    sdk: flutter
  cupertino_icons: ^1.0.2
```

No external ML libraries required! Pure Dart implementation.

## Performance

### Model Loading
- First load: ~500-1000ms
- Cached: <100ms

### Inference Speed
- Android: 10-30ms per prediction
- iOS: 10-30ms per prediction
- Web: 20-50ms per prediction

### Memory Usage
- Model in memory: ~1-2 MB
- Total app: ~50-100 MB

### Battery Impact
- Minimal (no network requests)
- Efficient CPU-only inference

## Testing

### Sample Transactions (English)
```
Starbucks Coffee → Food & Dining
Uber ride → Transportation
Amazon purchase → Shopping & Retail
CVS Pharmacy → Healthcare & Medical
Electric bill → Utilities & Services
Netflix subscription → Entertainment & Recreation
Salary deposit → Income
DMV fee → Government & Legal
Red Cross donation → Charity & Donations
```

### Sample Transactions (Arabic)
```
شراء من السوبرماركت → Food & Dining
ركبت المترو → Transportation
اشتريت من المول → Shopping & Retail
دفعت فاتورة الكهرباء → Utilities & Services
كشف عند الدكتور → Healthcare & Medical
راتب الشهر → Income
```

## Troubleshooting

### Model Not Loading
**Error**: "Error loading model"
**Solution**: Check that assets are properly configured in `pubspec.yaml`

### Low Confidence Scores
**Issue**: Predictions have <70% confidence
**Reason**: Transaction description is too short or ambiguous
**Solution**: Provide more descriptive text

### Wrong Predictions
**Issue**: Category doesn't match expectation
**Reason**: Model may need more context
**Solution**: Add merchant name or more details

### Arabic Text Not Showing
**Issue**: Arabic appears as boxes/question marks
**Solution**: Ensure device supports Arabic fonts

## Building for Release

### Android APK
```bash
flutter build apk --release
```
Output: `build/app/outputs/flutter-apk/app-release.apk`

### iOS IPA
```bash
flutter build ios --release
```

### Web
```bash
flutter build web --release
```
Output: `build/web/`

## Technical Notes

### Why No TensorFlow Lite?
- Scikit-learn models (TF-IDF + LogReg) don't convert to TFLite
- Pure Dart implementation is:
  - Faster (no bridge overhead)
  - Smaller (no TFLite runtime ~10 MB)
  - More portable (works on all platforms)

### Math Behind the Model

**TF-IDF Feature Extraction**:
```
TF-IDF(word, doc) = TF(word, doc) × IDF(word)
TF = count(word) / total_words
IDF = log((N + 1) / (df + 1)) + 1
```

**Logistic Regression**:
```
score = weights · features + bias
probability = softmax(score)
prediction = argmax(probability)
```

## Future Enhancements

Possible improvements:
- [ ] Transaction history storage
- [ ] Batch predictions
- [ ] Custom categories
- [ ] Export predictions to CSV
- [ ] Dark mode
- [ ] Multiple languages (Spanish, French, etc.)
- [ ] Voice input
- [ ] Camera OCR for receipts

## License

Part of the Smart Expense Classifier project.

## Credits

- **ML Model**: Trained on 100K+ transactions
- **Framework**: Flutter
- **Platform**: Cross-platform (Android, iOS, Web)
- **ML Implementation**: Pure Dart (no external ML libraries)

## Contact

For issues or questions:
- Project Repository: [GitHub Link]
- VioletPro Internship Project
- November 2026

---

**Built with ❤️ using Flutter and Machine Learning**
