import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import datetime
import numpy as np
from fastapi import FastAPI, Query
from sklearn.preprocessing import PolynomialFeatures

app2 = FastAPI()

# Load your dataset (assuming it's in a CSV file)
data = pd.read_csv("unique_dates_cities_df.csv")

data = data.drop("Unnamed: 0", axis=1)

# Preprocessing
# Assuming your dataset has columns: 'datetime', 'city', 'count'
# Convert the 'datetime' column to a proper datetime format
data['datetime'] = pd.to_datetime(data['datetime'])

# Extract relevant features from the datetime column
data['year'] = data['datetime'].dt.year
data['month'] = data['datetime'].dt.month
data['day'] = data['datetime'].dt.day
data['day_of_week'] = data['datetime'].dt.dayofweek  # Monday = 0, Sunday = 6

# One-hot encode the 'city' column
data = pd.get_dummies(data, columns=['city'], prefix='city')

# Split the data
X = data.drop(["count", "datetime"], axis=1)  # Features
y = data["count"]  # Target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


def model_training():
    # Model Training
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Model Evaluation
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    print(f"Root Mean Squared Error: {rmse}")



#
# def polynomial_model_training(degree):
#     # Generate polynomial features
#     poly = PolynomialFeatures(degree=degree)
#     X_train_poly = poly.fit_transform(X_train)
#     X_test_poly = poly.transform(X_test)
#
#     # Model Training
#     model = LinearRegression()
#     model.fit(X_train_poly, y_train)
#
#     # Model Evaluation
#     y_pred = model.predict(X_test_poly)
#     mse = mean_squared_error(y_test, y_pred)
#     rmse = np.sqrt(mse)
#     print(f"Root Mean Squared Error (Polynomial Degree {degree}): {rmse}")
#
# # Set the degree of the polynomial
# degree = 2  # You can experiment with different degrees
#
# polynomial_model_training(degree)




def save_model():
    # Save the model to a file
    joblib.dump(model, 'randomForest_regression_model.pkl')
    # joblib.dump(model, 'models/linear_regression_model.pkl')
# model_training()
# save_model()


# Load the saved model from the file
model = joblib.load('models/linear_regression_model.pkl')


def predict_count_for_date_and_city(date, city):
    # Prepare input features for prediction
    input_data = {
        'year': [date.year],
        'month': [date.month],
        'day': [date.day],
        'day_of_week': [date.weekday()],
    }

    # Get the list of all city columns used during training
    city_columns = [col for col in X_train.columns if col.startswith('city_')]

    # Set all city columns to 0
    for col in city_columns:
        input_data[col] = [0]

    # Set the corresponding city column to 1 based on the input city
    input_data[f'city_{city}'] = [1]

    # Make predictions
    prediction = model.predict(pd.DataFrame(input_data))
    return prediction[0]


# @app2.get("/predict_future_tweet_count/")
def predict_future_tweet_count(predict_date: str, select_city: str):
    print(predict_date)
    # Your prediction logic here
    print({"message": "Prediction result"})
    # Convert the string to a datetime object
    date_obj = datetime.datetime.strptime(predict_date, "%Y-%m-%d")

    # Extract year, month, and day as integers
    year = date_obj.year
    month = date_obj.month
    day = date_obj.day

    print(year, month, day)

    date_to_predict = datetime.datetime(year,month,day)  # Replace with the desired date
    city_to_predict = select_city  # Replace with the desired city
    predicted_count = predict_count_for_date_and_city(date_to_predict, city_to_predict)
    print(f"Predicted count for {date_to_predict} in {city_to_predict}: {predicted_count}")
    return predicted_count

