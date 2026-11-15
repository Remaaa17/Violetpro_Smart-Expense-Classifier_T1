"""
Smart Expense Classifier - Streamlit Demo
Simple and working demo application
"""

import streamlit as st
import joblib
import numpy as np
import pandas as pd
import re
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Smart Expense Classifier",
    page_icon="💳",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .big-font {
        font-size: 24px !important;
        font-weight: bold;
    }
    .result-box {
        padding: 20px;
        border-radius: 10px;
        background-color: #f0f8ff;
        border-left: 5px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    """Load the trained model"""
    try:
        model = joblib.load('models/final_expense_classifier.joblib')
        return model
    except:
        try:
            model = joblib.load('../models/final_expense_classifier.joblib')
            return model
        except Exception as e:
            st.error(f"Error loading model: {e}")
            return None

def preprocess_text(text):
    """Preprocess transaction description"""
    text = str(text).lower()
    text = re.sub(r'[^a-z\s]', ' ', text)
    text = ' '.join(text.split())
    return text

def predict_transaction(text, model):
    """Predict category for a transaction"""
    if not text or not text.strip():
        return None
    
    processed = preprocess_text(text)
    prediction = model.predict([processed])[0]
    probabilities = model.predict_proba([processed])[0]
    confidence = max(probabilities)
    
    # Get top 3 predictions
    top_3_idx = np.argsort(probabilities)[-3:][::-1]
    top_3 = [(model.classes_[i], probabilities[i]) for i in top_3_idx]
    
    return {
        'category': prediction,
        'confidence': confidence,
        'probabilities': dict(zip(model.classes_, probabilities)),
        'top_3': top_3
    }

def main():
    # Header
    st.title("💳 Smart Expense Classifier")
    st.markdown("### AI-Powered Transaction Categorization")
    st.markdown("---")
    
    # Load model
    model = load_model()
    
    if model is None:
        st.error("Failed to load model. Please check if the model file exists.")
        return
    
    # Sidebar
    with st.sidebar:
        st.header("About")
        st.info("""
        This app uses Machine Learning to automatically categorize financial transactions.
        
        **Accuracy**: 97.5%
        
        **Model**: Logistic Regression + TF-IDF
        """)
        
        st.header("Categories")
        for i, cat in enumerate(model.classes_, 1):
            st.write(f"{i}. {cat}")
        
        st.header("Example Transactions")
        st.code("""
Starbucks coffee
Uber ride to airport
Amazon purchase
Netflix subscription
Doctor visit
Electric bill payment
Monthly salary
Charity donation
Tax payment
        """)
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("🔮 Make a Prediction")
        
        # Input
        user_input = st.text_input(
            "Enter transaction description:",
            placeholder="e.g., Starbucks coffee, Uber ride, Netflix...",
            help="Type any transaction description"
        )
        
        # Quick examples
        st.write("**Quick Examples:**")
        example_col1, example_col2, example_col3, example_col4 = st.columns(4)
        
        examples = {
            "Starbucks": "Starbucks coffee",
            "Uber": "Uber ride",
            "Amazon": "Amazon purchase",
            "Netflix": "Netflix subscription"
        }
        
        for i, (btn_text, example_text) in enumerate(examples.items()):
            col = [example_col1, example_col2, example_col3, example_col4][i]
            if col.button(btn_text, use_container_width=True):
                user_input = example_text
                st.rerun()
        
        # Predict button
        if st.button("🚀 Predict Category", type="primary", use_container_width=True):
            if user_input and user_input.strip():
                with st.spinner("Analyzing transaction..."):
                    result = predict_transaction(user_input, model)
                    
                    if result:
                        # Store result in session state
                        st.session_state['last_result'] = result
                        st.session_state['last_input'] = user_input
                    else:
                        st.warning("Please enter a valid transaction description")
            else:
                st.warning("Please enter a transaction description")
        
        # Show result if available
        if 'last_result' in st.session_state:
            result = st.session_state['last_result']
            user_input = st.session_state['last_input']
            
            st.markdown("---")
            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            st.markdown(f"**Input:** {user_input}")
            st.markdown(f'<p class="big-font">Category: {result["category"]}</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="big-font">Confidence: {result["confidence"]:.1%}</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Top 3 predictions
            st.subheader("Top 3 Predictions")
            for i, (cat, prob) in enumerate(result['top_3'], 1):
                col_a, col_b = st.columns([3, 1])
                with col_a:
                    st.write(f"**{i}. {cat}**")
                with col_b:
                    st.write(f"{prob:.1%}")
                st.progress(float(prob))
    
    with col2:
        st.header("📊 Visualization")
        
        if 'last_result' in st.session_state:
            result = st.session_state['last_result']
            
            # Confidence gauge
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=result['confidence'] * 100,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Confidence"},
                number={'suffix': "%"},
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 50], 'color': "lightgray"},
                        {'range': [50, 75], 'color': "gray"},
                        {'range': [75, 100], 'color': "lightgreen"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))
            fig_gauge.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
            st.plotly_chart(fig_gauge, use_container_width=True)
            
            # Category probabilities
            st.subheader("All Categories")
            prob_df = pd.DataFrame({
                'Category': list(result['probabilities'].keys()),
                'Probability': [v * 100 for v in result['probabilities'].values()]
            }).sort_values('Probability', ascending=False)
            
            fig_bar = px.bar(
                prob_df,
                x='Probability',
                y='Category',
                orientation='h',
                color='Probability',
                color_continuous_scale='Blues'
            )
            fig_bar.update_layout(
                showlegend=False,
                height=400,
                xaxis_title="Probability (%)",
                yaxis_title=""
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("Make a prediction to see visualizations")
    
    # Batch prediction
    st.markdown("---")
    st.header("📄 Batch Prediction")
    
    uploaded_file = st.file_uploader(
        "Upload a CSV file with 'transaction_description' column",
        type=['csv'],
        help="CSV file must contain a column named 'transaction_description'"
    )
    
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            
            if 'transaction_description' in df.columns:
                st.write(f"**Loaded {len(df)} transactions**")
                st.dataframe(df.head(), use_container_width=True)
                
                if st.button("Predict All", type="primary"):
                    with st.spinner("Processing batch..."):
                        predictions = []
                        confidences = []
                        
                        for desc in df['transaction_description']:
                            result = predict_transaction(str(desc), model)
                            if result:
                                predictions.append(result['category'])
                                confidences.append(result['confidence'])
                            else:
                                predictions.append("Unknown")
                                confidences.append(0.0)
                        
                        df['predicted_category'] = predictions
                        df['confidence'] = [f"{c:.1%}" for c in confidences]
                        
                        st.success("Batch prediction complete!")
                        st.dataframe(df, use_container_width=True)
                        
                        # Download results
                        csv = df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="Download Results",
                            data=csv,
                            file_name="predictions.csv",
                            mime="text/csv"
                        )
            else:
                st.error("CSV must contain 'transaction_description' column")
        except Exception as e:
            st.error(f"Error processing file: {e}")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>Smart Expense Classifier | VioletPro Internship 2026 | Accuracy: 97.5%</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
