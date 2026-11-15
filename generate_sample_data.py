"""
Generate Sample Transaction Data for Smart Expense Classifier
This script creates synthetic transaction data for training and testing.
"""

import pandas as pd
import random
from datetime import datetime, timedelta

# Sample data for each category
TRANSACTION_DATA = {
    'Food & Dining': {
        'merchants': [
            'Starbucks', 'McDonald\'s', 'Subway', 'Chipotle', 'Panera Bread',
            'Whole Foods', 'Trader Joe\'s', 'Safeway', 'Kroger', 'Walmart Grocery',
            'Pizza Hut', 'Dominos', 'Taco Bell', 'KFC', 'Burger King',
            'Olive Garden', 'Red Lobster', 'Cheesecake Factory', 'Applebee\'s',
            'Local Restaurant', 'Coffee Shop', 'Bakery', 'Ice Cream Shop'
        ],
        'amount_range': (5, 150),
        'descriptions': [
            '{} Coffee', '{} Lunch', '{} Dinner', '{} Breakfast',
            '{} Groceries', '{} Food Purchase', '{} Meal', '{} Order'
        ]
    },
    'Transportation': {
        'merchants': [
            'Uber', 'Lyft', 'Shell', 'Chevron', 'Exxon', 'BP',
            'Metro Card', 'City Transit', 'Parking Garage', 'Toll Road',
            'Gas Station', 'Car Wash', 'Auto Service', 'Taxi Service'
        ],
        'amount_range': (10, 80),
        'descriptions': [
            '{} Ride', '{} Gas Purchase', '{} Fuel', '{} Parking',
            '{} Transit Pass', '{} Toll', '{} Transportation'
        ]
    },
    'Shopping': {
        'merchants': [
            'Amazon', 'Target', 'Walmart', 'Best Buy', 'Macy\'s',
            'Nordstrom', 'H&M', 'Zara', 'Nike', 'Adidas',
            'Apple Store', 'Home Depot', 'Lowe\'s', 'IKEA',
            'Costco', 'eBay', 'Etsy', 'Online Shop'
        ],
        'amount_range': (20, 300),
        'descriptions': [
            '{} Purchase', '{} Order', '{} Shopping',
            '{} Online Purchase', '{} Store Purchase', '{} Item'
        ]
    },
    'Utilities': {
        'merchants': [
            'ComEd Electric', 'Water Company', 'Gas Utility',
            'AT&T', 'Verizon', 'T-Mobile', 'Sprint', 'Comcast',
            'Internet Provider', 'Electric Bill', 'Water Bill',
            'Phone Bill', 'Internet Bill'
        ],
        'amount_range': (50, 250),
        'descriptions': [
            '{} Bill Payment', '{} Monthly Bill', '{} Utility Payment',
            '{} Service', '{} Subscription'
        ]
    },
    'Entertainment': {
        'merchants': [
            'Netflix', 'Hulu', 'Disney+', 'Spotify', 'Apple Music',
            'YouTube Premium', 'HBO Max', 'Amazon Prime',
            'Movie Theater', 'Concert Hall', 'Sports Stadium',
            'Game Store', 'PlayStation Network', 'Xbox Live'
        ],
        'amount_range': (10, 150),
        'descriptions': [
            '{} Subscription', '{} Membership', '{} Ticket',
            '{} Purchase', '{} Service', '{} Entertainment'
        ]
    },
    'Healthcare': {
        'merchants': [
            'CVS Pharmacy', 'Walgreens', 'Rite Aid', 'Local Pharmacy',
            'Hospital', 'Medical Clinic', 'Dental Office',
            'Eye Doctor', 'Urgent Care', 'Lab Tests', 'Health Insurance'
        ],
        'amount_range': (15, 300),
        'descriptions': [
            '{} Prescription', '{} Medical Service', '{} Healthcare',
            '{} Copay', '{} Medicine', '{} Medical Bill'
        ]
    },
    'Rent/Housing': {
        'merchants': [
            'Property Management', 'Landlord', 'Mortgage Company',
            'HOA Payment', 'Rent Payment', 'Housing Authority',
            'Apartment Complex', 'Home Depot', 'Lowe\'s Hardware',
            'Furniture Store', 'IKEA'
        ],
        'amount_range': (50, 2000),
        'descriptions': [
            'Rent Payment', 'Mortgage Payment', '{} HOA Fee',
            '{} Home Maintenance', '{} Furniture', '{} Home Repair'
        ]
    },
    'Education': {
        'merchants': [
            'University Tuition', 'College Bookstore', 'Udemy',
            'Coursera', 'LinkedIn Learning', 'Khan Academy',
            'School Payment', 'Textbook Store', 'Online Course',
            'Educational Platform'
        ],
        'amount_range': (30, 500),
        'descriptions': [
            '{} Course Fee', '{} Textbook', '{} Tuition Payment',
            '{} Educational Material', '{} Training', '{} Class Fee'
        ]
    },
    'Others': {
        'merchants': [
            'Miscellaneous', 'Cash Withdrawal', 'ATM',
            'Bank Fee', 'Service Charge', 'Gift Shop',
            'Pet Store', 'Donation', 'Charity'
        ],
        'amount_range': (10, 100),
        'descriptions': [
            '{} Purchase', '{} Service', '{} Fee',
            '{} Payment', '{} Transaction'
        ]
    }
}


