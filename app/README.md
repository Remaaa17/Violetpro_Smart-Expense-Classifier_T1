# 🎯 Application Demos

This folder contains various demo applications for the Smart Expense Classifier.

---

## 📱 Available Applications

### 1️⃣ **violetpro_app.py** ⭐ **NEW - VioletPro Branded**
**Purpose:** Clean, professional Streamlit app with VioletPro branding and styling

**Features:**
- Custom VioletPro theme (navy + yellow branding)
- Professional UI with logo and styled components
- Simple transaction input → category prediction
- Confidence score with progress bar

**Usage:**
```bash
streamlit run app/violetpro_app.py
```

**Dependencies:**
- `style.py` - Custom styling module
- `assets/logo.png` - VioletPro logo
- `.streamlit/config.toml` - Theme configuration

---

### 2️⃣ **streamlit_app.py**
**Purpose:** Standard Streamlit demo application

**Usage:**
```bash
streamlit run app/streamlit_app.py
```

---

### 3️⃣ **fintech_app.py**
**Purpose:** FinTech-focused demo application

**Usage:**
```bash
streamlit run app/fintech_app.py
```

---

### 4️⃣ **demo_app.py**
**Purpose:** Basic demo application

**Usage:**
```bash
streamlit run app/demo_app.py
```

---

## 🎨 Styling & Branding

### **style.py** - Custom Theme Module
Contains VioletPro branding elements:
- **Colors:**
  - Navy: `#1a3460` (primary)
  - Yellow: `#fae162` (accent)
  - Soft backgrounds and borders
  
- **Components:**
  - `apply_theme()` - Apply custom CSS
  - `header(title, subtitle)` - Branded header with logo
  - `result_card(category, confidence)` - Styled result display

**Usage in your app:**
```python
import streamlit as st
from style import apply_theme, header, result_card

st.set_page_config(page_title="App Name", page_icon="💳")
apply_theme()
header("Title", "Subtitle")
# ... your app code ...
result_card("Transportation", 0.95)
```

---

## 📁 Assets

### **assets/logo.png**
VioletPro company logo used in the branded app

---

## ⚙️ Configuration

### **.streamlit/config.toml**
Streamlit theme configuration matching VioletPro branding:
- Primary color: Navy `#1a3460`
- Background: White `#ffffff`
- Secondary background: Soft gray `#f5f7fc`
- Text: Dark `#1b2236`
- Font: Sans serif

---

## 🚀 Quick Start

### Run the VioletPro branded app:
```bash
cd Smart-Expense-Classifier
streamlit run app/violetpro_app.py
```

### Run any other app:
```bash
streamlit run app/streamlit_app.py
streamlit run app/fintech_app.py
streamlit run app/demo_app.py
```

---

## 🔧 Customization

### To use custom styling in your own app:

1. Import the style module:
```python
from style import apply_theme, header, result_card
```

2. Apply theme and use components:
```python
apply_theme()
header("Your App Title", "Your subtitle")
```

3. Display results with styled card:
```python
category, confidence = predict(text)
result_card(category, confidence)
```

---

## 📝 Notes

- All apps use the same ML models from `../models/`
- Streamlit config is in `../.streamlit/config.toml`
- Logo and assets are in `assets/` folder
- Style module provides consistent VioletPro branding

---

**Recommended:** Use `violetpro_app.py` for professional demos and presentations.

---

**Last Updated:** November 2026  
**Status:** ✅ All apps ready to use
