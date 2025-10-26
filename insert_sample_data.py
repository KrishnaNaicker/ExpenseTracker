"""
Sample Data Insertion Script
Adds realistic sample transactions to the database for demo purposes
"""

from pymongo import MongoClient
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import random

# Load environment variables
load_dotenv()

MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'expense_tracker_db')

# Connect to MongoDB
try:
    client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
    client.server_info()
    db = client[DATABASE_NAME]
    transactions_collection = db.transactions
    budgets_collection = db.budgets
    print("✓ Connected to MongoDB successfully!")
except Exception as e:
    print(f"✗ MongoDB connection failed: {e}")
    exit(1)

# Sample transactions data
sample_transactions = [
    # Income transactions
    {'type': 'income', 'amount': 5000.00, 'category': 'Salary', 'description': 'Monthly salary', 'days_ago': 30},
    {'type': 'income', 'amount': 5000.00, 'category': 'Salary', 'description': 'Monthly salary', 'days_ago': 60},
    {'type': 'income', 'amount': 500.00, 'category': 'Other', 'description': 'Freelance project payment', 'days_ago': 15},
    {'type': 'income', 'amount': 5000.00, 'category': 'Salary', 'description': 'Monthly salary', 'days_ago': 1},
    
    # Expense transactions - Current month
    {'type': 'expense', 'amount': 850.00, 'category': 'Food', 'description': 'Grocery shopping at Walmart', 'days_ago': 2},
    {'type': 'expense', 'amount': 45.50, 'category': 'Food', 'description': 'Lunch at restaurant', 'days_ago': 3},
    {'type': 'expense', 'amount': 120.00, 'category': 'Transport', 'description': 'Gas station fill-up', 'days_ago': 4},
    {'type': 'expense', 'amount': 89.99, 'category': 'Entertainment', 'description': 'Netflix and Spotify subscriptions', 'days_ago': 5},
    {'type': 'expense', 'amount': 250.00, 'category': 'Healthcare', 'description': 'Doctor visit copay', 'days_ago': 7},
    {'type': 'expense', 'amount': 180.00, 'category': 'Utilities', 'description': 'Electricity bill', 'days_ago': 8},
    {'type': 'expense', 'amount': 65.00, 'category': 'Utilities', 'description': 'Internet bill', 'days_ago': 9},
    {'type': 'expense', 'amount': 320.00, 'category': 'Shopping', 'description': 'New shoes and clothes', 'days_ago': 10},
    {'type': 'expense', 'amount': 55.00, 'category': 'Transport', 'description': 'Uber rides', 'days_ago': 12},
    {'type': 'expense', 'amount': 95.00, 'category': 'Food', 'description': 'Dinner with friends', 'days_ago': 14},
    
    # Previous month expenses
    {'type': 'expense', 'amount': 900.00, 'category': 'Food', 'description': 'Monthly groceries', 'days_ago': 35},
    {'type': 'expense', 'amount': 150.00, 'category': 'Transport', 'description': 'Gas and car maintenance', 'days_ago': 37},
    {'type': 'expense', 'amount': 200.00, 'category': 'Entertainment', 'description': 'Concert tickets', 'days_ago': 40},
    {'type': 'expense', 'amount': 175.00, 'category': 'Utilities', 'description': 'Electric and water bills', 'days_ago': 42},
    {'type': 'expense', 'amount': 450.00, 'category': 'Shopping', 'description': 'Electronics purchase', 'days_ago': 45},
    {'type': 'expense', 'amount': 80.00, 'category': 'Food', 'description': 'Restaurant meals', 'days_ago': 50},
]

# Sample budgets for current month
current_month = datetime.now().month
current_year = datetime.now().year

sample_budgets = [
    {'category': 'Food', 'amount': 800.00, 'month': current_month, 'year': current_year},
    {'category': 'Transport', 'amount': 300.00, 'month': current_month, 'year': current_year},
    {'category': 'Entertainment', 'amount': 150.00, 'month': current_month, 'year': current_year},
    {'category': 'Healthcare', 'amount': 400.00, 'month': current_month, 'year': current_year},
    {'category': 'Utilities', 'amount': 350.00, 'month': current_month, 'year': current_year},
    {'category': 'Shopping', 'amount': 500.00, 'month': current_month, 'year': current_year},
]

def insert_sample_data():
    """Insert sample transactions and budgets into the database"""
    
    # Clear existing data (optional - comment out if you want to keep existing data)
    print("\n⚠ Clearing existing data...")
    transactions_collection.delete_many({})
    budgets_collection.delete_many({})
    
    # Insert sample transactions
    print("\n📝 Inserting sample transactions...")
    inserted_transactions = []
    
    for transaction in sample_transactions:
        transaction_date = datetime.now() - timedelta(days=transaction['days_ago'])
        
        doc = {
            'type': transaction['type'],
            'amount': transaction['amount'],
            'category': transaction['category'],
            'description': transaction['description'],
            'date': transaction_date,
            'created_at': datetime.now()
        }
        
        result = transactions_collection.insert_one(doc)
        inserted_transactions.append(result.inserted_id)
        print(f"  ✓ Added {transaction['type']}: ${transaction['amount']} - {transaction['category']}")
    
    print(f"\n✓ Successfully inserted {len(inserted_transactions)} transactions!")
    
    # Insert sample budgets
    print("\n💰 Inserting sample budgets...")
    inserted_budgets = []
    
    for budget in sample_budgets:
        budget['updated_at'] = datetime.now()
        result = budgets_collection.insert_one(budget)
        inserted_budgets.append(result.inserted_id)
        print(f"  ✓ Set budget for {budget['category']}: ${budget['amount']}")
    
    print(f"\n✓ Successfully inserted {len(inserted_budgets)} budgets!")
    
    # Calculate and display summary
    print("\n" + "="*50)
    print("📊 DATA SUMMARY")
    print("="*50)
    
    total_income = sum(t['amount'] for t in sample_transactions if t['type'] == 'income')
    total_expenses = sum(t['amount'] for t in sample_transactions if t['type'] == 'expense')
    balance = total_income - total_expenses
    
    print(f"Total Income:    ${total_income:,.2f}")
    print(f"Total Expenses:  ${total_expenses:,.2f}")
    print(f"Balance:         ${balance:,.2f}")
    print(f"\nBudgets Set:     {len(inserted_budgets)} categories")
    print("="*50)
    
    print("\n✅ Sample data insertion completed successfully!")
    print("🚀 You can now run the Flask app and see the data in action!")

if __name__ == '__main__':
    try:
        insert_sample_data()
    except Exception as e:
        print(f"\n❌ Error inserting sample data: {e}")
    finally:
        client.close()
