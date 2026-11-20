"""
Egyptian Arabic-Only Financial Transaction Dataset Generator
Generates transactions with ONLY Arabic descriptions (no English, no mixed)

Features:
- Modern Standard Arabic (MSA)
- Egyptian Colloquial Arabic
- Realistic imperfections
- 10,000 records
- Fixed: Egypt, EGP
"""

import pandas as pd
import numpy as np
import random
import os
from datetime import datetime

# Set random seeds
RANDOM_SEED = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

# Fixed values
COUNTRY = "Egypt"
CURRENCY = "EGP"

# Categories (in English)
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

# Category weights (realistic distribution)
CATEGORY_WEIGHTS = [0.178, 0.154, 0.139, 0.117, 0.087, 0.118, 0.079, 0.049, 0.038, 0.041]

# Arabic merchants and entities
MERCHANTS = {
    "Food & Dining": [
        "البقالة", "السوبرماركت", "المطعم", "المقهى", "الكافيه", "الفرن",
        "محل البقالة", "السوبر ماركت", "مطعم الشواية", "كافتيريا الحي",
        "بقالة الركن", "فرن البلد", "مطعم الأسماك", "كافيه المدينة",
        "محل الفواكه", "سوبر ماركت الأسرة", "مطعم الكباب", "المخبز"
    ],
    "Transportation": [
        "التاكسي", "المترو", "الأتوبيس", "محطة البنزين", "موقف السيارات",
        "الميكروباص", "محطة الوقود", "تكسي", "المواصلات", "محطة مترو",
        "موقف العربيات", "الجراج", "محطة توتال", "محطة موبيل", "تاكسي أبيض",
        "أوبر", "كريم", "سواقة", "المحطة"
    ],
    "Shopping & Retail": [
        "المحل", "المول", "السوق", "المتجر", "محل الملابس", "محل الأحذية",
        "سيتي سنتر", "كارفور", "هايبر وان", "محل الإلكترونيات",
        "محل الموبايلات", "محلات الذهب", "محل الأثاث", "السوق التجاري",
        "المركز التجاري", "محل الهدايا", "بوتيك", "معرض"
    ],
    "Entertainment & Recreation": [
        "السينما", "النادي", "الملاهي", "الحديقة", "المسرح", "الصالة الرياضية",
        "صالة الألعاب", "الجيم", "نادي اللياقة", "حمام السباحة",
        "ملاعب كرة القدم", "ملعب", "صالة البولينج", "كافيه نت",
        "مركز الترفيه", "حديقة الحيوان", "المتحف", "قاعة الأفراح"
    ],
    "Healthcare & Medical": [
        "المستشفى", "العيادة", "الصيدلية", "المعمل", "مركز الأشعة",
        "عيادة الدكتور", "مستشفى", "صيدلية", "معمل التحاليل",
        "مركز طبي", "عيادة الأسنان", "دكتور", "طبيب",
        "المركز الطبي", "مستوصف", "عيادة خاصة", "المختبر"
    ],
    "Utilities & Services": [
        "شركة الكهرباء", "شركة المياه", "شركة الغاز", "الاتصالات",
        "الإنترنت", "فاتورة الكهرباء", "فاتورة المياه", "فاتورة التليفون",
        "فاتورة النت", "شركة فودافون", "شركة أورانج", "شركة اتصالات",
        "شركة تي إي داتا", "فاتورة الموبايل", "الخط الأرضي", "شحن الموبايل"
    ],
    "Financial Services": [
        "البنك", "ماكينة الصراف", "بنك", "الصراف الآلي", "البنك الأهلي",
        "بنك مصر", "البنك التجاري", "القرض", "التمويل", "التحويل البنكي",
        "رسوم البنك", "فوائد القرض", "قسط القرض", "رسوم الكارت",
        "الحساب البنكي", "خدمة بنكية", "رسوم خدمة"
    ],
    "Income": [
        "الراتب", "المرتب", "الشغل", "الشركة", "العمل", "الدخل",
        "المكافأة", "البونص", "الحوافز", "العمولة", "الأجر",
        "راتب الشهر", "مرتب", "دخل إضافي", "مكافأة نهاية الخدمة"
    ],
    "Government & Legal": [
        "المحكمة", "مصلحة الضرائب", "السجل المدني", "المرور",
        "الجوازات", "مجمع التحرير", "الشهر العقاري", "النيابة",
        "قسم الشرطة", "رسوم حكومية", "الجمارك", "التأمينات",
        "المصلحة الحكومية", "مبنى المحافظة", "الوحدة المحلية"
    ],
    "Charity & Donations": [
        "الجمعية الخيرية", "المسجد", "الكنيسة", "دار الأيتام",
        "جمعية", "المؤسسة الخيرية", "صدقة", "زكاة", "تبرع",
        "مستشفى السرطان", "بيت الزكاة", "رسالة", "جمعية خيرية",
        "الهلال الأحمر", "مؤسسة خيرية", "دار رعاية"
    ]
}

