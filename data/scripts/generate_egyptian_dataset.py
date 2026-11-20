"""
Egyptian Arabic Financial Transaction Dataset Generator
Senior Data Scientist | NLP Engineer | Synthetic Data Specialist

Generates realistic synthetic Egyptian financial transactions with:
- Modern Standard Arabic (MSA)
- Egyptian Colloquial Arabic
- Arabic-English mixed language
- Arabizi (Franco-Arabic)
- Realistic imperfections and noise
- Ambiguous cases
- Label noise experiments

Based on: https://huggingface.co/datasets/mitulshah/transaction-categorization
"""

import pandas as pd
import numpy as np
import random
import os
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# Set random seeds for reproducibility
RANDOM_SEED = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

# Fixed values
COUNTRY = "Egypt"
CURRENCY = "EGP"

# Categories (keep in English)
CATEGORIES = [
    "Food & Dining",
    "Transportation",
    "Shopping & Retail",
    "Entertainment & Recreation",
    "Healthcare & Medical",
    "Utilities & Services",
    "Financial Services",
    "Income",
    "Government & Legal",
    "Charity & Donations"
]


class EgyptianTransactionGenerator:
    """
    Generates realistic Egyptian Arabic financial transactions
    """
    
    def __init__(self, seed=42):
        self.seed = seed
        random.seed(seed)
        np.random.seed(seed)
        
        # Category templates with multiple language styles
        self.category_templates = self._build_templates()
        
        # Quality distribution profiles
        self.quality_profiles = {
            'clean': 0.55,
            'spelling_errors': 0.15,
            'mixed_language': 0.15,
            'ambiguous': 0.10,
            'incomplete': 0.05
        }
        
        # Language distribution
        self.language_styles = {
            'msa': 0.25,           # Modern Standard Arabic
            'egyptian': 0.30,       # Egyptian Colloquial
            'mixed': 0.20,          # Arabic-English mixed
            'arabizi': 0.15,        # Franco-Arabic
            'english': 0.10         # Pure English
        }
    
    def _build_templates(self):
        """Build category-specific transaction templates"""
        
        templates = {
            "Food & Dining": {
                'msa': [
                    "شراء مستلزمات غذائية من {merchant}",
                    "دفع فاتورة المطعم {merchant}",
                    "شراء وجبة من {merchant}",
                    "طلب توصيل طعام من {merchant}",
                    "دفع ثمن القهوة في {merchant}",
                    "شراء من السوبرماركت {merchant}",
                    "وجبة عشاء في {merchant}",
                    "شراء خبز من {merchant}"
                ],
                'egyptian': [
                    "اشتريت أكل من {merchant}",
                    "دفعت فلوس المطعم {merchant}",
                    "طلبت دليفري من {merchant}",
                    "اشتريت حاجات من {merchant}",
                    "قهوة من {merchant}",
                    "شراء من سوبرماركت {merchant}",
                    "عشا في {merchant}",
                    "اشتريت خبز من {merchant}"
                ],
                'mixed': [
                    "دفع {merchant} restaurant bill",
                    "شراء food من {merchant}",
                    "طلب delivery من {merchant}",
                    "{merchant} groceries",
                    "دفع coffee في {merchant}",
                    "شراء من {merchant} supermarket"
                ],
                'arabizi': [
                    "eshtarayt akl mn {merchant}",
                    "dafa3t flos el mat3am {merchant}",
                    "talbt delivery mn {merchant}",
                    "{merchant} food order",
                    "shera mn {merchant}"
                ],
                'english': [
                    "{merchant} restaurant payment",
                    "Food delivery from {merchant}",
                    "{merchant} groceries",
                    "Coffee at {merchant}",
                    "Dinner at {merchant}"
                ],
                'merchants': [
                    "كارفور", "Carrefour", "سبينس", "Spinneys", "المحل",
                    "مطعم الشواية", "McDonald's", "KFC", "Pizza Hut",
                    "مخبز", "البقالة", "السوبرماركت", "Metro", "Kazyon",
                    "Talabat", "طلبات", "كوستا", "Costa", "Cilantro",
                    "مطعم", "Restaurant", "كشري أبو طارق", "Zooba"
                ]
            },
            
            "Transportation": {
                'msa': [
                    "أجرة سيارة {merchant}",
                    "شراء وقود من {merchant}",
                    "دفع تذكرة المترو",
                    "صيانة السيارة في {merchant}",
                    "مواقف السيارات {merchant}",
                    "رحلة {merchant}"
                ],
                'egyptian': [
                    "أوبر {merchant}",
                    "بنزين من {merchant}",
                    "تكسي {merchant}",
                    "تصليح العربية في {merchant}",
                    "باركينج {merchant}",
                    "رحلة كريم {merchant}"
                ],
                'mixed': [
                    "دفع {merchant} ride",
                    "شراء fuel من {merchant}",
                    "{merchant} taxi fare",
                    "Car maintenance في {merchant}",
                    "{merchant} parking"
                ],
                'arabizi': [
                    "uber ride {merchant}",
                    "benzeen mn {merchant}",
                    "taxi fare",
                    "sa77 mn {merchant}"
                ],
                'english': [
                    "Uber ride",
                    "Fuel from {merchant}",
                    "Metro ticket",
                    "Car wash {merchant}",
                    "Parking {merchant}"
                ],
                'merchants': [
                    "أوبر", "Uber", "كريم", "Careem", "إنديجو", "Indigo",
                    "Shell", "شل", "Total", "توتال", "Wataniya",
                    "المترو", "Metro", "مواقف", "Parking", "CNG",
                    "محطة بنزين", "Gas Station", "تاكسي", "Taxi"
                ]
            },
            
            "Shopping & Retail": {
                'msa': [
                    "شراء منتجات من {merchant}",
                    "دفع ثمن الملابس من {merchant}",
                    "شراء الكترونيات من {merchant}",
                    "طلب عبر الإنترنت من {merchant}",
                    "شراء أدوات منزلية من {merchant}"
                ],
                'egyptian': [
                    "اشتريت من {merchant}",
                    "دفعت فلوس {merchant}",
                    "شريت هدوم من {merchant}",
                    "طلبت من {merchant} أونلاين",
                    "شراء حاجات من {merchant}"
                ],
                'mixed': [
                    "شراء من {merchant} store",
                    "{merchant} online shopping",
                    "دفع {merchant} purchase",
                    "Shopping من {merchant}",
                    "{merchant} order"
                ],
                'arabizi': [
                    "eshtarayt mn {merchant}",
                    "online order mn {merchant}",
                    "{merchant} shopping",
                    "shera2 mn {merchant}"
                ],
                'english': [
                    "{merchant} purchase",
                    "Online order from {merchant}",
                    "{merchant} shopping",
                    "Clothes from {merchant}",
                    "{merchant} electronics"
                ],
                'merchants': [
                    "Amazon.eg", "أمازون", "Jumia", "جوميا", "نون", "Noon",
                    "Carrefour", "كارفور", "Centrepoint", "سنتربوينت",
                    "H&M", "Zara", "زارا", "LC Waikiki", "Defacto",
                    "Extra", "إكسترا", "B.TECH", "Mobiles Shop", "Mall"
                ]
            },
            
            "Entertainment & Recreation": {
                'msa': [
                    "اشتراك شهري في {merchant}",
                    "تذكرة السينما {merchant}",
                    "اشتراك في {merchant}",
                    "دفع رسوم {merchant}"
                ],
                'egyptian': [
                    "اشتراك {merchant} الشهري",
                    "تذكرة سينما {merchant}",
                    "دفعت {merchant}",
                    "جيم {merchant}"
                ],
                'mixed': [
                    "اشتراك {merchant} subscription",
                    "{merchant} monthly fee",
                    "دفع {merchant} membership",
                    "Cinema ticket {merchant}"
                ],
                'arabizi': [
                    "{merchant} subscription",
                    "cinema ticket",
                    "gym membership",
                    "{merchant} monthly"
                ],
                'english': [
                    "{merchant} subscription",
                    "Cinema ticket",
                    "{merchant} membership",
                    "Gym payment {merchant}"
                ],
                'merchants': [
                    "Netflix", "نتفليكس", "Spotify", "سبوتيفاي",
                    "شاهد", "Shahid", "OSN", "watch it", "واتش إت",
                    "Gym", "جيم", "Gold's Gym", "Fitness First",
                    "سينما", "Cinema", "VOX", "Galaxy", "Zawya"
                ]
            },
            
            "Healthcare & Medical": {
                'msa': [
                    "شراء أدوية من {merchant}",
                    "زيارة طبيب في {merchant}",
                    "تحاليل طبية في {merchant}",
                    "دفع فاتورة {merchant}",
                    "كشف طبي في {merchant}"
                ],
                'egyptian': [
                    "اشتريت دوا من {merchant}",
                    "كشفت عند الدكتور {merchant}",
                    "عملت تحاليل في {merchant}",
                    "دفعت {merchant}",
                    "صيدلية {merchant}"
                ],
                'mixed': [
                    "شراء medicine من {merchant}",
                    "Doctor visit في {merchant}",
                    "{merchant} pharmacy",
                    "Lab tests في {merchant}"
                ],
                'arabizi': [
                    "pharmacy {merchant}",
                    "doctor visit",
                    "lab tests {merchant}",
                    "dawaa mn {merchant}"
                ],
                'english': [
                    "{merchant} pharmacy",
                    "Medical checkup at {merchant}",
                    "Lab tests {merchant}",
                    "{merchant} hospital"
                ],
                'merchants': [
                    "صيدليات", "Pharmacy", "19011", "الدواء", "El Ezaby",
                    "مستشفى", "Hospital", "Cleopatra", "كليوباترا",
                    "Lab", "مختبر", "معمل", "LabPlus", "Alpha Lab",
                    "Clinic", "عيادة", "Dr. Clinic", "Vezeeta"
                ]
            },
            
            "Utilities & Services": {
                'msa': [
                    "دفع فاتورة {merchant}",
                    "دفع اشتراك {merchant}",
                    "فاتورة الكهرباء {merchant}",
                    "فاتورة المياه",
                    "فاتورة الإنترنت {merchant}"
                ],
                'egyptian': [
                    "دفعت فاتورة {merchant}",
                    "فاتورة الكهربا",
                    "فاتورة النت {merchant}",
                    "موبايل {merchant}",
                    "بيل {merchant}"
                ],
                'mixed': [
                    "دفع {merchant} bill",
                    "{merchant} internet bill",
                    "Electricity bill",
                    "{merchant} mobile recharge"
                ],
                'arabizi': [
                    "{merchant} bill",
                    "internet bill",
                    "kahraba bill",
                    "mobile recharge"
                ],
                'english': [
                    "{merchant} electricity bill",
                    "Internet bill {merchant}",
                    "{merchant} mobile",
                    "Water bill"
                ],
                'merchants': [
                    "الكهرباء", "Electricity", "كهرباء", "شركة الكهرباء",
                    "Vodafone", "فودافون", "Orange", "أورانج",
                    "Etisalat", "اتصالات", "WE", "وي",
                    "TE Data", "تي إي داتا", "Water", "مياه", "Gas", "غاز"
                ]
            },
            
            "Financial Services": {
                'msa': [
                    "رسوم بنكية {merchant}",
                    "سداد قرض {merchant}",
                    "دفع قسط {merchant}",
                    "رسوم تأمين {merchant}",
                    "رسوم خدمة {merchant}"
                ],
                'egyptian': [
                    "رسوم البنك {merchant}",
                    "قسط {merchant}",
                    "دفعت للبنك {merchant}",
                    "سحب من الـ ATM",
                    "رسوم كارت {merchant}"
                ],
                'mixed': [
                    "{merchant} bank fees",
                    "Credit card payment {merchant}",
                    "ATM withdrawal",
                    "Insurance payment {merchant}"
                ],
                'arabizi': [
                    "bank fees {merchant}",
                    "ATM withdrawal",
                    "qest {merchant}",
                    "credit card"
                ],
                'english': [
                    "{merchant} bank fees",
                    "Loan installment",
                    "ATM withdrawal",
                    "{merchant} credit card"
                ],
                'merchants': [
                    "البنك", "Bank", "CIB", "NBE", "الأهلي",
                    "بنك مصر", "Banque Misr", "QNB", "HSBC",
                    "ATM", "ماكينة صراف", "Visa", "فيزا",
                    "Mastercard", "ماستركارد", "Insurance", "تأمين"
                ]
            },
            
            "Income": {
                'msa': [
                    "استلام الراتب الشهري",
                    "دفعة من {source}",
                    "تحويل من {source}",
                    "استلام أتعاب {source}",
                    "عمولة من {source}"
                ],
                'egyptian': [
                    "المرتب",
                    "فلوس من {source}",
                    "حوالة من {source}",
                    "دفعة شغل من {source}",
                    "كاش من {source}"
                ],
                'mixed': [
                    "Salary transfer",
                    "Payment من {source}",
                    "Freelance payment",
                    "تحويل من {source}"
                ],
                'arabizi': [
                    "salary",
                    "7awala mn {source}",
                    "payment mn {source}",
                    "morta  b"
                ],
                'english': [
                    "Monthly salary",
                    "Payment from {source}",
                    "Transfer from {source}",
                    "Freelance payment"
                ],
                'merchants': [
                    "الشركة", "Company", "العميل", "Client",
                    "Employer", "صاحب العمل", "Customer", "زبون",
                    "Freelance", "فريلانس", "Business", "شغل",
                    "Transfer", "تحويل", "Payment", "دفعة"
                ]
            },
            
            "Government & Legal": {
                'msa': [
                    "دفع رسوم حكومية",
                    "تجديد رخصة {service}",
                    "دفع ضريبة",
                    "رسوم {service}",
                    "استخراج {service}"
                ],
                'egyptian': [
                    "رسوم حكومية",
                    "جددت الرخصة {service}",
                    "دفعت ضرايب",
                    "رسوم {service}",
                    "طلعت {service}"
                ],
                'mixed': [
                    "Government fees",
                    "License renewal {service}",
                    "Tax payment",
                    "رسوم {service}"
                ],
                'arabizi': [
                    "government fees",
                    "license renewal",
                    "tax payment",
                    "rokhsa"
                ],
                'english': [
                    "Government fees",
                    "License renewal",
                    "Tax payment",
                    "{service} fees"
                ],
                'merchants': [
                    "الحكومة", "Government", "السجل المدني",
                    "Traffic Dept", "المرور", "الضرائب", "Tax Authority",
                    "مصلحة الضرائب", "License", "رخصة",
                    "Legal", "قانوني", "Court", "محكمة"
                ]
            },
            
            "Charity & Donations": {
                'msa': [
                    "تبرع لـ {charity}",
                    "دفع صدقة {charity}",
                    "تبرع خيري {charity}",
                    "مساهمة في {charity}"
                ],
                'egyptian': [
                    "تبرعت لـ {charity}",
                    "صدقة {charity}",
                    "دفعت تبرع {charity}",
                    "تبرع {charity}"
                ],
                'mixed': [
                    "Donation to {charity}",
                    "تبرع لـ {charity}",
                    "Charity {charity}"
                ],
                'arabizi': [
                    "donation {charity}",
                    "sadaqa",
                    "tabar3 {charity}"
                ],
                'english': [
                    "Donation to {charity}",
                    "Charity {charity}",
                    "Contribution to {charity}"
                ],
                'merchants': [
                    "جمعية خيرية", "Charity", "مسجد", "Mosque",
                    "Resala", "رسالة", "57357", "مستشفى ٥٧٣٥٧",
                    "كنيسة", "Church", "جمعية", "Association",
                    "Misr El Kheir", "مصر الخير", "Orphanage", "دار أيتام"
                ]
            }
        }
        
        return templates
    
    def _introduce_spelling_errors(self, text):
        """Introduce realistic spelling errors"""
        errors = {
            'الكهرباء': 'الكهربا',
            'مشتريات': 'مشترياات',
            'مصاريف': 'مصاريفف',
            'صيدلية': 'صيدليه',
            'محل': 'محلل',
            'فاتورة': 'فاتوره',
            'شراء': 'شرا',
            'دفع': 'دفعع'
        }
        
        for correct, error in errors.items():
            if correct in text and random.random() < 0.3:
                text = text.replace(correct, error)
        
        return text
    
    def _introduce_formatting_variations(self, text):
        """Introduce formatting variations"""
        variations = [
            lambda t: t.upper() if random.random() < 0.2 else t,
            lambda t: t.lower() if random.random() < 0.2 else t,
            lambda t: t.replace(' ', '_') if random.random() < 0.1 else t,
            lambda t: t.replace(' ', '-') if random.random() < 0.1 else t,
            lambda t: t + '  ' if random.random() < 0.1 else t,
            lambda t: '  ' + t if random.random() < 0.1 else t
        ]
        
        for variation in variations:
            text = variation(text)
        
        return text
    
    def _make_incomplete(self, text):
        """Make description incomplete"""
        incomplete_patterns = [
            "دفع فاتورة",
            "شراء من محل",
            "تحويل بنكي",
            "payment",
            "ATM withdrawal",
            "transfer"
        ]
        
        if random.random() < 0.5:
            return random.choice(incomplete_patterns)
        return text
    
    def generate_transaction(self, category, quality_profile='clean', language_style=None):
        """Generate a single transaction"""
        
        if language_style is None:
            language_style = random.choices(
                list(self.language_styles.keys()),
                weights=list(self.language_styles.values())
            )[0]
        
        templates = self.category_templates[category]
        
        # Select template and merchant
        if language_style in templates:
            template = random.choice(templates[language_style])
            merchant = random.choice(templates['merchants'])
            
            # Format with all possible placeholders
            try:
                description = template.format(
                    merchant=merchant,
                    source=merchant,
                    service=merchant,
                    charity=merchant
                )
            except KeyError:
                # If template doesn't have placeholders, use as is
                description = template
        else:
            # Fallback to MSA
            template = random.choice(templates['msa'])
            merchant = random.choice(templates['merchants'])
            description = template.format(merchant=merchant, source=merchant, service=merchant, charity=merchant)
        
        # Apply quality profile
        if quality_profile == 'spelling_errors':
            description = self._introduce_spelling_errors(description)
        elif quality_profile == 'mixed_language':
            # Already handled by language_style
            pass
        elif quality_profile == 'incomplete':
            if random.random() < 0.5:
                description = self._make_incomplete(description)
        
        # Apply formatting variations occasionally
        if random.random() < 0.2:
            description = self._introduce_formatting_variations(description)
        
        return {
            'transaction_description': description,
            'category': category,
            'country': COUNTRY,
            'currency': CURRENCY
        }
    
    def generate_dataset(self, n_records=10000, category_distribution=None):
        """Generate complete dataset"""
        
        print(f"🔄 Generating {n_records:,} Egyptian transaction records...")
        
        # Default imbalanced distribution
        if category_distribution is None:
            category_distribution = {
                "Food & Dining": 0.18,
                "Transportation": 0.15,
                "Shopping & Retail": 0.14,
                "Entertainment & Recreation": 0.11,
                "Healthcare & Medical": 0.09,
                "Utilities & Services": 0.12,
                "Financial Services": 0.08,
                "Income": 0.05,
                "Government & Legal": 0.04,
                "Charity & Donations": 0.04
            }
        
        records = []
        
        for _ in range(n_records):
            # Select category
            category = random.choices(
                list(category_distribution.keys()),
                weights=list(category_distribution.values())
            )[0]
            
            # Select quality profile
            quality_profile = random.choices(
                list(self.quality_profiles.keys()),
                weights=list(self.quality_profiles.values())
            )[0]
            
            # Generate transaction
            transaction = self.generate_transaction(category, quality_profile)
            records.append(transaction)
        
        df = pd.DataFrame(records)
        
        print(f"✅ Generated {len(df):,} records")
        return df


