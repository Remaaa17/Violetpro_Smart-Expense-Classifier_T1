"""
Generate Arabic Transaction Data for Smart Expense Classifier
Matches the structure of the Hugging Face dataset with Arabic translations
"""

import pandas as pd
import random
from datetime import datetime, timedelta

# Arabic transaction data for each category
ARABIC_TRANSACTION_DATA = {
    'Food & Dining': {
        'merchants_ar': [
            'مطعم', 'كافيه', 'مقهى', 'مخبز', 'سوبرماركت',
            'بقالة', 'مطعم شاورما', 'مطعم برجر', 'مطعم بيتزا',
            'كارفور', 'سبينس', 'جعيتا', 'مطعم صيدا'
        ],
        'merchants_en': [
            'Starbucks', 'McDonald\'s', 'Subway', 'Carrefour', 'Spinneys',
            'Local Restaurant', 'Pizza Hut', 'KFC', 'Burger King'
        ],
        'descriptions_ar': [
            'مطعم {}', 'شراء من {}', 'وجبة في {}', 'قهوة من {}',
            'طلب من {}', 'بقالة {}', 'عشاء في {}', 'فطور من {}'
        ],
        'amount_range': (10, 150)
    },
    'Transportation': {
        'merchants_ar': [
            'أوبر', 'كريم', 'تاكسي', 'محطة بنزين', 'شل', 'توتال',
            'موقف سيارات', 'طريق الأوتوستراد', 'مترو'
        ],
        'merchants_en': [
            'Uber', 'Careem', 'Taxi', 'Shell', 'Total', 'Parking'
        ],
        'descriptions_ar': [
            'رحلة {}', 'بنزين من {}', 'موقف {}', 'تاكسي {}',
            'وقود من {}', 'أجرة {}'
        ],
        'amount_range': (15, 100)
    },
    'Shopping': {
        'merchants_ar': [
            'أمازون', 'سيتي مول', 'محل ملابس', 'محل الكترونيات',
            'ABC مول', 'فيردون', 'محل أحذية', 'سوق'
        ],
        'merchants_en': [
            'Amazon', 'City Mall', 'ABC Mall', 'Online Shop', 'Store'
        ],
        'descriptions_ar': [
            'شراء من {}', 'طلب {}', 'تسوق من {}', 'شراء عبر الإنترنت من {}'
        ],
        'amount_range': (30, 300)
    },
    'Entertainment': {
        'merchants_ar': [
            'نتفليكس', 'سبوتيفاي', 'سينما', 'أوسكار سينما',
            'شاهد VIP', 'ألعاب', 'مسرح', 'حفلة موسيقية'
        ],
        'merchants_en': [
            'Netflix', 'Spotify', 'Cinema', 'Shahid', 'OSN'
        ],
        'descriptions_ar': [
            'اشتراك {}', 'تذكرة {}', 'خدمة {}', 'ترفيه {}'
        ],
        'amount_range': (10, 150)
    },
    'Healthcare': {
        'merchants_ar': [
            'صيدلية', 'مستشفى', 'عيادة', 'طبيب', 'صيدلية الحياة',
            'مختبر', 'أسنان', 'تأمين صحي'
        ],
        'merchants_en': [
            'Pharmacy', 'Hospital', 'Clinic', 'Doctor', 'Lab'
        ],
        'descriptions_ar': [
            'دواء من {}', 'زيارة {}', 'فحص {}', 'علاج في {}'
        ],
        'amount_range': (20, 300)
    },
    'Utilities': {
        'merchants_ar': [
            'كهرباء لبنان', 'أوجيرو', 'ألفا', 'تاتش', 'مياه',
            'فاتورة كهرباء', 'فاتورة ماء', 'فاتورة إنترنت', 'فاتورة هاتف'
        ],
        'merchants_en': [
            'EDL', 'Ogero', 'Alfa', 'Touch', 'Water Bill', 'Internet'
        ],
        'descriptions_ar': [
            'فاتورة {}', 'دفع {}', 'خدمة {}', 'اشتراك {}'
        ],
        'amount_range': (50, 250)
    },
    'Rent/Housing': {
        'merchants_ar': [
            'إيجار شقة', 'صيانة منزل', 'أثاث', 'مفروشات',
            'إدارة عقارية', 'إيجار', 'صاحب العقار'
        ],
        'merchants_en': [
            'Rent Payment', 'Property Management', 'Furniture Store'
        ],
        'descriptions_ar': [
            'إيجار {}', 'صيانة {}', 'شراء {} للمنزل', 'دفع {}'
        ],
        'amount_range': (100, 2000)
    },
    'Education': {
        'merchants_ar': [
            'جامعة', 'مدرسة', 'معهد', 'دورة تعليمية', 'كتب',
            'يوديمي', 'كورسيرا', 'رسوم دراسية', 'مكتبة'
        ],
        'merchants_en': [
            'University', 'School', 'Udemy', 'Coursera', 'Bookstore'
        ],
        'descriptions_ar': [
            'رسوم {}', 'دورة {}', 'كتاب من {}', 'تعليم {}'
        ],
        'amount_range': (50, 500)
    },
    'Others': {
        'merchants_ar': [
            'متفرقات', 'هدية', 'تبرع', 'رسوم بنك', 'خدمات متنوعة'
        ],
        'merchants_en': [
            'Miscellaneous', 'Gift', 'Bank Fee', 'Various Services'
        ],
        'descriptions_ar': [
            'مصاريف {}', 'دفع {}', 'خدمة {}', 'شراء {}'
        ],
        'amount_range': (10, 150)
    }
}


