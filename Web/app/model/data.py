import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder


def get_data(source):
    try:
        data = pd.read_excel(source)
        return pd.DataFrame(data)
    except Exception as e:
        print(f"Error occured while retrieving data: {e}")
        return None

def transform_data(data):
    # Step 2: Data Cleaning.
    Leeds_dataset = data[data['District'] == 'LEEDS']
    df = Leeds_dataset.copy()
    df_clean_col = df.drop(['SAON', 'Locality'], axis=1) # They both have incredibly high number of null values
    df_clean = df_clean_col.dropna()
    dataset = df_clean.drop(['Id', 'Postcode', 'PAON', 'Town/City',  'District', 'Duration',  'County', 'Street', 'Category type', 'Record Status - monthly file only'], axis=1)
    dataset = dataset.drop_duplicates()
    # Remove all prices below $10,000 and above $500,000
    dataset = dataset[(dataset['Price'] < 500000) & (dataset['Price'] > 10000)]
    date = pd.to_datetime(dataset['Date']) 
    year = date.dt.year
    month = date.dt.month
    dataset['Year'] = year
    dataset['Month'] = month
    dataset = dataset.drop(['Date'], axis=1)
    # Encoding Categorical Variables: Using get_dummies
    values_to_encode = ['Property type', 'Old/New']
    dataset = pd.get_dummies(dataset, columns=values_to_encode)
    # Fit and transform the 'Price' data
    # Reshape data using .values.reshape(-1, 1) because scaler expects 2D array
    dataset['Normalized Price'] = np.log(dataset['Price'])
    return dataset.drop(['Price'], axis=1)