def create_splits(df, train_ratio=0.70, val_ratio=0.15, test_ratio=0.15, seed=42):
    """Create train/validation/test splits"""
    
    print("\n🔀 Creating dataset splits...")
    
    # Remove exact duplicates
    df = df.drop_duplicates(subset=['transaction_description']).reset_index(drop=True)
    
    # Shuffle
    df = df.sample(frac=1, random_state=seed).reset_index(drop=True)
    
    n = len(df)
    train_end = int(n * train_ratio)
    val_end = train_end + int(n * val_ratio)
    
    train_df = df[:train_end].reset_index(drop=True)
    val_df = df[train_end:val_end].reset_index(drop=True)
    test_df = df[val_end:].reset_index(drop=True)
    
    print(f"  Train: {len(train_df):,} ({len(train_df)/n*100:.1f}%)")
    print(f"  Validation: {len(val_df):,} ({len(val_df)/n*100:.1f}%)")
    print(f"  Test: {len(test_df):,} ({len(test_df)/n*100:.1f}%)")
    
    return train_df, val_df, test_df


def add_label_noise(df, noise_rate=0.05, seed=42):
    """Add controlled label noise"""
    
    print(f"\n🔀 Adding {noise_rate*100:.0f}% label noise...")
    
    df = df.copy()
    df['true_category'] = df['category'].copy()
    
    n_corrupt = int(len(df) * noise_rate)
    corrupt_indices = np.random.choice(df.index, size=n_corrupt, replace=False)
    
    for idx in corrupt_indices:
        true_cat = df.loc[idx, 'category']
        other_cats = [c for c in CATEGORIES if c != true_cat]
        df.loc[idx, 'category'] = random.choice(other_cats)
    
    print(f"  Corrupted {n_corrupt:,} labels")
    return df


