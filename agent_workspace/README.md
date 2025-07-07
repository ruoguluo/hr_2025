# Company Analysis Platform

## Database Setup

1. Install MySQL if not already installed:
```bash
brew install mysql  # For macOS
```

2. Start MySQL service:
```bash
brew services start mysql  # For macOS
```

3. Create the database:
```sql
CREATE DATABASE company_analysis;
```

4. Create a MySQL user and grant permissions:
```sql
CREATE USER 'your_username'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON company_analysis.* TO 'your_username'@'localhost';
FLUSH PRIVILEGES;
```

5. Update the database credentials in `db_handler.py`:
```python
self.connection = mysql.connector.connect(
    host="localhost",
    user="your_username",    # Update this
    password="your_password", # Update this
    database="company_analysis"
)
```

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python api_server.py
```

The application will now store all company analysis data in the MySQL database automatically.