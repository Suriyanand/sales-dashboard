from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)  # Allow requests from any origin (frontend)

EXCEL_FILE = 'sales_data.xlsx'

# Create the Excel file with headers if it doesn't exist
if not os.path.exists(EXCEL_FILE):
    df = pd.DataFrame(columns=['Date', 'Amount'])
    df.to_excel(EXCEL_FILE, index=False)

@app.route('/submit', methods=['POST'])
def submit_data():
    try:
        data = request.get_json()
        date = data.get('date')
        amount = data.get('amount')

        if not date or not amount:
            return jsonify({'error': 'Date and Amount are required!'}), 400

        # Load existing data
        df = pd.read_excel(EXCEL_FILE, engine='openpyxl')
        
        # Append new data
        new_row = pd.DataFrame({'Date': [date], 'Amount': [amount]})
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_excel(EXCEL_FILE, index=False, engine='openpyxl')

        return jsonify({'message': '✅ Data saved successfully!'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def home():
    return '🎉 Welcome to Daily Sales Analyzer API!'

if __name__ == '__main__':
    app.run(debug=True)
