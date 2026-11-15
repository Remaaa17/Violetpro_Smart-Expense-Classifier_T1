@echo off
echo ========================================
echo Smart Expense Classifier - Demo Launch
echo ========================================
echo.
echo Starting Streamlit app...
echo.
echo The app will open in your browser at:
echo http://localhost:8501
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

python -m streamlit run app/demo_app.py

pause