def generate_arabic_transactions(num_transactions=2000, bilingual=True):
    """
    Generate Arabic transaction data
    
    Args:
        num_transactions (int): Number of transactions to generate
        bilingual (bool): Include both Arabic and English descriptions
    
    Returns:
        pandas.DataFrame: Generated transaction data
    """
    transactions = []
    
    # Date range: last year
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    for i in range(num_transactions):
        # Select random category
        category = random.choice(list(ARABIC_TRANSACTION_DATA.keys()))
        category_data = ARABIC_TRANSACTION_DATA[category]
        
        # Select merchant (50% Arabic, 50% English if bilingual)
        if bilingual and random.random() > 0.5:
            merchant = random.choice(category_data['merchants_en'])
            is_arabic = False
        else:
            merchant = random.choice(category_data['merchants_ar'])
            is_arabic = True
        
        # Generate description
        desc_template = random.choice(category_data['descriptions_ar'])
        description = desc_template.format(merchant)
        
        # Generate amount
        min_amount, max_amount = category_data['amount_range']
        amount = round(random.uniform(min_amount, max_amount), 2)
        
        # Generate random date
        time_delta = end_date - start_date
        random_days = random.randint(0, time_delta.days)
        transaction_date = start_date + timedelta(days=random_days)
        
        # Create transaction
        transaction = {
            'transaction_id': f'TXN{i+1:05d}',
            'date': transaction_date.strftime('%Y-%m-%d'),
            'description': description,
            'amount': amount,
            'merchant': merchant,
            'category': category,
            'language': 'ar' if is_arabic else 'en',
            'currency': 'LBP'  # Lebanese Pound
        }
        
        transactions.append(transaction)
    
    # Create DataFrame
    df = pd.DataFrame(transactions)
    
    # Sort by date
    df = df.sort_values('date').reset_index(drop=True)
    
    return df