# MSA templates (Modern Standard Arabic)
MSA_TEMPLATES = {
    "Food & Dining": [
        "شراء مواد غذائية من {merchant}",
        "دفع فاتورة {merchant}",
        "شراء وجبة من {merchant}",
        "شراء خبز من {merchant}",
        "دفع ثمن الطعام في {merchant}",
        "شراء من {merchant}",
        "وجبة في {merchant}",
        "طلب طعام من {merchant}"
    ],
    "Transportation": [
        "دفع أجرة {merchant}",
        "تذكرة {merchant}",
        "دفع ثمن الوقود في {merchant}",
        "رسوم {merchant}",
        "أجرة السيارة {merchant}",
        "ركوب {merchant}",
        "رحلة {merchant}",
        "دفع مقابل {merchant}"
    ],
    "Shopping & Retail": [
        "شراء من {merchant}",
        "تسوق من {merchant}",
        "شراء ملابس من {merchant}",
        "شراء منتجات من {merchant}",
        "دفع ثمن المشتريات في {merchant}",
        "شراء مستلزمات من {merchant}",
        "تسوق في {merchant}",
        "شراء أغراض من {merchant}"
    ],
    "Entertainment & Recreation": [
        "تذكرة دخول {merchant}",
        "اشتراك في {merchant}",
        "دفع رسوم {merchant}",
        "دخول {merchant}",
        "رسوم العضوية في {merchant}",
        "اشتراك شهري في {merchant}",
        "زيارة {merchant}",
        "دفع مقابل {merchant}"
    ],
    "Healthcare & Medical": [
        "كشف عند {merchant}",
        "شراء دواء من {merchant}",
        "تحاليل في {merchant}",
        "أشعة في {merchant}",
        "دفع فاتورة {merchant}",
        "علاج في {merchant}",
        "فحص طبي في {merchant}",
        "زيارة {merchant}"
    ],
    "Utilities & Services": [
        "فاتورة {merchant}",
        "دفع فاتورة {merchant}",
        "اشتراك {merchant}",
        "رسوم {merchant}",
        "دفع مستحقات {merchant}",
        "خدمة {merchant}",
        "سداد فاتورة {merchant}",
        "رسوم خدمة {merchant}"
    ],
    "Financial Services": [
        "رسوم {merchant}",
        "قسط {merchant}",
        "تحويل من {merchant}",
        "رسوم خدمة {merchant}",
        "دفع مستحقات {merchant}",
        "سحب من {merchant}",
        "عمولة {merchant}",
        "خدمة بنكية من {merchant}"
    ],
    "Income": [
        "راتب من {merchant}",
        "مرتب {merchant}",
        "دخل من {merchant}",
        "تحويل من {merchant}",
        "مكافأة من {merchant}",
        "أجر {merchant}",
        "حوافز {merchant}",
        "عمولة من {merchant}"
    ],
    "Government & Legal": [
        "رسوم {merchant}",
        "دفع في {merchant}",
        "استخراج من {merchant}",
        "تجديد في {merchant}",
        "رسوم حكومية في {merchant}",
        "معاملة في {merchant}",
        "غرامة {merchant}",
        "خدمة {merchant}"
    ],
    "Charity & Donations": [
        "تبرع لـ {merchant}",
        "صدقة في {merchant}",
        "دفع زكاة لـ {merchant}",
        "تبرع في {merchant}",
        "مساهمة في {merchant}",
        "صدقة لـ {merchant}",
        "تبرع خيري لـ {merchant}",
        "دعم {merchant}"
    ]
}