def generate_quality_report(df, output_dir='reports'):
    """Generate dataset quality report"""
    
    print("\n📊 Generating quality report...")
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Statistics
    stats = {
        'Total Records': len(df),
        'Unique Descriptions': df['transaction_description'].nunique(),
        'Duplicate Rate (%)': (1 - df['transaction_description'].nunique()/len(df)) * 100,
        'Missing Values': df.isnull().sum().sum(),
        'Categories': df['category'].nunique(),
        'Avg Description Length': df['transaction_description'].str.len().mean(),
        'Min Description Length': df['transaction_description'].str.len().min(),
        'Max Description Length': df['transaction_description'].str.len().max()
    }
    
    # Category distribution
    cat_dist = df['category'].value_counts()
    
    # Save stats
    with open(f'{output_dir}/data_quality_summary.txt', 'w', encoding='utf-8') as f:
        f.write("="*60 + "\n")
        f.write("DATASET QUALITY REPORT\n")
        f.write("="*60 + "\n\n")
        
        f.write("Overall Statistics:\n")
        f.write("-"*60 + "\n")
        for key, value in stats.items():
            f.write(f"{key:<30}: {value}\n")
        
        f.write("\n\nCategory Distribution:\n")
        f.write("-"*60 + "\n")
        for cat, count in cat_dist.items():
            pct = (count / len(df)) * 100
            f.write(f"{cat:<35}: {count:>6,} ({pct:>5.1f}%)\n")
    
    # Visualization
    plt.figure(figsize=(12, 6))
    cat_dist.plot(kind='bar', color='skyblue')
    plt.title('Category Distribution', fontsize=14, fontweight='bold')
    plt.xlabel('Category')
    plt.ylabel('Count')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/category_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✅ Quality report saved to {output_dir}/")
    
    return stats


