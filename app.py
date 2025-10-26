from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from pymongo import MongoClient, DESCENDING
from bson.objectid import ObjectId
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
from collections import defaultdict

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key')

# MongoDB Configuration
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'expense_tracker_db')

# Initialize MongoDB connection
try:
    client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
    client.server_info()  # Test connection
    db = client[DATABASE_NAME]
    transactions_collection = db.transactions
    budgets_collection = db.budgets
    print("✓ MongoDB connected successfully!")
except Exception as e:
    print(f"✗ MongoDB connection failed: {e}")
    print("Please ensure MongoDB is running or check your connection string in .env file")

# Categories
CATEGORIES = ['Food', 'Transport', 'Entertainment', 'Healthcare', 'Utilities', 'Shopping', 'Salary', 'Other']

# Helper Functions
def get_date_filter(filter_type='all'):
    """Generate date filter for queries"""
    if filter_type == 'today':
        start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        return {'date': {'$gte': start}}
    elif filter_type == 'week':
        start = datetime.now() - timedelta(days=7)
        return {'date': {'$gte': start}}
    elif filter_type == 'month':
        start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        return {'date': {'$gte': start}}
    elif filter_type == 'year':
        start = datetime.now().replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        return {'date': {'$gte': start}}
    return {}

def calculate_statistics(filter_type='all'):
    """Calculate income, expenses, and balance"""
    date_filter = get_date_filter(filter_type)
    
    income_pipeline = [
        {'$match': {**date_filter, 'type': 'income'}},
        {'$group': {'_id': None, 'total': {'$sum': '$amount'}}}
    ]
    expense_pipeline = [
        {'$match': {**date_filter, 'type': 'expense'}},
        {'$group': {'_id': None, 'total': {'$sum': '$amount'}}}
    ]
    
    income_result = list(transactions_collection.aggregate(income_pipeline))
    expense_result = list(transactions_collection.aggregate(expense_pipeline))
    
    total_income = income_result[0]['total'] if income_result else 0
    total_expenses = expense_result[0]['total'] if expense_result else 0
    balance = total_income - total_expenses
    
    return {
        'income': total_income,
        'expenses': total_expenses,
        'balance': balance
    }

def get_category_breakdown(filter_type='month'):
    """Get expense breakdown by category"""
    date_filter = get_date_filter(filter_type)
    
    pipeline = [
        {'$match': {**date_filter, 'type': 'expense'}},
        {'$group': {
            '_id': '$category',
            'total': {'$sum': '$amount'}
        }},
        {'$sort': {'total': -1}}
    ]
    
    results = list(transactions_collection.aggregate(pipeline))
    return {item['_id']: item['total'] for item in results}

# Routes
@app.route('/')
def index():
    """Dashboard page with summary statistics"""
    stats = calculate_statistics('all')
    month_stats = calculate_statistics('month')
    
    # Get recent transactions
    recent_transactions = list(transactions_collection.find().sort('date', DESCENDING).limit(5))
    
    # Get category breakdown for charts
    category_data = get_category_breakdown('month')
    
    # Get budget alerts
    current_month = datetime.now().month
    current_year = datetime.now().year
    budgets = list(budgets_collection.find({'month': current_month, 'year': current_year}))
    
    budget_alerts = []
    for budget in budgets:
        category = budget['category']
        budget_amount = budget['amount']
        spent = category_data.get(category, 0)
        percentage = (spent / budget_amount * 100) if budget_amount > 0 else 0
        
        if percentage >= 100:
            budget_alerts.append({
                'category': category,
                'budget': budget_amount,
                'spent': spent,
                'percentage': percentage,
                'status': 'exceeded'
            })
        elif percentage >= 80:
            budget_alerts.append({
                'category': category,
                'budget': budget_amount,
                'spent': spent,
                'percentage': percentage,
                'status': 'warning'
            })
    
    return render_template('index.html', 
                         stats=stats,
                         month_stats=month_stats,
                         recent_transactions=recent_transactions,
                         category_data=category_data,
                         budget_alerts=budget_alerts)

@app.route('/add', methods=['GET', 'POST'])
def add_transaction():
    """Add new income or expense"""
    if request.method == 'POST':
        try:
            transaction = {
                'type': request.form.get('type'),
                'amount': float(request.form.get('amount')),
                'category': request.form.get('category'),
                'description': request.form.get('description', ''),
                'date': datetime.strptime(request.form.get('date'), '%Y-%m-%d'),
                'created_at': datetime.now()
            }
            
            transactions_collection.insert_one(transaction)
            flash(f'{transaction["type"].capitalize()} added successfully!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Error adding transaction: {str(e)}', 'error')
    
    return render_template('add_transaction.html', categories=CATEGORIES)

@app.route('/transactions')
def view_transactions():
    """View all transactions with filtering"""
    filter_type = request.args.get('filter', 'all')
    category_filter = request.args.get('category', 'all')
    type_filter = request.args.get('type', 'all')
    
    # Build query
    query = get_date_filter(filter_type)
    
    if category_filter != 'all':
        query['category'] = category_filter
    
    if type_filter != 'all':
        query['type'] = type_filter
    
    # Get transactions
    transactions = list(transactions_collection.find(query).sort('date', DESCENDING))
    
    # Calculate totals
    total_income = sum(t['amount'] for t in transactions if t['type'] == 'income')
    total_expenses = sum(t['amount'] for t in transactions if t['type'] == 'expense')
    
    return render_template('view_transactions.html',
                         transactions=transactions,
                         categories=CATEGORIES,
                         current_filter=filter_type,
                         current_category=category_filter,
                         current_type=type_filter,
                         total_income=total_income,
                         total_expenses=total_expenses)