# Egyptian Colloquial templates
EGYPTIAN_TEMPLATES = {
    "Food & Dining": [
        "اشتريت أكل من {merchant}",
        "دفعت فلوس {merchant}",
        "جبت أكل من {merchant}",
        "اشتريت من {merchant}",
        "دفعت في {merchant}",
        "خدت أكل من {merchant}",
        "روحت {merchant}",
        "جبت حاجات من {merchant}"
    ],
    "Transportation": [
        "ركبت {merchant}",
        "دفعت أجرة {merchant}",
        "خدت {merchant}",
        "ركوب {merchant}",
        "دفعت للسواق {merchant}",
        "أجرة {merchant}",
        "نزلت من {merchant}",
        "رحلة {merchant}"
    ],
    "Shopping & Retail": [
        "اشتريت من {merchant}",
        "جبت حاجات من {merchant}",
        "شريت من {merchant}",
        "خدت من {merchant}",
        "دفعت في {merchant}",
        "اشتريت حاجة من {merchant}",
        "روحت {merchant}",
        "جبت حاجة من {merchant}"
    ],
    "Entertainment & Recreation": [
        "روحت {merchant}",
        "دفعت في {merchant}",
        "اشتركت في {merchant}",
        "دخلت {merchant}",
        "لعبت في {merchant}",
        "قعدت في {merchant}",
        "زرت {merchant}",
        "رحت {merchant}"
    ],
    "Healthcare & Medical": [
        "كشفت عند {merchant}",
        "روحت {merchant}",
        "عملت تحاليل في {merchant}",
        "اشتريت دوا من {merchant}",
        "دفعت في {merchant}",
        "جبت دوا من {merchant}",
        "عملت أشعة في {merchant}",
        "زرت {merchant}"
    ],
    "Utilities & Services": [
        "دفعت فاتورة {merchant}",
        "دفعت {merchant}",
        "سددت {merchant}",
        "دفعت بيل {merchant}",
        "فاتورة {merchant}",
        "دفعت فلوس {merchant}",
        "سددت فاتورة {merchant}",
        "بيل {merchant}"
    ],
    "Financial Services": [
        "دفعت للبنك {merchant}",
        "سحبت من {merchant}",
        "دفعت قسط {merchant}",
        "حولت من {merchant}",
        "دفعت في {merchant}",
        "رسوم {merchant}",
        "دفعت فلوس {merchant}",
        "معاملة {merchant}"
    ],
    "Income": [
        "المرتب من {merchant}",
        "جالي فلوس من {merchant}",
        "راتب {merchant}",
        "حولولي من {merchant}",
        "مرتب {merchant}",
        "دخلولي فلوس من {merchant}",
        "استلمت من {merchant}",
        "فلوس من {merchant}"
    ],
    "Government & Legal": [
        "طلعت من {merchant}",
        "دفعت في {merchant}",
        "روحت {merchant}",
        "عملت معاملة في {merchant}",
        "دفعت رسوم {merchant}",
        "استخرجت من {merchant}",
        "جددت في {merchant}",
        "معاملة {merchant}"
    ],
    "Charity & Donations": [
        "تبرعت لـ {merchant}",
        "دفعت صدقة في {merchant}",
        "تبرعت في {merchant}",
        "دفعت لـ {merchant}",
        "ساهمت في {merchant}",
        "صدقة {merchant}",
        "تبرع {merchant}",
        "دفعت زكاة {merchant}"
    ]
}

def generate_description(category, language_style='msa'):
    """Generate Arabic-only transaction description"""
    
    # Choose template set
    if language_style == 'msa' or language_style not in ['msa', 'egyptian']:
        templates = MSA_TEMPLATES
    else:
        templates = EGYPTIAN_TEMPLATES
    
    # Get merchant
    merchant = random.choice(MERCHANTS[category])
    
    # Get template
    template = random.choice(templates[category])
    
    # Format
    try:
        description = template.format(merchant=merchant)
    except:
        description = template.replace('{merchant}', merchant)
    
    return description

def add_imperfections(text, quality_type):
    """Add realistic imperfections to text"""
    
    if quality_type == 'clean':
        return text
    
    elif quality_type == 'spelling_errors':
        # Common Arabic typos
        typos = {
            'ا': 'أ', 'أ': 'ا', 'إ': 'ا', 'ي': 'ى', 'ى': 'ي',
            'ة': 'ه', 'ه': 'ة', 'و': 'ؤ', 'ؤ': 'و'
        }
        chars = list(text)
        if len(chars) > 3:
            idx = random.randint(1, len(chars) - 2)
            if chars[idx] in typos:
                chars[idx] = typos[chars[idx]]
        return ''.join(chars)
    
    elif quality_type == 'incomplete':
        # Truncate text
        if len(text) > 10:
            cut_point = random.randint(int(len(text) * 0.6), len(text) - 3)
            return text[:cut_point]
        return text
    
    elif quality_type == 'ambiguous':
        # Make it shorter/vaguer
        words = text.split()
        if len(words) > 2:
            return ' '.join(words[:2])
        return text
    
    return text

