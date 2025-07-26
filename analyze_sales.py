import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Excel file path
EXCEL_FILE = 'sales_data.xlsx'

def analyze_sales():
    try:
        # Read Excel file
        df = pd.read_excel(EXCEL_FILE, engine='openpyxl')

        # Check if required columns are present
        if 'Date' not in df.columns or 'Amount' not in df.columns:
            print("❌ Error: 'Date' or 'Amount' column missing in Excel file.")
            return

        # Convert Date column to datetime
        df['Date'] = pd.to_datetime(df['Date'])

        # Sort by date
        df = df.sort_values(by='Date')

        # Total and average sales
        total_sales = df['Amount'].sum()
        avg_sales = df['Amount'].mean()

        print("📊 Sales Summary:")
        print(f"Total Sales: ₹{total_sales:.2f}")
        print(f"Average Daily Sales: ₹{avg_sales:.2f}")

        # Group by date
        daily_sales = df.groupby(df['Date'].dt.date)['Amount'].sum()

        # Plot sales trend
        plt.figure(figsize=(10, 5))
        daily_sales.plot(kind='line', marker='o', color='blue')
        plt.title('📈 Daily Sales Trend')
        plt.xlabel('Date')
        plt.ylabel('Sales Amount (₹)')
        plt.grid(True)
        plt.tight_layout()
        plt.xticks(rotation=45)
        plt.show()

    except FileNotFoundError:
        print("❌ Error: Excel file not found.")
    except Exception as e:
        print(f"⚠️ Error during analysis: {e}")

if __name__ == '__main__':
    analyze_sales()