@app.route('/delete/<transaction_id>')
def delete_transaction(transaction_id):
    """Delete a transaction"""
    try:
        transactions_collection.delete_one({'_id': ObjectId(transaction_id)})
        flash('Transaction deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting transaction: {str(e)}', 'error')
    
    return redirect(url_for('view_transactions'))

@app.route('/budget', methods=['GET', 'POST'])
def budget():
    """Set and view budgets by category"""
    current_month = datetime.now().month
    current_year = datetime.now().year
    current_month_name = datetime.now().strftime('%B %Y')
    
    if request.method == 'POST':
        try:
            category = request.form.get('category')
            amount = float(request.form.get('amount'))
            
            # Update or insert budget
            budgets_collection.update_one(
                {
                    'category': category,
                    'month': current_month,
                    'year': current_year
                },
                {
                    '$set': {
                        'category': category,
                        'amount': amount,
                        'month': current_month,
                        'year': current_year,
                        'updated_at': datetime.now()
                    }
                },
                upsert=True
            )
            flash(f'Budget for {category} set successfully!', 'success')
            return redirect(url_for('budget'))
        except Exception as e:
            flash(f'Error setting budget: {str(e)}', 'error')
    
    # Get current budgets
    budgets = list(budgets_collection.find({'month': current_month, 'year': current_year}))
    
    # Get actual spending
    category_spending = get_category_breakdown('month')
    
    # Combine budget and actual data
    budget_data = []
    for category in CATEGORIES:
        if category != 'Salary':  # Exclude Salary from budgets
            budget_item = next((b for b in budgets if b['category'] == category), None)
            budget_amount = budget_item['amount'] if budget_item else 0
            spent = category_spending.get(category, 0)
            percentage = (spent / budget_amount * 100) if budget_amount > 0 else 0
            
            status = 'safe'
            if percentage >= 100:
                status = 'exceeded'
            elif percentage >= 80:
                status = 'warning'
            
            budget_data.append({
                'category': category,
                'budget': budget_amount,
                'spent': spent,
                'remaining': budget_amount - spent,
                'percentage': min(percentage, 100),
                'status': status
            })
    
    return render_template('budget.html', 
                         budget_data=budget_data,
                         categories=[c for c in CATEGORIES if c != 'Salary'],
                         current_month_name=current_month_name)

@app.route('/reports')
def reports():
    """Monthly and yearly reports with charts"""
    # Get monthly data for the past 6 months
    monthly_data = []
    for i in range(6):
        date = datetime.now() - timedelta(days=30*i)
        month_start = date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        if i > 0:
            next_month = month_start + timedelta(days=32)
            month_end = next_month.replace(day=1)
        else:
            month_end = datetime.now()
        
        income = list(transactions_collection.aggregate([
            {'$match': {'type': 'income', 'date': {'$gte': month_start, '$lt': month_end}}},
            {'$group': {'_id': None, 'total': {'$sum': '$amount'}}}
        ]))
        
        expenses = list(transactions_collection.aggregate([
            {'$match': {'type': 'expense', 'date': {'$gte': month_start, '$lt': month_end}}},
            {'$group': {'_id': None, 'total': {'$sum': '$amount'}}}
        ]))
        
        monthly_data.append({
            'month': month_start.strftime('%B %Y'),
            'income': income[0]['total'] if income else 0,
            'expenses': expenses[0]['total'] if expenses else 0
        })
    
    monthly_data.reverse()
    
    # Get current month statistics
    month_stats = calculate_statistics('month')
    year_stats = calculate_statistics('year')
    
    # Category breakdown
    category_data = get_category_breakdown('month')
    
    return render_template('reports.html',
                         monthly_data=monthly_data,
                         month_stats=month_stats,
                         year_stats=year_stats,
                         category_data=category_data)

@app.route('/api/chart-data')
def chart_data():
    """API endpoint for chart data"""
    chart_type = request.args.get('type', 'category')
    
    if chart_type == 'category':
        data = get_category_breakdown('month')
        return jsonify(data)
    
    elif chart_type == 'monthly':
        monthly_data = []
        for i in range(6):
            date = datetime.now() - timedelta(days=30*i)
            month_start = date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            
            if i > 0:
                next_month = month_start + timedelta(days=32)
                month_end = next_month.replace(day=1)
            else:
                month_end = datetime.now()
            
            income = list(transactions_collection.aggregate([
                {'$match': {'type': 'income', 'date': {'$gte': month_start, '$lt': month_end}}},
                {'$group': {'_id': None, 'total': {'$sum': '$amount'}}}
            ]))
            
            expenses = list(transactions_collection.aggregate([
                {'$match': {'type': 'expense', 'date': {'$gte': month_start, '$lt': month_end}}},
                {'$group': {'_id': None, 'total': {'$sum': '$amount'}}}
            ]))
            
            monthly_data.append({
                'month': month_start.strftime('%b %Y'),
                'income': income[0]['total'] if income else 0,
                'expenses': expenses[0]['total'] if expenses else 0
            })
        
        monthly_data.reverse()
        return jsonify(monthly_data)
    
    return jsonify({})

# Template filters
@app.template_filter('currency')
def currency_filter(value):
    """Format number as currency"""
    return f"${value:,.2f}"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