def generate_dataset(n_records=10000):
    """Generate complete Arabic-only dataset"""
    
    print("="*70)
    print("ARABIC-ONLY EGYPTIAN TRANSACTION DATASET GENERATOR")
    print("="*70)
    print(f"Fixed values: country={COUNTRY}, currency={CURRENCY}")
    print(f"Categories: {len(CATEGORIES)}")
    print(f"Random seed: {RANDOM_SEED}")
    print(f" Generating {n_records:,} Arabic-only Egyptian transaction records...")
    
    records = []
    
    # Quality distribution
    quality_types = list({
        'clean': 0.55,
        'spelling_errors': 0.15,
        'incomplete': 0.10,
        'ambiguous': 0.20
    }.keys())
    quality_weights = [0.55, 0.15, 0.10, 0.20]
    
    # Language style distribution (MSA vs Egyptian)
    language_styles = ['msa', 'egyptian']
    language_weights = [0.45, 0.55]  # More Egyptian colloquial
    
    for i in range(n_records):
        # Select category
        category = random.choices(CATEGORIES, weights=CATEGORY_WEIGHTS)[0]
        
        # Select language style
        lang_style = random.choices(language_styles, weights=language_weights)[0]
        
        # Generate description
        description = generate_description(category, lang_style)
        
        # Add imperfections
        quality = random.choices(quality_types, weights=quality_weights)[0]
        description = add_imperfections(description, quality)
        
        # Create record
        records.append({
            'transaction_description': description,
            'category': category,
            'country': COUNTRY,
            'currency': CURRENCY
        })
    
    df = pd.DataFrame(records)
    
    print(f" Generated {len(df):,} records")
    
    return df

def main():
    """Main execution"""
    
    # Create directories
    os.makedirs('data', exist_ok=True)
    os.makedirs('reports', exist_ok=True)
    
    # Generate dataset
    df = generate_dataset(10000)
    
    # Save main file
    df.to_csv('data/arabic_only_transactions.csv', index=False, encoding='utf-8')
    print(f" Saved: data/arabic_only_transactions.csv")
    
    df.to_parquet('data/arabic_only_transactions.parquet', index=False)
    print(f" Saved: data/arabic_only_transactions.parquet")
    
    # Create splits
    print(" Creating dataset splits...")
    
    # Shuffle
    df = df.sample(frac=1, random_state=RANDOM_SEED).reset_index(drop=True)
    
    # Split sizes
    n_total = len(df)
    n_train = int(n_total * 0.70)
    n_val = int(n_total * 0.15)
    
    train_df = df[:n_train]
    val_df = df[n_train:n_train + n_val]
    test_df = df[n_train + n_val:]
    
    print(f"  Train: {len(train_df):,} ({len(train_df)/n_total*100:.1f}%)")
    print(f"  Validation: {len(val_df):,} ({len(val_df)/n_total*100:.1f}%)")
    print(f"  Test: {len(test_df):,} ({len(test_df)/n_total*100:.1f}%)")
    
    # Save splits
    train_df.to_csv('data/arabic_only_train.csv', index=False, encoding='utf-8')
    val_df.to_csv('data/arabic_only_validation.csv', index=False, encoding='utf-8')
    test_df.to_csv('data/arabic_only_test.csv', index=False, encoding='utf-8')
    print(" Saved train/validation/test splits")
    
    # Generate report
    print(" Generating quality report...")
    
    report = []
    report.append("="*60)
    report.append("ARABIC-ONLY DATASET QUALITY REPORT")
    report.append("="*60)
    report.append("")
    report.append("Overall Statistics:")
    report.append("-"*60)
    report.append(f"Total Records                 : {len(df)}")
    report.append(f"Unique Descriptions           : {df['transaction_description'].nunique()}")
    report.append(f"Duplicate Rate (%)            : {(1 - df['transaction_description'].nunique()/len(df))*100:.1f}")
    report.append(f"Missing Values                : {df.isnull().sum().sum()}")
    report.append(f"Categories                    : {df['category'].nunique()}")
    report.append(f"Avg Description Length        : {df['transaction_description'].str.len().mean():.2f}")
    report.append(f"Min Description Length        : {df['transaction_description'].str.len().min()}")
    report.append(f"Max Description Length        : {df['transaction_description'].str.len().max()}")
    report.append("")
    report.append("")
    report.append("Category Distribution:")
    report.append("-"*60)
    for cat, count in df['category'].value_counts().items():
        pct = (count / len(df)) * 100
        report.append(f"{cat:30s} : {count:5,} ({pct:5.1f}%)")
    report.append("")
    
    report_text = '\n'.join(report)
    
    with open('reports/arabic_only_quality_summary.txt', 'w', encoding='utf-8') as f:
        f.write(report_text)
    
    print(" Quality report saved to reports/")
    
    # Show samples
    print("\n Sample transactions:")
    for cat in random.sample(list(df['category'].unique()), 3):
        samples = df[df['category'] == cat]['transaction_description'].head(2)
        print(f"{cat}:")
        for desc in samples:
            print(f"  • {desc}")
    
    print("\n" + "="*70)
    print(" ARABIC-ONLY DATASET GENERATION COMPLETE!")
    print("="*70)
    print("Files created:")
    print("  • data/arabic_only_transactions.csv")
    print("  • data/arabic_only_transactions.parquet")
    print("  • data/arabic_only_train.csv")
    print("  • data/arabic_only_validation.csv")
    print("  • data/arabic_only_test.csv")
    print("  • reports/arabic_only_quality_summary.txt")
    print()

if __name__ == "__main__":
    main()
