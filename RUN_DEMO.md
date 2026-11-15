# Run the Streamlit Demo

## Quick Start (2 Steps)

### Step 1: Open Terminal
Open PowerShell or Command Prompt in the project folder:
```
cd "C:\Users\Cairo Lap\violetpro_Internship\Smart-Expense-Classifier"
```

### Step 2: Run Streamlit
```bash
streamlit run app/demo_app.py
```

The app will automatically open in your browser at `http://localhost:8501`

---

## What the Demo Does

### Features:
1. **Single Transaction Prediction**
   - Enter any transaction description
   - Get instant category prediction
   - See confidence score

2. **Visual Dashboard**
   - Confidence gauge
   - Top 3 predictions
   - Probability chart for all categories

3. **Quick Examples**
   - Pre-filled example buttons
   - Test with one click

4. **Batch Prediction**
   - Upload CSV file
   - Predict multiple transactions at once
   - Download results

---

## How to Use

### Test Single Transactions

1. Type a transaction in the input box:
   - "Starbucks coffee"
   - "Uber ride to airport"
   - "Netflix subscription"
   - "Doctor appointment"
   - "Electric bill payment"

2. Click "Predict Category"

3. See the result:
   - Predicted category
   - Confidence percentage
   - Top 3 alternatives
   - Visual charts

### Test Batch Upload

1. Create a CSV file with this format:
```csv
transaction_description
Starbucks coffee
Uber ride
Amazon purchase
Netflix subscription
Doctor visit
```

2. Click "Browse files" in the Batch Prediction section

3. Upload your CSV

4. Click "Predict All"

5. Download the results with predictions

---

## Expected Results

| Transaction | Category | Confidence |
|-------------|----------|------------|
| Starbucks coffee | Food & Dining | 99% |
| Uber ride | Transportation | 99% |
| Netflix | Entertainment & Recreation | 99% |
| Doctor visit | Healthcare & Medical | 85%+ |
| Electric bill | Utilities & Services | 92% |

---

## Troubleshooting

### App doesn't start
```bash
# Make sure streamlit is installed
python -m pip install streamlit

# Try running with python -m
python -m streamlit run app/demo_app.py
```

### Model not found error
```bash
# Check if model exists
dir models\final_expense_classifier.joblib

# If not, retrain the model
python src/train_complete_pipeline.py
```

### Browser doesn't open
Manually open: `http://localhost:8501`

### Port already in use
```bash
# Use a different port
streamlit run app/demo_app.py --server.port 8502
```

---

## Demo Screenshots (What to Expect)

### Main Interface:
- Clean, modern UI
- Input box at the top
- Quick example buttons
- Prediction results box
- Sidebar with categories

### After Prediction:
- Large result display
- Confidence gauge (0-100%)
- Top 3 predictions with bars
- Full category probability chart

### Batch Prediction:
- File upload area
- Preview of uploaded data
- Predict button
- Results table
- Download button

---

## Testing Checklist

- [ ] App starts without errors
- [ ] Can enter text and get prediction
- [ ] Quick example buttons work
- [ ] Confidence scores show correctly
- [ ] Top 3 predictions display
- [ ] Charts render properly
- [ ] Batch upload accepts CSV
- [ ] Batch predictions work
- [ ] Can download results
- [ ] No crashes or errors

---

## Next Steps

After testing the demo:

1. **Take Screenshots**
   - Main interface
   - Prediction results
   - Charts and visualizations
   - Batch prediction results

2. **Record Demo Video** (Optional)
   - Screen record while using app
   - Show different predictions
   - Explain the features
   - 2-3 minutes max

3. **Prepare Presentation**
   - Use screenshots in slides
   - Show live demo
   - Explain accuracy metrics

---

## Demo Tips

### For Presentation:
- Start with simple examples (Starbucks, Uber)
- Show high confidence predictions first
- Demonstrate the visual charts
- Show batch prediction feature
- Mention 97.5% accuracy

### Common Questions:
- **Q**: How does it work?
  - **A**: TF-IDF converts text to numbers, Logistic Regression classifies

- **Q**: How accurate is it?
  - **A**: 97.5% accuracy on 100K+ transactions

- **Q**: Can it handle Arabic?
  - **A**: Yes, we have a separate Arabic model trained on 10K Egyptian transactions

- **Q**: What if it's wrong?
  - **A**: Show the top 3 predictions - often the correct one is in top 3

---

## Performance Notes

- **Fast**: Predictions in <1 second
- **Accurate**: 97.5% correct
- **Scalable**: Can handle thousands of transactions
- **User-friendly**: Simple interface, no technical knowledge needed

---

**Ready to demo!** 

Just run: `streamlit run app/demo_app.py`