def main():
    """Main generation pipeline"""
    
    print("="*70)
    print("EGYPTIAN ARABIC FINANCIAL TRANSACTION DATASET GENERATOR")
    print("="*70)
    print(f"\nFixed values: country={COUNTRY}, currency={CURRENCY}")
    print(f"Categories: {len(CATEGORIES)}")
    print(f"Random seed: {RANDOM_SEED}\n")
    
    # Create directories
    os.makedirs('data', exist_ok=True)
    os.makedirs('reports', exist_ok=True)
    
    # Initialize generator
    generator = EgyptianTransactionGenerator(seed=RANDOM_SEED)
    
    # Generate main dataset
    df_full = generator.generate_dataset(n_records=10000)
    
    # Save clean dataset
    df_full.to_csv('data/arabic_transactions_clean.csv', index=False, encoding='utf-8-sig')
    df_full.to_parquet('data/arabic_transactions_clean.parquet', index=False)
    print(f"\n✅ Saved: data/arabic_transactions_clean.csv")
    print(f"✅ Saved: data/arabic_transactions_clean.parquet")
    
    # Create splits
    train_df, val_df, test_df = create_splits(df_full)
    
    train_df.to_csv('data/arabic_transactions_train.csv', index=False, encoding='utf-8-sig')
    val_df.to_csv('data/arabic_transactions_validation.csv', index=False, encoding='utf-8-sig')
    test_df.to_csv('data/arabic_transactions_test.csv', index=False, encoding='utf-8-sig')
    print(f"\n✅ Saved train/validation/test splits")
    
    # Generate noisy labels (2%)
    noisy_df_2 = add_label_noise(train_df.copy(), noise_rate=0.02)
    noisy_df_2.to_csv('data/arabic_transactions_noisy_2pct.csv', index=False, encoding='utf-8-sig')
    
    # Generate noisy labels (5%)
    noisy_df_5 = add_label_noise(train_df.copy(), noise_rate=0.05)
    noisy_df_5.to_csv('data/arabic_transactions_noisy_5pct.csv', index=False, encoding='utf-8-sig')
    print(f"✅ Saved noisy label datasets (2% and 5%)")
    
    # Generate quality report
    stats = generate_quality_report(df_full)
    
    # Generate samples
    print("\n📝 Sample transactions:")
    for cat in CATEGORIES[:3]:
        samples = df_full[df_full['category'] == cat].head(2)
        print(f"\n{cat}:")
        for _, row in samples.iterrows():
            print(f"  • {row['transaction_description']}")
    
    print("\n" + "="*70)
    print("✅ DATASET GENERATION COMPLETE!")
    print("="*70)
    print(f"\nFiles created:")
    print(f"  • data/arabic_transactions_clean.csv")
    print(f"  • data/arabic_transactions_clean.parquet")
    print(f"  • data/arabic_transactions_train.csv")
    print(f"  • data/arabic_transactions_validation.csv")
    print(f"  • data/arabic_transactions_test.csv")
    print(f"  • data/arabic_transactions_noisy_2pct.csv")
    print(f"  • data/arabic_transactions_noisy_5pct.csv")
    print(f"  • reports/data_quality_summary.txt")
    print(f"  • reports/category_distribution.png")


if __name__ == "__main__":
    main()
