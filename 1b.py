import pandas as pd
import matplotlib.pyplot as plt
import os

# Path to uploaded file (Double-check for any typo in the file path)
file_path = 'C:\\Users\\Admin\\Downloads\\archive (2)\\train.csv'

# Check if file exists
if os.path.exists(file_path):
    print("File exists. Ready for processing.")
else:
    print("File not found at:", file_path)

# Load and Clean Data
def load_and_clean_data(file_path):
    try:
        # Load data from CSV
        data = pd.read_csv(file_path)
        print("Data loaded successfully!")

        # Display initial info and preview data
        print("\nInitial Data Info:")
        print(data.info())
        print("\nSample Data:")
        print(data.head())

        # Drop rows with missing values
        data = data.dropna()
        print("\nMissing values removed. Data cleaned successfully!")

        # Ensure date columns are in datetime format
        data['Order Date'] = pd.to_datetime(data['Order Date'], errors='coerce')
        data['Ship Date'] = pd.to_datetime(data['Ship Date'], errors='coerce')

        # Check for any invalid datetime conversions
        if data['Order Date'].isnull().any():
            print("\nError: Some 'Order Date' values could not be converted. Check input data.")
        return data
    except Exception as e:
        print(f"Error loading or cleaning data: {e}")
        return None

# Calculate Metrics
def calculate_metrics(data):
    try:
        # Total and average sales
        total_sales = data['Sales'].sum()
        avg_sales = data['Sales'].mean()

        # Sales trend over time
        sales_trend = data.groupby(data['Order Date'].dt.to_period('M'))['Sales'].sum()

        print(f"\nTotal Sales: {total_sales}")
        print(f"Average Sales: {avg_sales}")
        return total_sales, avg_sales, sales_trend
    except KeyError as e:
        print(f"Missing column for metric calculation: {e}")
        return None, None, None

# Visualize Data
def visualize_sales(data, sales_trend):
    try:
        # Total Sales by Category
        if 'Category' in data.columns:
            data.groupby('Category')['Sales'].sum().plot(kind='bar', title='Total Sales by Category', color='skyblue')
            plt.xlabel('Category')
            plt.ylabel('Total Sales')
            plt.show()

        # Total Sales by Region
        if 'Region' in data.columns:
            data.groupby('Region')['Sales'].sum().plot(kind='bar', title='Total Sales by Region', color='orange')
            plt.xlabel('Region')
            plt.ylabel('Total Sales')
            plt.show()

        # Sales Trend Over Time
        sales_trend.plot(title='Sales Trend Over Time', marker='o', color='green')
        plt.xlabel('Order Date')
        plt.ylabel('Sales')
        plt.show()
    except Exception as e:
        print(f"Error in visualization: {e}")

# Identify Top Performers
def top_performers(data, column, n=5):
    if column in data.columns:
        # Calculate top N performers by total sales
        top_items = data.groupby(column)['Sales'].sum().sort_values(ascending=False).head(n)
        print(f"\nTop {n} {column}s by Sales:")
        print(top_items)
        
        # Plot top N items
        top_items.plot(kind='bar', title=f'Top {n} {column}s by Sales', color='purple')
        plt.xlabel(column)
        plt.ylabel('Total Sales')
        plt.show()
    else:
        print(f"Column '{column}' not found in the dataset.")

# Main Function
def main():
    file_path = 'C:\\Users\\Admin\\Downloads\\archive (2)\\train.csv'  # Ensure path is correct
    data = load_and_clean_data(file_path)
    
    if data is not None:
        # Calculate Metrics
        total_sales, avg_sales, sales_trend = calculate_metrics(data)
        
        # Visualize Metrics
        visualize_sales(data, sales_trend)
        
        #  Analyze Top Performers
        if 'Product Name' in data.columns:
            top_performers(data, 'Product Name')  # Top 5 Products
        if 'Region' in data.columns:
            top_performers(data, 'Region')  # Top 5 Regions

# Run the script
if __name__ == "__main__":
    main()
