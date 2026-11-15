"""
Setup script for Smart Expense Classifier environment
Installs all dependencies and downloads required NLTK data
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"\n{'='*70}")
    print(f"🔧 {description}")
    print(f"{'='*70}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)
        print(f"✅ {description} - Complete!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        print(f"Output: {e.stdout}")
        print(f"Error: {e.stderr}")
        return False

def download_nltk_data():
    """Download required NLTK data"""
    print(f"\n{'='*70}")
    print("📚 Downloading NLTK data")
    print(f"{'='*70}")
    
    try:
        import nltk
        
        # Download stopwords
        print("Downloading stopwords...")
        nltk.download('stopwords', quiet=True)
        
        # Download punkt (for tokenization)
        print("Downloading punkt...")
        nltk.download('punkt', quiet=True)
        
        # Download wordnet (for lemmatization)
        print("Downloading wordnet...")
        nltk.download('wordnet', quiet=True)
        
        print("✅ NLTK data download complete!")
        return True
    except Exception as e:
        print(f"❌ Error downloading NLTK data: {e}")
        return False

def verify_installation():
    """Verify all packages are installed correctly"""
    print(f"\n{'='*70}")
    print("🔍 Verifying Installation")
    print(f"{'='*70}")
    
    required_packages = [
        'pandas',
        'numpy',
        'matplotlib',
        'seaborn',
        'sklearn',
        'joblib',
        'nltk',
        'streamlit',
        'plotly',
        'jupyter'
    ]
    
    all_good = True
    
    for package in required_packages:
        try:
            if package == 'sklearn':
                __import__('sklearn')
            else:
                __import__(package)
            print(f"✅ {package:20s} - OK")
        except ImportError:
            print(f"❌ {package:20s} - NOT FOUND")
            all_good = False
    
    return all_good

def main():
    """Main setup execution"""
    print("\n" + "="*70)
    print("🚀 SMART EXPENSE CLASSIFIER - ENVIRONMENT SETUP")
    print("="*70)
    
    # Check Python version
    python_version = sys.version_info
    print(f"\n✅ Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print("⚠️  Warning: Python 3.8+ is recommended")
    
    # Install pip packages
    success = run_command(
        f"{sys.executable} -m pip install -r requirements.txt",
        "Installing Python packages from requirements.txt"
    )
    
    if not success:
        print("\n❌ Package installation failed!")
        return False
    
    # Download NLTK data
    download_nltk_data()
    
    # Verify installation
    if verify_installation():
        print("\n" + "="*70)
        print("✅ ENVIRONMENT SETUP COMPLETE!")
        print("="*70)
        print("\n📋 Next Steps:")
        print("  1. Run the ML pipeline:")
        print("     python src/train_complete_pipeline.py")
        print("\n  2. Or open Jupyter notebook:")
        print("     jupyter notebook notebooks/01_Complete_ML_Pipeline.ipynb")
        print("\n  3. Run Streamlit demo (after training model):")
        print("     streamlit run app/streamlit_app.py")
        print("\n" + "="*70)
        return True
    else:
        print("\n⚠️  Some packages may not be installed correctly")
        print("Try running: pip install -r requirements.txt")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
