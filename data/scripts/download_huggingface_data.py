"""
Download Real HuggingFace Transaction Dataset
Dataset: mitulshah/transaction-categorization
"""

from datasets import load_dataset
import pandas as pd
import os

print("="*70)
print("DOWNLOADING REAL HUGGINGFACE TRANSACTION DATASET")
print("="*70)
print("Dataset: mitulshah/transaction-categorization")
print()

# Create data directory
os.makedirs('data/raw', exist_ok=True)

try:
    # Load dataset from HuggingFace
    print("[INFO] Loading dataset from HuggingFace...")
    dataset = load_dataset("mitulshah/transaction-categorization")
    
    print(f"[SUCCESS] Dataset loaded successfully!")
    print(f"[INFO] Available splits: {list(dataset.keys())}")
    
    # Convert to pandas DataFrame
    if 'train' in dataset:
        df = dataset['train'].to_pandas()
        print(f"\n[INFO] Dataset shape: {df.shape}")
        print(f"[INFO] Columns: {list(df.columns)}")
        
        # Save full dataset
        full_path = 'data/raw/huggingface_full_dataset.csv'
        df.to_csv(full_path, index=False, encoding='utf-8')
        print(f"\n[SUCCESS] Full dataset saved: {full_path}")
        print(f"   Total records: {len(df):,}")
        
        # Save sample (10k records)
        sample_df = df.sample(n=min(10000, len(df)), random_state=42)
        sample_path = 'data/raw/huggingface_sample_10k.csv'
        sample_df.to_csv(sample_path, index=False, encoding='utf-8')
        print(f"[SUCCESS] Sample dataset saved: {sample_path}")
        print(f"   Sample records: {len(sample_df):,}")
        
        # Show info
        print(f"\n[INFO] Dataset Info:")
        print(df.info())
        
        print(f"\n[INFO] First 5 records:")
        print(df.head())
        
        # Category distribution if available
        if 'category' in df.columns:
            print(f"\n[INFO] Category Distribution:")
            print(df['category'].value_counts())
        elif 'label' in df.columns:
            print(f"\n[INFO] Label Distribution:")
            print(df['label'].value_counts())
        
    else:
        print("[WARNING] 'train' split not found. Available splits:", list(dataset.keys()))
        # Try to use first available split
        first_split = list(dataset.keys())[0]
        print(f"Using '{first_split}' split instead...")
        df = dataset[first_split].to_pandas()
        df.to_csv('data/raw/huggingface_full_dataset.csv', index=False, encoding='utf-8')
        print(f"[SUCCESS] Saved {len(df):,} records")
    
    print("\n" + "="*70)
    print("[SUCCESS] DOWNLOAD COMPLETE!")
    print("="*70)
    
except Exception as e:
    print(f"\n[ERROR] {e}")
    print("\nTrying alternative download method...")
    
    # Alternative: try different dataset name or structure
    try:
        print("Attempting to load with different configuration...")
        dataset = load_dataset("mitulshah/transaction-categorization", split='train')
        df = pd.DataFrame(dataset)
        df.to_csv('data/raw/huggingface_full_dataset.csv', index=False, encoding='utf-8')
        print(f"[SUCCESS] Saved {len(df):,} records")
    except Exception as e2:
        print(f"[ERROR] Alternative method also failed: {e2}")
        print("\nPlease check:")
        print("1. Dataset name: mitulshah/transaction-categorization")
        print("2. Internet connection")
        print("3. HuggingFace access permissions")
