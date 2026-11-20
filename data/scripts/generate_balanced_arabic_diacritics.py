"""
Balanced Arabic Dataset Generator with Diacritics (Tashkeel)
Features:
- Equal distribution across all 10 categories
- Mix of full diacritics (30%) and partial diacritics (40%) and no diacritics (30%)
- Egyptian Colloquial + Modern Standard Arabic
- 10,000 records (1000 per category)
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

# Categories (equal distribution)
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

# Arabic merchants with diacritics
MERCHANTS = {
    "Food & Dining": [
        # Without diacritics
        "البقالة", "السوبرماركت", "المطعم", "المقهى", "الكافيه", "الفرن",
        # Partial diacritics
        "محلّ البقالة", "السوبر ماركت", "مطعم الشوايّة", "كافتيريا الحيّ",
        # Full diacritics
        "بَقَّالَةُ الرُّكْنِ", "فُرْنُ الْبَلَدِ", "مَطْعَمُ الأَسْمَاكِ", "كَافِيهْ الْمَدِينَةِ",
        "مَحَلُّ الْفَوَاكِهِ", "سُوبَرْ مَارْكِتْ الأُسْرَةِ", "مَطْعَمُ الْكَبَابِ", "الْمَخْبَزُ"
    ],
    "Transportation": [
        # Without diacritics
        "التاكسي", "المترو", "الأتوبيس", "محطة البنزين", "موقف السيارات",
        # Partial diacritics
        "الميكروباص", "محطّة الوقود", "تكسي", "المواصلات", "محطّة مترو",
        # Full diacritics
        "مَوْقِفُ الْعَرَبِيَّاتِ", "الْجَرَاجُ", "مَحَطَّةُ تُوتَالْ", "مَحَطَّةُ مُوبِيلْ", "تَاكْسِي أَبْيَضْ",
        "أُوبَرْ", "كَرِيمْ", "سَوَّاقَةٌ", "الْمَحَطَّةُ"
    ],
    "Shopping & Retail": [
        # Without diacritics
        "المحل", "المول", "السوق", "المتجر", "محل الملابس", "محل الأحذية",
        # Partial diacritics
        "سيتي سنتر", "كارفور", "هايبر وان", "محلّ الإلكترونيّات",
        # Full diacritics
        "مَحَلُّ الْمُوبَايْلاتِ", "مَحَلاَّتُ الذَّهَبِ", "مَحَلُّ الأَثَاثِ", "السُّوقُ التِّجَارِيُّ",
        "الْمَرْكَزُ التِّجَارِيُّ", "مَحَلُّ الْهَدَايَا", "بُوتِيكْ", "مَعْرِضٌ"
    ],
    "Entertainment & Recreation": [
        # Without diacritics
        "السينما", "النادي", "الملاهي", "الحديقة", "المسرح", "الصالة الرياضية",
        # Partial diacritics
        "صالة الألعاب", "الجيم", "نادي اللياقة", "حمّام السباحة",
        # Full diacritics
        "مَلاَعِبُ كُرَةِ الْقَدَمِ", "مَلْعَبٌ", "صَالَةُ الْبُولِينْجْ", "كَافِيهْ نِتْ",
        "مَرْكَزُ التَّرْفِيهِ", "حَدِيقَةُ الْحَيَوَانِ", "الْمَتْحَفُ", "قَاعَةُ الأَفْرَاحِ"
    ],
    "Healthcare & Medical": [
        # Without diacritics
        "المستشفى", "العيادة", "الصيدلية", "المعمل", "مركز الأشعة",
        # Partial diacritics
        "عيادة الدكتور", "مستشفى", "صيدليّة", "معمل التحاليل",
        # Full diacritics
        "مَرْكَزٌ طِبِّيٌّ", "عِيَادَةُ الأَسْنَانِ", "دُكْتُورٌ", "طَبِيبٌ",
        "الْمَرْكَزُ الطِّبِّيُّ", "مُسْتَوْصَفٌ", "عِيَادَةٌ خَاصَّةٌ", "الْمُخْتَبَرُ"
    ],
    "Utilities & Services": [
        # Without diacritics
        "شركة الكهرباء", "شركة المياه", "شركة الغاز", "الاتصالات",
        # Partial diacritics
        "الإنترنت", "فاتورة الكهرباء", "فاتورة المياه", "فاتورة التليفون",
        # Full diacritics
        "فَاتُورَةُ النِّتْ", "شَرِكَةُ فُودَافُونْ", "شَرِكَةُ أُورَانْجْ", "شَرِكَةُ اتِّصَالاَتٍ",
        "شَرِكَةُ تِي إِي دَاتَا", "فَاتُورَةُ الْمُوبَايْلِ", "الْخَطُّ الأَرْضِيُّ", "شَحْنُ الْمُوبَايْلِ"
    ],
    "Financial Services": [
        # Without diacritics
        "البنك", "ماكينة الصراف", "بنك", "الصراف الآلي", "البنك الأهلي",
        # Partial diacritics
        "بنك مصر", "البنك التجاري", "القرض", "التمويل", "التحويل البنكي",
        # Full diacritics
        "رُسُومُ الْبَنْكِ", "فَوَائِدُ الْقَرْضِ", "قِسْطُ الْقَرْضِ", "رُسُومُ الْكَارْتِ",
        "الْحِسَابُ الْبَنْكِيُّ", "خِدْمَةٌ بَنْكِيَّةٌ", "رُسُومُ خِدْمَةٍ"
    ],
    "Income": [
        # Without diacritics
        "الراتب", "المرتب", "الشغل", "الشركة", "العمل", "الدخل",
        # Partial diacritics
        "المكافأة", "البونص", "الحوافز", "العمولة", "الأجر",
        # Full diacritics
        "رَاتِبُ الشَّهْرِ", "مُرَتَّبٌ", "دَخْلٌ إِضَافِيٌّ", "مُكَافَأَةُ نِهَايَةِ الْخِدْمَةِ"
    ],
    "Government & Legal": [
        # Without diacritics
        "المحكمة", "مصلحة الضرائب", "السجل المدني", "المرور",
        # Partial diacritics
        "الجوازات", "مجمّع التحرير", "الشهر العقاري", "النيابة",
        # Full diacritics
        "قِسْمُ الشُّرْطَةِ", "رُسُومٌ حُكُومِيَّةٌ", "الْجَمَارِكُ", "التَّأْمِينَاتُ",
        "الْمَصْلَحَةُ الْحُكُومِيَّةُ", "مَبْنَى الْمُحَافَظَةِ", "الْوَحْدَةُ الْمَحَلِّيَّةُ"
    ],
    "Charity & Donations": [
        # Without diacritics
        "الجمعية الخيرية", "المسجد", "الكنيسة", "دار الأيتام",
        # Partial diacritics
        "جمعيّة", "المؤسّسة الخيريّة", "صدقة", "زكاة", "تبرّع",
        # Full diacritics
        "مُسْتَشْفَى السَّرَطَانِ", "بَيْتُ الزَّكَاةِ", "رِسَالَةٌ", "جَمْعِيَّةٌ خَيْرِيَّةٌ",
        "الْهِلاَلُ الأَحْمَرُ", "مُؤَسَّسَةٌ خَيْرِيَّةٌ", "دَارُ رِعَايَةٍ"
    ]
}

# Templates with diacritics variations
TEMPLATES_NO_DIACRITICS = {
    "Food & Dining": [
        "شراء مواد غذائية من {merchant}",
        "دفع فاتورة {merchant}",
        "شراء وجبة من {merchant}",
        "اشتريت أكل من {merchant}",
        "دفعت فلوس {merchant}",
        "جبت أكل من {merchant}"
    ],
    "Transportation": [
        "دفع أجرة {merchant}",
        "تذكرة {merchant}",
        "ركبت {merchant}",
        "دفعت أجرة {merchant}",
        "خدت {merchant}",
        "رحلة {merchant}"
    ],
    "Shopping & Retail": [
        "شراء من {merchant}",
        "تسوق من {merchant}",
        "اشتريت من {merchant}",
        "جبت حاجات من {merchant}",
        "شريت من {merchant}"
    ],
    "Entertainment & Recreation": [
        "تذكرة دخول {merchant}",
        "اشتراك في {merchant}",
        "روحت {merchant}",
        "دفعت في {merchant}",
        "زرت {merchant}"
    ],
    "Healthcare & Medical": [
        "كشف عند {merchant}",
        "شراء دواء من {merchant}",
        "كشفت عند {merchant}",
        "روحت {merchant}",
        "جبت دوا من {merchant}"
    ],
    "Utilities & Services": [
        "فاتورة {merchant}",
        "دفع فاتورة {merchant}",
        "دفعت فاتورة {merchant}",
        "سددت {merchant}"
    ],
    "Financial Services": [
        "رسوم {merchant}",
        "قسط {merchant}",
        "دفعت للبنك {merchant}",
        "سحبت من {merchant}"
    ],
    "Income": [
        "راتب من {merchant}",
        "مرتب {merchant}",
        "المرتب من {merchant}",
        "جالي فلوس من {merchant}"
    ],
    "Government & Legal": [
        "رسوم {merchant}",
        "دفع في {merchant}",
        "طلعت من {merchant}",
        "روحت {merchant}"
    ],
    "Charity & Donations": [
        "تبرع لـ {merchant}",
        "صدقة في {merchant}",
        "تبرعت لـ {merchant}",
        "دفعت صدقة في {merchant}"
    ]
}

TEMPLATES_PARTIAL_DIACRITICS = {
    "Food & Dining": [
        "شراء مواد غذائيّة من {merchant}",
        "دفع فاتورة {merchant}",
        "شراء وجبة من {merchant}",
        "اشتريتُ أكل من {merchant}",
        "دفعتُ فلوس {merchant}",
        "جبتُ أكل من {merchant}"
    ],
    "Transportation": [
        "دفع أجرة {merchant}",
        "تذكرة {merchant}",
        "ركبتُ {merchant}",
        "دفعتُ أجرة {merchant}",
        "خدتُ {merchant}",
        "رحلة {merchant}"
    ],
    "Shopping & Retail": [
        "شراء من {merchant}",
        "تسوّق من {merchant}",
        "اشتريتُ من {merchant}",
        "جبتُ حاجات من {merchant}",
        "شريتُ من {merchant}"
    ],
    "Entertainment & Recreation": [
        "تذكرة دخول {merchant}",
        "اشتراك في {merchant}",
        "روحتُ {merchant}",
        "دفعتُ في {merchant}",
        "زرتُ {merchant}"
    ],
    "Healthcare & Medical": [
        "كشف عند {merchant}",
        "شراء دواء من {merchant}",
        "كشفتُ عند {merchant}",
        "روحتُ {merchant}",
        "جبتُ دوا من {merchant}"
    ],
    "Utilities & Services": [
        "فاتورة {merchant}",
        "دفع فاتورة {merchant}",
        "دفعتُ فاتورة {merchant}",
        "سدّدتُ {merchant}"
    ],
    "Financial Services": [
        "رسوم {merchant}",
        "قسط {merchant}",
        "دفعتُ للبنك {merchant}",
        "سحبتُ من {merchant}"
    ],
    "Income": [
        "راتب من {merchant}",
        "مرتّب {merchant}",
        "المرتّب من {merchant}",
        "جالي فلوس من {merchant}"
    ],
    "Government & Legal": [
        "رسوم {merchant}",
        "دفع في {merchant}",
        "طلعتُ من {merchant}",
        "روحتُ {merchant}"
    ],
    "Charity & Donations": [
        "تبرّع لـ {merchant}",
        "صدقة في {merchant}",
        "تبرّعتُ لـ {merchant}",
        "دفعتُ صدقة في {merchant}"
    ]
}

TEMPLATES_FULL_DIACRITICS = {
    "Food & Dining": [
        "شِرَاءُ مَوَادَّ غِذَائِيَّةٍ مِنْ {merchant}",
        "دَفْعُ فَاتُورَةِ {merchant}",
        "شِرَاءُ وَجْبَةٍ مِنْ {merchant}",
        "اشْتَرَيْتُ أَكْلاً مِنْ {merchant}",
        "دَفَعْتُ فُلُوسَ {merchant}",
        "جِبْتُ أَكْلاً مِنْ {merchant}"
    ],
    "Transportation": [
        "دَفْعُ أُجْرَةِ {merchant}",
        "تَذْكِرَةُ {merchant}",
        "رَكِبْتُ {merchant}",
        "دَفَعْتُ أُجْرَةَ {merchant}",
        "أَخَذْتُ {merchant}",
        "رِحْلَةُ {merchant}"
    ],
    "Shopping & Retail": [
        "شِرَاءٌ مِنْ {merchant}",
        "تَسَوُّقٌ مِنْ {merchant}",
        "اشْتَرَيْتُ مِنْ {merchant}",
        "جِبْتُ حَاجَاتٍ مِنْ {merchant}",
        "اشْتَرَيْتُ مِنْ {merchant}"
    ],
    "Entertainment & Recreation": [
        "تَذْكِرَةُ دُخُولِ {merchant}",
        "اشْتِرَاكٌ فِي {merchant}",
        "رُحْتُ {merchant}",
        "دَفَعْتُ فِي {merchant}",
        "زُرْتُ {merchant}"
    ],
    "Healthcare & Medical": [
        "كَشْفٌ عِنْدَ {merchant}",
        "شِرَاءُ دَوَاءٍ مِنْ {merchant}",
        "كَشَفْتُ عِنْدَ {merchant}",
        "رُحْتُ {merchant}",
        "جِبْتُ دَوَاءً مِنْ {merchant}"
    ],
    "Utilities & Services": [
        "فَاتُورَةُ {merchant}",
        "دَفْعُ فَاتُورَةِ {merchant}",
        "دَفَعْتُ فَاتُورَةَ {merchant}",
        "سَدَّدْتُ {merchant}"
    ],
    "Financial Services": [
        "رُسُومُ {merchant}",
        "قِسْطُ {merchant}",
        "دَفَعْتُ لِلْبَنْكِ {merchant}",
        "سَحَبْتُ مِنْ {merchant}"
    ],
    "Income": [
        "رَاتِبٌ مِنْ {merchant}",
        "مُرَتَّبُ {merchant}",
        "الْمُرَتَّبُ مِنْ {merchant}",
        "جَالِي فُلُوسٌ مِنْ {merchant}"
    ],
    "Government & Legal": [
        "رُسُومُ {merchant}",
        "دَفْعٌ فِي {merchant}",
        "طَلَّعْتُ مِنْ {merchant}",
        "رُحْتُ {merchant}"
    ],
    "Charity & Donations": [
        "تَبَرُّعٌ لِـ {merchant}",
        "صَدَقَةٌ فِي {merchant}",
        "تَبَرَّعْتُ لِـ {merchant}",
        "دَفَعْتُ صَدَقَةً فِي {merchant}"
    ]
}

def generate_description(category, diacritic_type='none'):
    """Generate Arabic transaction description with diacritics"""
    
    # Choose template set based on diacritic type
    if diacritic_type == 'full':
        templates = TEMPLATES_FULL_DIACRITICS
    elif diacritic_type == 'partial':
        templates = TEMPLATES_PARTIAL_DIACRITICS
    else:
        templates = TEMPLATES_NO_DIACRITICS
    
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

def generate_balanced_dataset(base_records=1000):
    """Generate realistic dataset with varied distribution across categories"""
    
    # Realistic distribution (not perfectly balanced)
    # Some categories are more common than others
    category_multipliers = {
        "Food & Dining": 1.3,              # Most common
        "Transportation": 1.2,             # Very common
        "Shopping & Retail": 1.1,          # Common
        "Utilities & Services": 1.0,       # Baseline
        "Entertainment & Recreation": 0.9, # Slightly less
        "Healthcare & Medical": 0.8,       # Less frequent
        "Financial Services": 0.7,         # Less frequent
        "Government & Legal": 0.6,         # Infrequent
        "Charity & Donations": 0.5,        # Least common
        "Income": 0.4                      # Least common (monthly)
    }
    
    total_records = sum(int(base_records * mult) for mult in category_multipliers.values())
    
    print("="*70)
    print("REALISTIC ARABIC DATASET WITH DIACRITICS (TASHKEEL)")
    print("="*70)
    print(f"Base records: {base_records}")
    print(f"Total categories: {len(CATEGORIES)}")
    print(f"Total records: {total_records:,}")
    print(f"Distribution: Realistic (varied by category frequency)")
    print(f"Diacritics: 30% none, 40% partial, 30% full")
    print()
    
    records = []
    
    # Diacritic type distribution
    diacritic_types = ['none', 'partial', 'full']
    diacritic_weights = [0.30, 0.40, 0.30]
    
    for category in CATEGORIES:
        # Calculate records for this category
        category_records = int(base_records * category_multipliers[category])
        print(f"Generating {category_records:4d} records for: {category:30s} ({category_multipliers[category]:.1f}x)")
        
        for i in range(category_records):
            # Select diacritic type
            diacritic_type = random.choices(diacritic_types, weights=diacritic_weights)[0]
            
            # Generate description
            description = generate_description(category, diacritic_type)
            
            # Create record
            records.append({
                'transaction_description': description,
                'category': category,
                'country': COUNTRY,
                'currency': CURRENCY,
                'diacritic_type': diacritic_type
            })
    
    df = pd.DataFrame(records)
    
    # Shuffle dataset
    df = df.sample(frac=1, random_state=RANDOM_SEED).reset_index(drop=True)
    
    print(f"\n Generated {len(df):,} total records")
    
    return df

def main():
    """Main execution"""
    
    # Create directories
    os.makedirs('data/raw', exist_ok=True)
    os.makedirs('reports', exist_ok=True)
    
    # Generate dataset with realistic distribution
    df = generate_balanced_dataset(base_records=1000)
    
    # Save main file
    output_path = 'data/raw/arabic_balanced_diacritics.csv'
    df.to_csv(output_path, index=False, encoding='utf-8')
    print(f"\nSaved: {output_path}")
    
    # Also save without diacritic_type column for training
    df_train = df[['transaction_description', 'category', 'country', 'currency']].copy()
    df_train.to_csv('data/raw/arabic_balanced_diacritics_clean.csv', index=False, encoding='utf-8')
    print(f"Saved: data/raw/arabic_balanced_diacritics_clean.csv")
    
    print("\nNOTE: Train/Validation/Test split will be done AFTER preprocessing in the notebook.")
    
    # Generate report
    print("\nGenerating quality report...")
    
    report = []
    report.append("="*60)
    report.append("REALISTIC ARABIC DATASET WITH DIACRITICS - QUALITY REPORT")
    report.append("="*60)
    report.append("")
    report.append("Overall Statistics:")
    report.append("-"*60)
    report.append(f"Total Records                 : {len(df):,}")
    report.append(f"Unique Descriptions           : {df['transaction_description'].nunique():,}")
    report.append(f"Duplicate Rate (%)            : {(1 - df['transaction_description'].nunique()/len(df))*100:.2f}")
    report.append(f"Missing Values                : {df.isnull().sum().sum()}")
    report.append(f"Categories                    : {df['category'].nunique()}")
    report.append(f"Avg Description Length        : {df['transaction_description'].str.len().mean():.2f}")
    report.append(f"Min Description Length        : {df['transaction_description'].str.len().min()}")
    report.append(f"Max Description Length        : {df['transaction_description'].str.len().max()}")
    report.append("")
    report.append("")
    report.append("Category Distribution (REALISTIC - Varied by Frequency):")
    report.append("-"*60)
    for cat, count in df['category'].value_counts().sort_index().items():
        pct = (count / len(df)) * 100
        report.append(f"{cat:30s} : {count:5,} ({pct:5.1f}%)")
    report.append("")
    report.append("")
    report.append("Diacritic Type Distribution:")
    report.append("-"*60)
    for dtype, count in df['diacritic_type'].value_counts().items():
        pct = (count / len(df)) * 100
        report.append(f"{dtype:30s} : {count:5,} ({pct:5.1f}%)")
    report.append("")
    
    report_text = '\n'.join(report)
    
    with open('reports/arabic_balanced_diacritics_report.txt', 'w', encoding='utf-8') as f:
        f.write(report_text)
    
    print(report_text)
    
    # Show samples
    print("\nSample transactions (showing different diacritic levels):")
    print("-"*60)
    for cat in random.sample(list(df['category'].unique()), 3):
        print(f"\n{cat}:")
        samples = df[df['category'] == cat].head(3)
        for _, row in samples.iterrows():
            print(f"  [{row['diacritic_type']:7s}] {row['transaction_description']}")
    
    print("\n" + "="*70)
    print("REALISTIC ARABIC DATASET GENERATION COMPLETE!")
    print("="*70)
    print("Files created:")
    print("  - data/raw/arabic_balanced_diacritics.csv (with metadata)")
    print("  - data/raw/arabic_balanced_diacritics_clean.csv (for training)")
    print("  - reports/arabic_balanced_diacritics_report.txt")
    print()
    print("Distribution: Realistic (not perfectly balanced)")
    print("Most common: Food & Dining, Transportation")
    print("Least common: Income, Charity & Donations")
    print()
    print("NOTE: Train/validation/test split should be done AFTER preprocessing")
    print("      in the notebook to avoid data leakage.")
    print()

if __name__ == "__main__":
    main()
