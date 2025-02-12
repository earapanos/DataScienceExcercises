

https://github.com/user-attachments/assets/16c315ed-06a3-4caf-915e-4079fdf61c46


# Income Forecast for Financial Institutions

## Overview
This project focuses on predicting customer income for financial institutions using a dataset containing customer demographics, socioeconomic details, and financial attributes. The goal is to assist in decision-making for credit limits, loan amounts, and personalized financial product offerings.

## Key Steps

### 1. **Data Understanding**
   - **Dataset**: Contains 14 columns with customer information (e.g., age, gender, income type, education, marital status).
   - **Missing Data**: Handled missing values in the `employment_time` column.
   - **Data Types**: Numerical (e.g., age, income) and categorical (e.g., gender, education) variables.

### 2. **Data Preparation**
   - **Cleaning**: Removed missing values and irrelevant columns (`id_cliente`, `Unnamed: 0`, `data_ref`).
   - **Transformation**: Encoded categorical variables (e.g., gender) and created dummy variables for modeling.
   - **Feature Selection**: Selected significant variables using LASSO regularization.

### 3. **Modeling**
   - **Algorithm**: Decision Tree Regressor.
   - **Hyperparameter Tuning**: Optimized `max_depth` and `min_samples_leaf` for better performance.
   - **Evaluation**: Achieved an R-squared of ~48% for training and ~42% for testing, with a Mean Absolute Error (MAE) of ~3400.

### 4. **Deployment**
   - **Model Saving**: Saved the trained model using `joblib`.
   - **Prediction Function**: Created a function to classify customers based on predicted income into credit limits, card types, and loan amounts.
   - **Application**: Applied the model to new data, generating predictions and saving results to a CSV file.

## Results
The model effectively predicts customer income, enabling financial institutions to make informed decisions on credit limits, loan amounts, and product offerings. The deployment phase demonstrates practical applications, such as assigning credit limits and card classes based on predicted income.

## Future Work
- Incorporate additional variables (e.g., credit history, delinquency status) for more accurate predictions.
- Explore other machine learning algorithms (e.g., Random Forest, Gradient Boosting) for improved performance.
- Implement the model in a real-time system for automated decision-making.

## Streamlit
- You can access the project on streamlit: 