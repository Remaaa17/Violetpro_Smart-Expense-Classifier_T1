"""
Smart Expense Classifier - Streamlit Demo App
Interactive web application for transaction category prediction
"""

import streamlit as st
import joblib
import numpy as np
import re
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import json
import os

# Page config
st.set_page_config(
    page_title="Smart Expense Classifier",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .prediction-box {
        background-color: #f0f8ff;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 1rem 0;
    }
    .metric-card {
        background-color: #fff;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_model():
    """Load the trained model"""
    model_path = '../models/final_expense_classifier.joblib'
    if not os.path.exists(model_path):
        model_path = 'models/final_expense_classifier.joblib'
    return joblib.load(model_path)


@st.cache_resource
def load_metadata():
    """Load model metadata"""
    metadata_path = '../models/model_metadata.json'
    if not os.path.exists(metadata_path):
        metadata_path = 'models/model_metadata.json'
    with open(metadata_path, 'r') as f:
        return json.load(f)


def preprocess_text(text):
    """Preprocess transaction description"""
    text = str(text).lower()
    text = re.sub(r'[^a-z\s]', ' ', text)
    text = ' '.join(text.split())
    return text


def predict(text, model):
    """Predict category and confidence"""
    processed = preprocess_text(text)
    
    if not processed.strip():
        return None
    
    prediction = model.predict([processed])[0]
    probabilities = model.predict_proba([processed])[0]
    confidence = max(probabilities)
    
    # Get all predictions with probabilities
    all_predictions = [(model.classes_[i], float(probabilities[i])) 
                      for i in range(len(model.classes_))]
    all_predictions = sorted(all_predictions, key=lambda x: x[1], reverse=True)
    
    return {
        'category': prediction,
        'confidence': float(confidence),
        'all_predictions': all_predictions
    }


def create_confidence_chart(all_predictions):
    """Create interactive bar chart for all predictions"""
    df_pred = pd.DataFrame(all_predictions, columns=['Category', 'Probability'])
    df_pred['Probability'] = df_pred['Probability'] * 100  # Convert to percentage
    
    fig = px.bar(
        df_pred,
        x='Probability',
        y='Category',
        orientation='h',
        title='Category Probabilities',
        labels={'Probability': 'Probability (%)', 'Category': ''},
        color='Probability',
        color_continuous_scale='Blues',
        text='Probability'
    )
    
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig.update_layout(
        showlegend=False,
        height=500,
        xaxis_range=[0, 100]
    )
    
    return fig


def create_top3_gauge(confidence):
    """Create gauge chart for confidence"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=confidence * 100,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Confidence", 'font': {'size': 24}},
        number={'suffix': "%"},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 50], 'color': '#ffcccc'},
                {'range': [50, 75], 'color': '#ffffcc'},
                {'range': [75, 100], 'color': '#ccffcc'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
    return fig


def main():
    """Main application"""
    
    # Header
    st.markdown('<div class="main-header">💰 Smart Expense Classifier</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">AI-Powered Transaction Categorization</div>', unsafe_allow_html=True)
    
    # Load model
    try:
        model = load_model()
        metadata = load_metadata()
    except Exception as e:
        st.error(f"Error loading model: {e}")
        st.stop()
    
    # Sidebar - Model Info
    with st.sidebar:
        st.header("📊 Model Information")
        st.info(f"**Model:** {metadata['model_name']}")
        st.info(f"**Test Accuracy:** {metadata['test_metrics']['accuracy']:.2%}")
        st.info(f"**F1-Score:** {metadata['test_metrics']['f1_score']:.2%}")
        
        st.header("📋 Categories")
        for i, cat in enumerate(metadata['categories'], 1):
            st.write(f"{i}. {cat}")
        
        st.header("💡 Tips")
        st.markdown("""
        - Enter a clear transaction description
        - Include merchant name if available
        - Use common keywords (e.g., 'coffee', 'uber', 'rent')
        - Try both short and detailed descriptions
        """)
        
        st.header("📌 Example Transactions")
        examples = {
            "Starbucks Coffee": "Food & Dining",
            "Uber ride to airport": "Transportation",
            "Amazon electronics": "Shopping & Retail",
            "Doctor appointment": "Healthcare & Medical",
            "Electric bill payment": "Utilities & Services",
            "Monthly salary": "Income",
            "Bank fees": "Financial Services",
            "Netflix subscription": "Entertainment & Recreation",
            "Donation to charity": "Charity & Donations",
            "Tax payment": "Government & Legal"
        }
        
        for desc, cat in examples.items():
            st.caption(f"_{desc}_ → {cat}")
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("🔮 Make a Prediction")
        
        # Input methods
        tab1, tab2 = st.tabs(["✍️ Single Prediction", "📄 Batch Prediction"])
        
        with tab1:
            # Text input
            user_input = st.text_input(
                "Enter transaction description:",
                placeholder="e.g., Starbucks coffee, Uber ride, Netflix subscription...",
                help="Type any transaction description to get category prediction"
            )
            
            # Quick examples
            st.write("**Quick Examples:**")
            example_cols = st.columns(5)
            quick_examples = [
                "Starbucks",
                "Uber",
                "Amazon",
                "Doctor",
                "Netflix"
            ]
            
            for i, example in enumerate(quick_examples):
                if example_cols[i].button(example, use_container_width=True):
                    user_input = example
                    st.rerun()
            
            # Predict button
            if st.button("🚀 Predict Category", type="primary", use_container_width=True):
                if user_input and user_input.strip():
                    with st.spinner("Analyzing transaction..."):
                        result = predict(user_input, model)
                        
                        if result:
                            # Display result
                            st.markdown('<div class="prediction-box">', unsafe_allow_html=True)
                            st.markdown(f"### Predicted Category: **{result['category']}**")
                            st.markdown(f"### Confidence: **{result['confidence']:.2%}**")
                            st.markdown('</div>', unsafe_allow_html=True)
                            
                            # Store in session state for visualization
                            st.session_state['last_prediction'] = result
                        else:
                            st.warning("Please enter a valid transaction description")
                else:
                    st.warning("Please enter a transaction description")
        
        with tab2:
            st.info("Upload a CSV file with a 'transaction_description' column")
            uploaded_file = st.file_uploader("Choose CSV file", type=['csv'])
            
            if uploaded_file:
                df = pd.read_csv(uploaded_file)
                
                if 'transaction_description' in df.columns:
                    st.write(f"**Loaded {len(df)} transactions**")
                    
                    if st.button("Predict All", type="primary"):
                        with st.spinner("Processing batch..."):
                            predictions = []
                            confidences = []
                            
                            for desc in df['transaction_description']:
                                result = predict(str(desc), model)
                                if result:
                                    predictions.append(result['category'])
                                    confidences.append(result['confidence'])
                                else:
                                    predictions.append("Unknown")
                                    confidences.append(0.0)
                            
                            df['predicted_category'] = predictions
                            df['confidence'] = confidences
                            
                            st.success("✅ Batch prediction complete!")
                            st.dataframe(df, use_container_width=True)
                            
                            # Download results
                            csv = df.to_csv(index=False).encode('utf-8')
                            st.download_button(
                                label="📥 Download Results",
                                data=csv,
                                file_name="predictions.csv",
                                mime="text/csv"
                            )
                else:
                    st.error("CSV must contain 'transaction_description' column")
    
    with col2:
        st.header("📈 Visualization")
        
        # Show visualization if prediction exists
        if 'last_prediction' in st.session_state:
            result = st.session_state['last_prediction']
            
            # Confidence gauge
            st.subheader("Confidence Score")
            fig_gauge = create_top3_gauge(result['confidence'])
            st.plotly_chart(fig_gauge, use_container_width=True)
            
            # Top 3 predictions
            st.subheader("Top 3 Predictions")
            top_3 = result['all_predictions'][:3]
            for i, (cat, prob) in enumerate(top_3, 1):
                col_a, col_b = st.columns([3, 1])
                with col_a:
                    st.write(f"**{i}. {cat}**")
                with col_b:
                    st.write(f"{prob:.1%}")
                st.progress(prob)
        else:
            st.info("👆 Make a prediction to see visualization")
    
    # Full probability chart (below main content)
    if 'last_prediction' in st.session_state:
        st.header("📊 All Category Probabilities")
        result = st.session_state['last_prediction']
        fig_bar = create_confidence_chart(result['all_predictions'])
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>Smart Expense Classifier | Built with Streamlit & scikit-learn | VioletPro Internship 2026</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