def generate_and_save(output_file='data/arabic_transactions.csv', num_transactions=2000):
    """
    Generate Arabic transactions and save to CSV
    
    Args:
        output_file (str): Output file path
        num_transactions (int): Number of transactions to generate
    """
    print("="*70)
    print("🇱🇧 GENERATING ARABIC TRANSACTION DATA")
    print("="*70)
    print(f"\n📊 Generating {num_transactions} Arabic transactions...")
    
    df = generate_arabic_transactions(num_transactions, bilingual=True)
    
    # Statistics
    print(f"\n✅ Generated {len(df)} transactions")
    
    print(f"\n🏷️ Category Distribution:")
    category_counts = df['category'].value_counts()
    for cat, count in category_counts.items():
        percentage = (count / len(df)) * 100
        print(f"   {cat:.<45} {count:>5} ({percentage:>5.1f}%)")
    
    print(f"\n🌐 Language Distribution:")
    lang_counts = df['language'].value_counts()
    for lang, count in lang_counts.items():
        percentage = (count / len(df)) * 100
        lang_name = 'Arabic' if lang == 'ar' else 'English'
        print(f"   {lang_name:.<45} {count:>5} ({percentage:>5.1f}%)")
    
    print(f"\n💰 Amount Statistics:")
    amount_stats = df.groupby('category')['amount'].agg(['count', 'mean', 'min', 'max'])
    print(amount_stats.to_string())
    
    # Sample transactions
    print(f"\n📝 Sample Transactions:")
    print(f"\nArabic Examples:")
    arabic_samples = df[df['language'] == 'ar'].sample(min(5, len(df[df['language'] == 'ar'])))
    for _, row in arabic_samples.iterrows():
        print(f"\n   [{row['transaction_id']}] {row['description']}")
        print(f"   Category: {row['category']} | Amount: {row['amount']} {row['currency']}")
    
    print(f"\n\nEnglish/Mixed Examples:")
    english_samples = df[df['language'] == 'en'].sample(min(5, len(df[df['language'] == 'en'])))
    for _, row in english_samples.iterrows():
        print(f"\n   [{row['transaction_id']}] {row['description']}")
        print(f"   Category: {row['category']} | Amount: {row['amount']} {row['currency']}")
    
    # Save to CSV
    df.to_csv(output_file, index=False, encoding='utf-8-sig')  # UTF-8 with BOM for Excel compatibility
    print(f"\n💾 Saved to: {output_file}")
    print(f"   Encoding: UTF-8 with BOM (Excel compatible)")
    
    # Also save English-only version
    english_file = output_file.replace('.csv', '_english.csv')
    df_english = df[df['language'] == 'en']
    df_english.to_csv(english_file, index=False)
    print(f"   English-only: {english_file} ({len(df_english)} records)")
    
    # Combined with original English data
    print(f"\n📦 Creating combined dataset (English + Arabic)...")
    try:
        # Load English data if exists
        english_df = pd.read_csv('data/sample_transactions.csv')
        combined_df = pd.concat([english_df, df], ignore_index=True)
        combined_file = 'data/combined_transactions.csv'
        combined_df.to_csv(combined_file, index=False, encoding='utf-8-sig')
        print(f"   ✅ Combined: {combined_file} ({len(combined_df)} records)")
    except:
        print(f"   ⚠️  Original English data not found, skipping combined dataset")
    
    print("\n" + "="*70)
    print("✅ ARABIC DATA GENERATION COMPLETE!")
    print("="*70)
    
    print(f"\n📁 Files Created:")
    print(f"   ✅ {output_file} (All transactions)")
    print(f"   ✅ {english_file} (English only)")
    
    print(f"\n🎯 Next Steps:")
    print(f"   1. Review: {output_file}")
    print(f"   2. Test model with Arabic data")
    print(f"   3. Update preprocessing for Arabic text")
    print(f"   4. Train bilingual model")
    
    return df


if __name__ == "__main__":
    # Generate Arabic transaction data
    df = generate_and_save(
        output_file='data/arabic_transactions.csv',
        num_transactions=2000
    )
    
    print("\n✨ Ready to train bilingual expense classifier! 🇱🇧🇬🇧")
