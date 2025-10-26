# 💰 Personal Expense Tracker

A modern, full-stack web application for tracking personal income and expenses with budget management and visual analytics.

## 🌟 Features

- **Dashboard**: Overview with total income, expenses, balance, and recent transactions
- **Transaction Management**: Add, view, filter, and delete income/expense transactions
- **Budget Tracking**: Set monthly budgets by category with visual alerts
- **Reports & Analytics**: Interactive charts showing spending patterns and trends
- **Category Breakdown**: Visualize expenses by category with pie and bar charts
- **Responsive Design**: Modern dark theme that works on desktop and mobile
- **Real-time Filtering**: Filter transactions by date, type, and category

## 🛠️ Tech Stack

- **Backend**: Python Flask 3.0
- **Database**: MongoDB (Local or Atlas)
- **Frontend**: HTML5, CSS3, JavaScript
- **Charts**: Chart.js
- **Styling**: Custom CSS with dark theme
- **Icons**: Font Awesome 6

## 📋 Prerequisites

Before running this application, ensure you have the following installed:

1. **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
2. **MongoDB** - Choose one option:
   - **Option A**: [MongoDB Community Edition](https://www.mongodb.com/try/download/community) (Local)
   - **Option B**: [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) (Cloud - Free tier available)

## 🚀 Installation & Setup

### Step 1: Navigate to Project Directory

```powershell
cd C:\Users\krish\expense-tracker
```

### Step 2: Create Virtual Environment

```powershell
python -m venv venv
```

### Step 3: Activate Virtual Environment

**Windows PowerShell:**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows CMD:**
```cmd
venv\Scripts\activate.bat
```

**If you get an execution policy error in PowerShell, run:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Step 4: Install Dependencies

```powershell
pip install -r requirements.txt
```

### Step 5: MongoDB Setup

#### Option A: Local MongoDB

1. Install MongoDB Community Edition
2. Start MongoDB service:
   ```powershell
   # MongoDB should start automatically, or run:
   net start MongoDB
   ```
3. Keep the default `.env` configuration (already set to `mongodb://localhost:27017/`)

#### Option B: MongoDB Atlas (Cloud)

1. Create free account at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a new cluster (free tier M0)
3. Create a database user with password
4. Whitelist your IP address (or use 0.0.0.0/0 for testing)
5. Get your connection string
6. Update `.env` file:
   ```
   MONGODB_URI=mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```

### Step 6: Insert Sample Data (Optional but Recommended)

```powershell
python insert_sample_data.py
```

This will add 20+ realistic sample transactions and budgets to your database.

### Step 7: Run the Application

```powershell
python app.py
```

You should see:
```
✓ MongoDB connected successfully!
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

### Step 8: Access the Application

Open your browser and navigate to:
```
http://localhost:5000
```

## 📱 Application Pages

1. **Dashboard** (`/`) - Overview of your finances with charts and statistics
2. **Add Transaction** (`/add`) - Form to add new income or expense
3. **Transactions** (`/transactions`) - View all transactions with filtering options
4. **Budget** (`/budget`) - Set and track monthly budgets by category
5. **Reports** (`/reports`) - Visual analytics and trends over time

## 🎨 Features Showcase

### Dashboard
- 4 Summary cards (Total Income, Total Expenses, Current Balance, Monthly Expenses)
- Budget alerts when spending exceeds 80% or 100%
- Category breakdown pie chart
- Recent transactions list

### Add Transaction
- Dynamic category selection based on transaction type
- Date picker with default today's date
- Form validation
- Quick tips sidebar

### View Transactions
- Multi-filter support (time period, type, category)
- Summary cards showing filtered totals
- Sortable table view
- Delete functionality with confirmation

### Budget Management
- Set budgets per category for current month
- Visual progress bars with color coding
- Status indicators (safe, warning, exceeded)
- Budget tips section

### Reports & Analytics
- Month and year statistics comparison
- 6-month income vs expenses trend line chart
- Category distribution pie chart
- Detailed category breakdown table

## 🗄️ Database Schema

### Transactions Collection
```javascript
{
  _id: ObjectId,
  type: "income" | "expense",
  amount: Number,
  category: String,
  description: String,
  date: ISODate,
  created_at: ISODate
}
```

### Budgets Collection
```javascript
{
  _id: ObjectId,
  category: String,
  amount: Number,
  month: Number,
  year: Number,
  updated_at: ISODate
}
```

### Categories
- **Expenses**: Food, Transport, Entertainment, Healthcare, Utilities, Shopping, Other
- **Income**: Salary, Other

## 🛑 Troubleshooting

### MongoDB Connection Issues

**Error**: `MongoDB connection failed`

**Solutions**:
1. Ensure MongoDB service is running: `net start MongoDB`
2. Check your `.env` file has correct MongoDB URI
3. For Atlas, verify:
   - IP whitelist includes your IP
   - Username and password are correct
   - Connection string is properly formatted

### Python Package Issues

**Error**: `ModuleNotFoundError`

**Solution**:
```powershell
pip install --upgrade -r requirements.txt
```

### Port Already in Use

**Error**: `Address already in use`

**Solution**: Change port in `app.py`:
```python
app.run(debug=True, port=5001)  # Use different port
```

### Virtual Environment Not Activating

**Solution**:
```powershell
# PowerShell execution policy fix
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 🔐 Security Notes

⚠️ **Important for Production**:
1. Change `SECRET_KEY` in `.env` to a strong random string
2. Never commit `.env` file to version control
3. Use environment variables for sensitive data
4. Enable MongoDB authentication
5. Use HTTPS in production
6. Set `FLASK_ENV=production` in `.env`

## 📦 Project Structure

```
expense-tracker/
├── app.py                      # Flask application
├── insert_sample_data.py       # Sample data insertion script
├── requirements.txt            # Python dependencies
├── .env                        # Environment configuration
├── README.md                   # This file
├── templates/                  # HTML templates
│   ├── base.html              # Base template
│   ├── index.html             # Dashboard
│   ├── add_transaction.html   # Add transaction form
│   ├── view_transactions.html # Transactions list
│   ├── budget.html            # Budget management
│   └── reports.html           # Reports & analytics
└── static/                     # Static assets
    ├── css/
    │   └── style.css          # Custom styles
    └── js/
        └── main.js            # JavaScript code
```

## 🎯 Usage Tips

1. **Start with Sample Data**: Run `insert_sample_data.py` to see the app in action
2. **Set Budgets First**: Go to Budget page and set monthly limits
3. **Regular Updates**: Add transactions as they occur for accurate tracking
4. **Weekly Reviews**: Check Reports page to analyze spending patterns
5. **Budget Alerts**: Pay attention to warnings when approaching budget limits

## 🔄 Updating the Application

To update dependencies:
```powershell
pip install --upgrade -r requirements.txt
```

To reset database (warning: deletes all data):
```powershell
python insert_sample_data.py
```

## 📝 License

This project is for educational and personal use.

## 👨‍💻 Author

Built by Krishna Naicker

## 🆘 Support

For issues or questions:
1. Check the Troubleshooting section
2. Verify MongoDB is running
3. Ensure all dependencies are installed
4. Check Python and MongoDB versions

---

**Happy Expense Tracking! 💰📊**
