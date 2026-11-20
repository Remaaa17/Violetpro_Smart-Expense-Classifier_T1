
Preprocessing Steps for Mobile:
1. Convert text to lowercase
2. Remove all non-alphabetic characters (keep only a-z and spaces)
3. Remove extra spaces
4. Split into words
5. Apply TF-IDF vectorization using vocabulary
6. Run through classifier

Example (Dart):
```dart
String preprocessText(String text) {
  // Lowercase
  text = text.toLowerCase();
  
  // Remove non-alphabetic characters
  text = text.replaceAll(RegExp(r'[^a-z\s]'), ' ');
  
  // Remove extra spaces
  text = text.trim().replaceAll(RegExp(r'\s+'), ' ');
  
  return text;
}
```
