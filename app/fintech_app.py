"""
Smart Expense Classifier - Professional FinTech Interface
Modern dark theme financial dashboard with testing capabilities
"""

import streamlit as st
import joblib
import numpy as np
import pandas as pd
import re
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import random

# Page configuration
st.set_page_config(
    page_title="Smart Expense Classifier",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Professional FinTech Dark Theme
st.markdown("""
<style>
    /* Import Inter font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main background */
    .main {
        background-color: #0B1120;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #263449;
    }
    
    [data-testid="stSidebar"] .css-1d391kg {
        padding-top: 2rem;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Text colors */
    .main, .main p, .main span, .main label {
        color: #F8FAFC !important;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #F8FAFC !important;
        font-weight: 600 !important;
    }
    
    /* Card styling */
    .card {
        background-color: #172235;
        border-radius: 14px;
        padding: 24px;
        border: 1px solid #263449;
        margin-bottom: 20px;
    }
    
    .card-title {
        color: #F8FAFC;
        font-size: 18px;
        font-weight: 600;
        margin-bottom: 8px;
    }
    
    .card-subtitle {
        color: #94A3B8;
        font-size: 14px;
        margin-bottom: 16px;
    }
    
    /* Logo section */
    .logo-section {
        padding: 20px;
        text-align: center;
        margin-bottom: 30px;
    }
    
    .app-title {
        color: #F8FAFC;
        font-size: 20px;
        font-weight: 700;
        margin: 10px 0 5px 0;
    }
    
    .app-subtitle {
        color: #94A3B8;
        font-size: 12px;
        margin: 0;
    }
    
    /* Sidebar sections */
    .sidebar-section {
        background-color: #172235;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 16px;
        border: 1px solid #263449;
    }
    
    .sidebar-section-title {
        color: #F8FAFC;
        font-size: 14px;
        font-weight: 600;
        margin-bottom: 12px;
    }
    
    .sidebar-info-item {
        color: #94A3B8;
        font-size: 13px;
        margin: 8px 0;
        line-height: 1.6;
    }
    
    .sidebar-info-label {
        color: #F8FAFC;
        font-weight: 500;
    }
    
    /* Category list */
    .category-item {
        color: #94A3B8;
        font-size: 13px;
        padding: 6px 0;
        border-bottom: 1px solid #263449;
    }
    
    .category-item:last-child {
        border-bottom: none;
    }
    
    .category-number {
        color: #3B82F6;
        font-weight: 600;
        margin-right: 8px;
    }
    
    /* Status badge */
    .status-badge {
        background-color: #10B981;
        color: #F8FAFC;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 500;
        display: inline-block;
    }
    
    /* Input styling */
    .stTextInput input, .stTextArea textarea {
        background-color: #1E293B !important;
        border: 1px solid #263449 !important;
        border-radius: 10px !important;
        color: #F8FAFC !important;
        padding: 12px 16px !important;
        font-size: 14px !important;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #3B82F6 !important;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2) !important;
    }
    
    /* Button styling for all buttons */
    .stButton button {
        background-color: #3B82F6 !important;
        color: #F8FAFC !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 16px 32px !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3) !important;
        letter-spacing: 0.3px !important;
        text-transform: none !important;
        min-height: 52px !important;
    }
    
    .stButton button:hover {
        background-color: #2563EB !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 20px rgba(59, 130, 246, 0.5) !important;
    }
    
    .stButton button:active {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3) !important;
    }
    
    /* Primary action button - Predict, Generate, Run Test */
    .stButton button[kind="primary"],
    div[data-testid="column"]:first-child .stButton button {
        background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%) !important;
        font-size: 17px !important;
        padding: 18px 36px !important;
        min-height: 56px !important;
    }
    
    /* Secondary/utility buttons */
    div[data-testid="column"]:nth-child(2) .stButton button,
    div[data-testid="column"]:last-child .stButton button {
        background-color: #1E293B !important;
        border: 2px solid #263449 !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2) !important;
        color: #94A3B8 !important;
    }
    
    div[data-testid="column"]:nth-child(2) .stButton button:hover,
    div[data-testid="column"]:last-child .stButton button:hover {
        background-color: #263449 !important;
        border-color: #3B82F6 !important;
        color: #F8FAFC !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.2) !important;
    }
    
    /* Download button styling */
    .stDownloadButton button {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%) !important;
        border: none !important;
    }
    
    .stDownloadButton button:hover {
        background: linear-gradient(135deg, #059669 0%, #047857 100%) !important;
        box-shadow: 0 8px 20px rgba(16, 185, 129, 0.4) !important;
    }
    
    /* Result card */
    .result-card {
        background: linear-gradient(135deg, #172235 0%, #1E293B 100%);
        border-radius: 14px;
        padding: 28px;
        border: 1px solid #263449;
        margin: 20px 0;
    }
    
    .result-category {
        color: #06B6D4;
        font-size: 28px;
        font-weight: 700;
        margin: 12px 0;
    }
    
    .result-confidence {
        color: #10B981;
        font-size: 24px;
        font-weight: 600;
    }
    
    .result-label {
        color: #94A3B8;
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 4px;
    }
    
    /* Progress bar */
    .custom-progress {
        background-color: #1E293B;
        border-radius: 8px;
        height: 8px;
        overflow: hidden;
        margin: 8px 0;
    }
    
    .custom-progress-fill {
        background: linear-gradient(90deg, #3B82F6, #06B6D4);
        height: 100%;
        transition: width 0.3s ease;
    }
    
    /* Empty state */
    .empty-state {
        text-align: center;
        padding: 60px 20px;
        color: #94A3B8;
    }
    
    .empty-state-icon {
        margin-bottom: 16px;
        opacity: 0.5;
    }
    
    .empty-state-icon svg {
        width: 48px;
        height: 48px;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #172235;
        border-radius: 10px;
        padding: 4px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 8px;
        color: #94A3B8;
        font-weight: 500;
        padding: 12px 24px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #3B82F6;
        color: #F8FAFC;
    }
    
    /* Add icons before tab text */
    .stTabs [data-baseweb="tab"]:nth-child(1)::before {
        content: "";
        margin-right: 8px;
        font-size: 16px;
    }
    
    .stTabs [data-baseweb="tab"]:nth-child(2)::before {
        content: "";
        margin-right: 8px;
        font-size: 16px;
    }
    
    .stTabs [data-baseweb="tab"]:nth-child(3)::before {
        content: "";
        margin-right: 8px;
        font-size: 16px;
    }
    
    /* Dataframe styling */
    .stDataFrame {
        background-color: #172235;
        border-radius: 10px;
    }
    
    /* Custom action buttons with icons */
    .action-buttons {
        display: flex;
        gap: 16px;
        margin: 24px 0;
    }
    
    .action-btn {
        flex: 1;
        background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
        color: #F8FAFC;
        border: none;
        border-radius: 10px;
        padding: 16px 24px;
        font-weight: 600;
        font-size: 15px;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
    }
    
    .action-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4);
    }
    
    .action-btn-secondary {
        background: #1E293B;
        border: 1.5px solid #263449;
        box-shadow: none;
    }
    
    .action-btn-secondary:hover {
        background-color: #263449;
        border-color: #3B82F6;
    }

</style>
""", unsafe_allow_html=True)

# Sample test data for each category
SAMPLE_DATA = {
    "Charity & Donations": [
        "Red Cross donation",
        "Church offering",
        "UNICEF monthly contribution",
        "Local mosque donation",
        "Charity fundraiser contribution"
    ],
    "Entertainment & Recreation": [
        "Cinema tickets for Avatar movie",
        "Spotify Premium subscription",
        "Netflix monthly payment",
        "PlayStation Store game purchase",
        "Concert tickets"
    ],
    "Financial Services": [
        "Bank account maintenance fee",
        "Credit card annual fee",
        "Investment platform commission",
        "Currency exchange fee",
        "ATM withdrawal charge"
    ],
    "Food & Dining": [
        "Starbucks morning coffee",
        "McDonald's lunch meal",
        "Pizza Hut delivery",
        "Grocery shopping at Carrefour",
        "Restaurant dinner"
    ],
    "Government & Legal": [
        "Passport renewal fee",
        "Traffic violation fine",
        "Legal consultation fee",
        "Government tax payment",
        "Property registration fee"
    ],
    "Healthcare & Medical": [
        "Doctor consultation",
        "Pharmacy prescription medicine",
        "Dental cleaning",
        "Health insurance premium",
        "Hospital emergency visit"
    ],
    "Income": [
        "Monthly salary payment",
        "Freelance project payment",
        "Investment dividend",
        "Rental income",
        "Bonus payment"
    ],
    "Shopping & Retail": [
        "Amazon electronics purchase",
        "Zara clothing shopping",
        "IKEA furniture",
        "Nike shoes",
        "Mobile phone purchase"
    ],
    "Transportation": [
        "Uber ride to airport",
        "Gas station fuel",
        "Car insurance payment",
        "Metro card refill",
        "Parking fee"
    ],
    "Utilities & Services": [
        "Electricity bill payment",
        "Internet service monthly fee",
        "Water bill",
        "Mobile phone bill",
        "Home maintenance service"
    ]
}

# Load model
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
        except:
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
    
    # Get all predictions sorted
    all_predictions = list(zip(model.classes_, probabilities))
    all_predictions.sort(key=lambda x: x[1], reverse=True)
    
    return {
        'category': prediction,
        'confidence': confidence,
        'all_predictions': all_predictions
    }

def generate_test_data(num_samples=10):
    """Generate random test transactions"""
    test_data = []
    categories = list(SAMPLE_DATA.keys())
    
    for _ in range(num_samples):
        category = random.choice(categories)
        transaction = random.choice(SAMPLE_DATA[category])
        test_data.append({
            'transaction': transaction,
            'expected_category': category
        })
    
    return pd.DataFrame(test_data)

# Sidebar
with st.sidebar:
    # Logo and title
    st.markdown("""
    <div class="logo-section">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M3 3v18h18" stroke="#3B82F6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M18 9l-5 5-4-4-6 6" stroke="#06B6D4" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <div class="app-title">Smart Expense Classifier</div>
        <div class="app-subtitle">AI-Powered Transaction Analysis</div>
    </div>
    """, unsafe_allow_html=True)
    
    # About section
    st.markdown("""
    <div class="sidebar-section">
        <div class="sidebar-section-title">About</div>
        <div class="sidebar-info-item">
            <span class="sidebar-info-label">Model:</span> Logistic Regression + TF-IDF
        </div>
        <div class="sidebar-info-item">
            <span class="sidebar-info-label">Accuracy:</span> 97.5%
        </div>
        <div class="sidebar-info-item" style="margin-top: 12px; line-height: 1.6;">
            Automatically classify financial transactions into categories using advanced machine learning.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Categories section
    st.markdown("""
    <div class="sidebar-section">
        <div class="sidebar-section-title">Supported Categories</div>
    """, unsafe_allow_html=True)
    
    categories = [
        "Charity & Donations",
        "Entertainment & Recreation",
        "Financial Services",
        "Food & Dining",
        "Government & Legal",
        "Healthcare & Medical",
        "Income",
        "Shopping & Retail",
        "Transportation",
        "Utilities & Services"
    ]
    
    for i, cat in enumerate(categories, 1):
        st.markdown(f"""
        <div class="category-item">
            <span class="category-number">{i:02d}</span>{cat}
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Main content
model = load_model()

if model is None:
    st.error("Model not found. Please ensure the model file exists in the models/ directory.")
    st.stop()

# Header
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("""
    <h1 style='margin-bottom: 8px;'>Smart Expense Classifier</h1>
    <p style='color: #94A3B8; font-size: 16px; margin-top: 0;'>
        AI-Powered Transaction Categorization & Testing
    </p>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='text-align: right; padding-top: 20px;'>
        <span class="status-badge">Model Ready</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Tabs for different features
tab1, tab2, tab3 = st.tabs(["Single Prediction", "Test Data Generator", "Batch Testing"])

# TAB 1: Single Prediction
with tab1:
    col_main, col_viz = st.columns([2, 1])
    
    with col_main:
        # Prediction card
        st.markdown("""
        <div class="card">
            <div class="card-title">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="display: inline-block; vertical-align: middle; margin-right: 8px;">
                    <circle cx="12" cy="12" r="10" stroke="#3B82F6" stroke-width="2" fill="none"/>
                    <path d="M12 6v6l4 2" stroke="#3B82F6" stroke-width="2" stroke-linecap="round"/>
                </svg>
                Transaction Classification
            </div>
            <div class="card-subtitle">
                Enter a transaction description to identify its most likely financial category
            </div>
        """, unsafe_allow_html=True)
        
        # Initialize input value
        if 'selected_example' not in st.session_state:
            st.session_state.selected_example = ""
        
        user_input = st.text_input(
            "Transaction Description",
            value=st.session_state.selected_example,
            placeholder="e.g., Starbucks coffee, Uber ride, Netflix subscription...",
            label_visibility="collapsed",
            key="transaction_input_tab1"
        )
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Action buttons with better spacing
        col_empty1, col_btn1, col_btn2, col_empty2 = st.columns([0.5, 2.5, 1.5, 0.5])
        
        with col_btn1:
            predict_clicked = st.button(
                "Predict Category",
                type="primary",
                use_container_width=True,
                key="predict_btn"
            )
        
        with col_btn2:
            if st.button(
                "Clear",
                use_container_width=True,
                key="clear_btn"
            ):
                st.session_state.selected_example = ""
                if 'last_result' in st.session_state:
                    del st.session_state['last_result']
                st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Handle prediction
        if predict_clicked and user_input and user_input.strip():
            with st.spinner("Analyzing transaction..."):
                result = predict_transaction(user_input, model)
                if result:
                    st.session_state['last_result'] = result
                    st.session_state['last_input'] = user_input
        
        # Display result
        if 'last_result' in st.session_state:
            result = st.session_state['last_result']
            user_input_stored = st.session_state.get('last_input', '')
            
            st.markdown("""
            <div class="result-card">
                <div class="result-label">Predicted Category</div>
                <div class="result-category">{}</div>
                
                <div class="result-label" style="margin-top: 20px;">Confidence Score</div>
                <div class="result-confidence">{}%</div>
                
                <div class="result-label" style="margin-top: 20px;">Original Transaction</div>
                <div style="color: #F8FAFC; font-size: 14px; margin-top: 4px;">{}</div>
            </div>
            """.format(
                result['category'],
                f"{result['confidence']*100:.1f}",
                user_input_stored
            ), unsafe_allow_html=True)
            
            # Top predictions
            st.markdown("""
            <div class="card">
                <div class="card-title">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="display: inline-block; vertical-align: middle; margin-right: 8px;">
                        <path d="M3 3v18h18" stroke="#06B6D4" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        <rect x="7" y="10" width="3" height="11" fill="#06B6D4"/>
                        <rect x="12" y="6" width="3" height="15" fill="#3B82F6"/>
                        <rect x="17" y="13" width="3" height="8" fill="#06B6D4"/>
                    </svg>
                    Top Predictions
                </div>
            """, unsafe_allow_html=True)
            
            for i, (cat, prob) in enumerate(result['all_predictions'][:3], 1):
                st.markdown(f"""
                <div style="margin: 16px 0;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                        <span style="color: #F8FAFC; font-size: 14px; font-weight: 500;">{i}. {cat}</span>
                        <span style="color: #06B6D4; font-size: 14px; font-weight: 600;">{prob*100:.1f}%</span>
                    </div>
                    <div class="custom-progress">
                        <div class="custom-progress-fill" style="width: {prob*100}%;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    with col_viz:
        # Visualization panel
        st.markdown("""
        <div class="card">
            <div class="card-title">Prediction Analytics</div>
        """, unsafe_allow_html=True)
        
        if 'last_result' in st.session_state:
            result = st.session_state['last_result']
            
            # Confidence gauge
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=result['confidence'] * 100,
                domain={'x': [0, 1], 'y': [0, 1]},
                number={'suffix': "%", 'font': {'size': 32, 'color': '#F8FAFC'}},
                gauge={
                    'axis': {'range': [None, 100], 'tickcolor': '#94A3B8'},
                    'bar': {'color': "#3B82F6"},
                    'bgcolor': "#1E293B",
                    'borderwidth': 0,
                    'steps': [
                        {'range': [0, 50], 'color': '#1E293B'},
                        {'range': [50, 75], 'color': '#263449'},
                        {'range': [75, 100], 'color': '#172235'}
                    ],
                    'threshold': {
                        'line': {'color': "#06B6D4", 'width': 4},
                        'thickness': 0.75,
                        'value': 95
                    }
                }
            ))
            
            fig_gauge.update_layout(
                paper_bgcolor='#172235',
                plot_bgcolor='#172235',
                font={'color': '#F8FAFC', 'family': 'Inter'},
                height=250,
                margin=dict(l=20, r=20, t=40, b=20)
            )
            
            st.plotly_chart(fig_gauge, use_container_width=True)
            
            # Category distribution
            st.markdown("""
            <div class="card-subtitle" style="margin-top: 24px;">
                Category Distribution
            </div>
            """, unsafe_allow_html=True)
            
            # Create bar chart
            top_5 = result['all_predictions'][:5]
            categories_list = [cat for cat, _ in top_5]
            probabilities_list = [prob * 100 for _, prob in top_5]
            
            fig_bar = go.Figure(data=[
                go.Bar(
                    x=probabilities_list,
                    y=categories_list,
                    orientation='h',
                    marker=dict(
                        color=probabilities_list,
                        colorscale=[[0, '#1E293B'], [0.5, '#3B82F6'], [1, '#06B6D4']],
                        line=dict(color='#263449', width=1)
                    ),
                    text=[f'{p:.1f}%' for p in probabilities_list],
                    textposition='outside',
                    textfont=dict(color='#94A3B8', size=11)
                )
            ])
            
            fig_bar.update_layout(
                paper_bgcolor='#172235',
                plot_bgcolor='#172235',
                font={'color': '#F8FAFC', 'family': 'Inter'},
                height=250,
                margin=dict(l=20, r=60, t=10, b=20),
                xaxis=dict(
                    showgrid=False,
                    showticklabels=False,
                    range=[0, 105]
                ),
                yaxis=dict(
                    showgrid=False,
                    tickfont=dict(size=11)
                ),
                showlegend=False
            )
            
            st.plotly_chart(fig_bar, use_container_width=True)
            
        else:
            st.markdown("""
            <div class="empty-state">
                <div class="empty-state-icon">
                    <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <rect x="3" y="3" width="18" height="18" rx="2" stroke="#94A3B8" stroke-width="2" fill="none"/>
                        <line x1="3" y1="9" x2="21" y2="9" stroke="#94A3B8" stroke-width="2"/>
                        <line x1="3" y1="15" x2="21" y2="15" stroke="#94A3B8" stroke-width="2"/>
                        <line x1="9" y1="9" x2="9" y2="21" stroke="#94A3B8" stroke-width="2"/>
                        <line x1="15" y1="9" x2="15" y2="21" stroke="#94A3B8" stroke-width="2"/>
                    </svg>
                </div>
                <div>Your prediction analytics will appear here</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

# TAB 2: Test Data Generator
with tab2:
    st.markdown("""
    <div class="card">
        <div class="card-title">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="display: inline-block; vertical-align: middle; margin-right: 8px;">
                <path d="M9 2v4m6-4v4M4 10h16M5 4h14a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2z" stroke="#06B6D4" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            Test Data Generator
        </div>
        <div class="card-subtitle">
            Generate random transaction samples for testing the classifier
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        num_samples = st.number_input(
            "Number of samples",
            min_value=5,
            max_value=100,
            value=10,
            step=5,
            key="num_samples_gen"
        )
        
        if st.button("Generate Test Data", type="primary", use_container_width=True):
            st.session_state['generated_data'] = generate_test_data(num_samples)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    if 'generated_data' in st.session_state:
        df = st.session_state['generated_data']
        
        st.markdown("""
        <div class="card">
            <div class="card-title">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="display: inline-block; vertical-align: middle; margin-right: 8px;">
                    <polyline points="22 12 18 12 15 21 9 3 6 12 2 12" stroke="#10B981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                Generated Test Transactions
            </div>
        """, unsafe_allow_html=True)
        
        st.dataframe(
            df,
            use_container_width=True,
            height=400
        )
        
        # Download button
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"test_transactions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Category distribution chart
        st.markdown("""
        <div class="card">
            <div class="card-title">Category Distribution</div>
        """, unsafe_allow_html=True)
        
        category_counts = df['expected_category'].value_counts()
        
        fig_dist = go.Figure(data=[
            go.Bar(
                x=category_counts.values,
                y=category_counts.index,
                orientation='h',
                marker=dict(
                    color='#3B82F6',
                    line=dict(color='#263449', width=1)
                )
            )
        ])
        
        fig_dist.update_layout(
            paper_bgcolor='#172235',
            plot_bgcolor='#172235',
            font={'color': '#F8FAFC', 'family': 'Inter'},
            height=400,
            margin=dict(l=20, r=20, t=20, b=20),
            xaxis=dict(
                showgrid=True,
                gridcolor='#263449',
                title="Count"
            ),
            yaxis=dict(
                showgrid=False,
                title=""
            )
        )
        
        st.plotly_chart(fig_dist, use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

# TAB 3: Batch Testing
with tab3:
    st.markdown("""
    <div class="card">
        <div class="card-title">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="display: inline-block; vertical-align: middle; margin-right: 8px;">
                <rect x="3" y="3" width="7" height="7" stroke="#3B82F6" stroke-width="2" fill="none" rx="1"/>
                <rect x="14" y="3" width="7" height="7" stroke="#3B82F6" stroke-width="2" fill="none" rx="1"/>
                <rect x="3" y="14" width="7" height="7" stroke="#3B82F6" stroke-width="2" fill="none" rx="1"/>
                <rect x="14" y="14" width="7" height="7" stroke="#3B82F6" stroke-width="2" fill="none" rx="1"/>
            </svg>
            Batch Testing
        </div>
        <div class="card-subtitle">
            Test the classifier with multiple transactions at once
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        batch_input = st.text_area(
            "Enter transactions (one per line)",
            height=200,
            placeholder="Starbucks coffee\nUber ride to airport\nNetflix subscription\n...",
            key="batch_input"
        )
    
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        if st.button("Run Batch Test", type="primary", use_container_width=True):
            if batch_input and batch_input.strip():
                transactions = [t.strip() for t in batch_input.split('\n') if t.strip()]
                
                results = []
                progress_bar = st.progress(0)
                
                for i, transaction in enumerate(transactions):
                    result = predict_transaction(transaction, model)
                    if result:
                        results.append({
                            'Transaction': transaction,
                            'Predicted Category': result['category'],
                            'Confidence': f"{result['confidence']*100:.1f}%"
                        })
                    progress_bar.progress((i + 1) / len(transactions))
                
                st.session_state['batch_results'] = pd.DataFrame(results)
        
        if st.button("Use Generated Data", use_container_width=True):
            if 'generated_data' in st.session_state:
                df = st.session_state['generated_data']
                transactions = df['transaction'].tolist()
                
                results = []
                progress_bar = st.progress(0)
                
                for i, transaction in enumerate(transactions):
                    result = predict_transaction(transaction, model)
                    if result:
                        expected = df.iloc[i]['expected_category']
                        predicted = result['category']
                        is_correct = expected == predicted
                        
                        results.append({
                            'Transaction': transaction,
                            'Expected': expected,
                            'Predicted': predicted,
                            'Confidence': f"{result['confidence']*100:.1f}%",
                            'Correct': '' if is_correct else ''
                        })
                    progress_bar.progress((i + 1) / len(transactions))
                
                st.session_state['batch_results'] = pd.DataFrame(results)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    if 'batch_results' in st.session_state:
        df_results = st.session_state['batch_results']
        
        st.markdown("""
        <div class="card">
            <div class="card-title">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="display: inline-block; vertical-align: middle; margin-right: 8px;">
                    <path d="M9 11l3 3L22 4" stroke="#10B981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11" stroke="#10B981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                Batch Test Results
            </div>
        """, unsafe_allow_html=True)
        
        # Show statistics if we have expected categories
        if 'Expected' in df_results.columns:
            total = len(df_results)
            correct = (df_results['Correct'] == '').sum()
            accuracy = (correct / total) * 100
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div style="text-align: center; padding: 20px;">
                    <div class="result-label">Total Tests</div>
                    <div style="color: #F8FAFC; font-size: 32px; font-weight: 700;">{total}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div style="text-align: center; padding: 20px;">
                    <div class="result-label">Correct</div>
                    <div style="color: #10B981; font-size: 32px; font-weight: 700;">{correct}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div style="text-align: center; padding: 20px;">
                    <div class="result-label">Accuracy</div>
                    <div style="color: #06B6D4; font-size: 32px; font-weight: 700;">{accuracy:.1f}%</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Show results table
        st.dataframe(
            df_results,
            use_container_width=True,
            height=400
        )
        
        # Download button
        csv = df_results.to_csv(index=False)
        st.download_button(
            label="Download Results",
            data=csv,
            file_name=f"batch_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
        
        st.markdown("</div>", unsafe_allow_html=True)

