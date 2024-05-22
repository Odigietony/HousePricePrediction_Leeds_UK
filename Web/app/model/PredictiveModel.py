import os
import numpy as np
import pandas as pd
from app.model.data import get_data, transform_data
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor



def predict(property_type, state_of_house, year, month):
    file_path = os.path.abspath("app/model/dataset/pp-complete-2.xlsx")
    data = get_data(file_path)
    normalized_data = transform_data(data)
    accepted_features = ['Year', 'Month', 'Property type_D', 'Property type_F', 'Property type_O', 'Property type_S', 'Property type_T', 'Old/New_N', 'Old/New_Y']
    property = {'Property type_D': [1, 0, 0,0,0], 'Property type_F': [0, 1, 0,0,0], 'Property type_O': [0, 0, 1,0,0], 'Property type_S': [0, 0, 0,1,0], 'Property type_T': [0, 0, 0,0,1]}
    old_new = {'Old/New_N': [1, 0], 'Old/New_Y': [0, 1]}
    X_train = normalized_data[accepted_features]
    y_train = normalized_data['Normalized Price']
    random_forest_model_2 = RandomForestRegressor(n_estimators=500, min_samples_split = 10, random_state=42)
    random_forest_model_2.fit(X_train, y_train)
    # Predict on the training data
    y_prediction_rf = random_forest_model_2.predict(X_train)
    # Calculate the residuals
    residuals = y_train - y_prediction_rf
    # Initialize the gradient boosting regressor
    gbr = GradientBoostingRegressor(n_estimators=500, max_depth=5, random_state=42)
    # Fit the model on residuals
    gbr.fit(X_train, residuals)
    X_test = pd.DataFrame([[year] + [month] + property[property_type] + old_new[state_of_house]], columns=accepted_features)
    # Predict on the test data using both models
    y_pred_rf_test = random_forest_model_2.predict(X_test)[0]
    y_pred_gbr_test = gbr.predict(X_test)[0]
    # Combine predictions
    predicted_price = y_pred_rf_test + y_pred_gbr_test
    predicted_price = np.exp(predicted_price)
    price_to_return = "£{:,.2f}".format(predicted_price)
    return price_to_return