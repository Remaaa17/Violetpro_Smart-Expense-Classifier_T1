"""VioletPro look & feel for the Streamlit demo.
Usage in app.py:
    import streamlit as st
    from style import apply_theme, header
    st.set_page_config(page_title="Smart Expense Classifier", page_icon="💳", layout="centered")
    apply_theme()
    header("Smart Expense Classifier", "Type a transaction description and get its category")
"""
import base64
from pathlib import Path
import streamlit as st

NAVY, NAVY_DARK, NAVY_MID = "#1a3460", "#0f2142", "#2c4d8a"
YELLOW, YELLOW_SOFT = "#fae162", "#e8b923"
BG_SOFT, LINE = "#f5f7fc", "#dbe2f0"

_LOGO = Path(__file__).parent / "assets" / "logo.png"

CSS = f"""
<style>
  .block-container {{padding-top: 1.5rem; max-width: 760px;}}
  h1, h2, h3 {{color: {NAVY};}}
  .vp-hero {{background: linear-gradient(135deg, {NAVY_DARK}, {NAVY} 70%, {NAVY_MID});
    color: #fff; border-radius: 14px; padding: 22px 26px; margin-bottom: 22px;}}
  .vp-hero img {{height: 64px; background: #fff; border-radius: 10px; padding: 6px 10px; margin-bottom: 14px;}}
  .vp-hero h1 {{color: #fff; margin: 0; font-size: 1.9rem;}}
  .vp-hero p {{margin: 4px 0 0; opacity: .85;}}
  .vp-tag {{display: inline-block; background: {YELLOW}; color: {NAVY_DARK}; font-weight: 700;
    font-size: 11px; letter-spacing: 1.5px; text-transform: uppercase; padding: 3px 10px;
    border-radius: 99px; margin-bottom: 8px;}}
  .vp-result {{background: {BG_SOFT}; border: 1px solid {LINE}; border-top: 4px solid {YELLOW_SOFT};
    border-radius: 10px; padding: 14px 18px; margin-top: 14px;}}
  .vp-result b {{font-size: 1.6rem; color: {NAVY};}}
  .vp-result span {{color: #5f6b85;}}
  .stButton > button {{background: {NAVY}; color: #fff; border: 0; border-radius: 8px; font-weight: 600;}}
  .stButton > button:hover {{background: {NAVY_MID}; color: {YELLOW};}}
  .stTextInput input, .stTextArea textarea {{border: 1px solid {LINE}; border-radius: 8px;}}
  .stProgress > div > div > div > div {{background-color: {YELLOW_SOFT};}}
  footer {{visibility: hidden;}}
</style>
"""

def apply_theme():
    st.markdown(CSS, unsafe_allow_html=True)

def header(title, subtitle=""):
    logo = ""
    if _LOGO.exists():
        b64 = base64.b64encode(_LOGO.read_bytes()).decode()
        logo = f'<img src="data:image/png;base64,{b64}" alt="VioletPro">'
    st.markdown(
        f'<div class="vp-hero">{logo}<br><span class="vp-tag">AI &amp; ML</span>'
        f'<h1>{title}</h1><p>{subtitle}</p></div>', unsafe_allow_html=True)

def result_card(category, confidence):
    st.markdown(
        f'<div class="vp-result"><span>Predicted category</span><br><b>{category}</b>'
        f'<br><span>Confidence: {confidence:.1%}</span></div>', unsafe_allow_html=True)
    st.progress(float(confidence))