def generate_transactions(num_transactions=1500, start_date=None, end_date=None):
    """
    Generate synthetic transaction data
    
    Args:
        num_transactions (int): Number of transactions to generate
        start_date (datetime): Start date for transactions
        end_date (datetime): End date for transactions
    
    Returns:
        pandas.DataFrame: Generated transaction data
    """
    if start_date is None:
        start_date = datetime.now() - timedelta(days=365)
    if end_date is None:
        end_date = datetime.now()
    
    transactions = []
    
    for i in range(num_transactions):
        # Select random category
        category = random.choice(list(TRANSACTION_DATA.keys()))
        category_data = TRANSACTION_DATA[category]
        
        # Select random merchant
        merchant = random.choice(category_data['merchants'])
        
        # Generate amount within range
        min_amount, max_amount = category_data['amount_range']
        amount = round(random.uniform(min_amount, max_amount), 2)
        
        # Generate description
        desc_template = random.choice(category_data['descriptions'])
        if '{}' in desc_template:
            description = desc_template.format(merchant)
        else:
            description = desc_template
        
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
            'category': category
        }
        
        transactions.append(transaction)
    
    # Create DataFrame
    df = pd.DataFrame(transactions)
    
    # Sort by date
    df = df.sort_values('date').reset_index(drop=True)
    
    return df


def generate_and_save(output_file='data/sample_transactions.csv', num_transactions=1500):
    """
    Generate transactions and save to CSV
    
    Args:
        output_file (str): Output file path
        num_transactions (int): Number of transactions to generate
    """
    print(f"Generating {num_transactions} sample transactions...")
    
    df = generate_transactions(num_transactions)
    
    # Print statistics
    print(f"\n✅ Generated {len(df)} transactions")
    print(f"\nCategory Distribution:")
    print(df['category'].value_counts().sort_index())
    
    print(f"\nAmount Statistics:")
    print(df.groupby('category')['amount'].agg(['count', 'mean', 'min', 'max']))
    
    # Save to CSV
    df.to_csv(output_file, index=False)
    print(f"\n💾 Saved to: {output_file}")
    
    # Show sample
    print(f"\nSample transactions:")
    print(df.head(10).to_string())
    
    return df


if __name__ == "__main__":
    # Generate sample data
    df = generate_and_save(
        output_file='data/sample_transactions.csv',
        num_transactions=1500
    )
    
    print("\n✨ Sample data generation complete!")
    print("\nNext steps:")
    print("1. Review the generated data: data/sample_transactions.csv")
    print("2. Open Jupyter notebook for exploration")
    print("3. Start with notebooks/01_data_exploration.ipynb")
