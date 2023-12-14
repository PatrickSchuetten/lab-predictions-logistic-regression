# get data
# clean data, dropping any rows and columns that need to be dropped (1)
# select features (could postpone this)
# X/y split
# Train/Test split
# split both Train and Test in numericals and categoricals
# transformations on numericals:
#     fit ONLY on numericals_train
#     transform BOTH numericals_train and numericals_test
# encoding categoricals
#     fit ONLY on categricals_train
#     transform BOTH categoricals_train and categoricals_test
# combine numericals_train and categoricals_train into train_processed
# combine numericals_test and categoricals_test into test_processed
# define model/s
# fit model on train_processed
# evaluate (score) model on train_processed test_processed

# save model and transformers/encoders/scalers (2)
# save all our functions

# main.py
# For unseen data:
# drop columns and rows according to the criteria used in (1)
# split in numericals and categoricals
# transform numericals and encode categoricals using transformers/encoders saved in (2)
# make predictions using model saved in (2)

import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.tools.tools import add_constant

def plot_distributions(X_train_num: pd.DataFrame):
    n_rows = int(X_train_num.shape[1]/2)
    n_cols = 2
    row_index = 0
    col_index = 0
    fig, ax = plt.subplots(n_rows, n_cols, figsize=(10,5))
    for col in X_train_num:
        sns.histplot(X_train_num[col], ax=ax[row_index, col_index])
        col_index += 1
        if col_index > 1:
            col_index = 0
            row_index += 1
    plt.tight_layout()
    plt.show()

def select_features_for_linear_models_based_on_correlation(df: pd.DataFrame, y: str, threshold=0.75) -> list:
    '''
    This function picks a DataFrame and a `y` column computes the correlation matrix between all the numerical
    columns. Then it returns a Python list with the columns that have a abs(corr(x,y)) >= 0.75

    Inputs:
    df: Pandas DataFrame
    y: string with the column to be considered `y`

    Outputs:
    list of columns highñy correlated with the `y` column
    '''

    df2 = df.copy()
    df2 = df2.select_dtypes([float,int])
    
    correlation_matrix = df2.corr()
    correlation_matrix.drop(y,axis=0, inplace=True)
    
    selected_columns = correlation_matrix[y]

    list_of_selected_columns = correlation_matrix[abs(selected_columns) >= threshold].index.tolist()
    

    return list_of_selected_columns



def compute_vif(df: pd.DataFrame, columns: list):

    X = df.loc[:, columns]
    # the calculation of variance inflation requires a constant
    X.loc[:,'intercept'] = 1

    # create dataframe to store vif values
    vif = pd.DataFrame()
    vif["Variable"] = X.columns
    vif["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
    vif = vif.loc[vif['Variable']!='intercept'].sort_values('VIF', ascending=False).reset_index(drop=True)
    return vif
'''
while any(vif_df["VIF"] > 3):
    selected_columns.remove(vif_df.iloc[0,0])
    display(vif_df)
    print(selected_columns)
    vif_df = compute_vif(reg_data, selected_columns)

display(vif_df)
print("The final selected columns are: ", selected_columns)
'''


from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
def error_metrics_report(y_real_train: list, y_real_test: list, y_pred_train: list, y_pred_test: list) -> pd.DataFrame:
    '''
    Function: Calculate the various error metrics for a given set of train and test data prediciton splits and organaises them DataFrame 
    Input 
    Outtput Dataframe with metrics column and erors sploit by test and training data type
    '''

    MAE_train = mean_absolute_error(y_real_train, y_pred_train)
    MAE_test  = mean_absolute_error(y_real_test,  y_pred_test)

    # Mean squared error
    MSE_train = mean_squared_error(y_real_train, y_pred_train)
    MSE_test  = mean_squared_error(y_real_test,  y_pred_test)
  
    
    # Root mean squared error
    RMSE_train = mean_squared_error(y_real_train, y_pred_train, squared=False)
    RMSE_test  = mean_squared_error(y_real_test, y_pred_test, squared=False)

    # R2
    R2_train = r2_score(y_real_train, y_pred_train)
    R2_test  = r2_score(y_real_test,  y_pred_test)

    results = {"Metric":['MAE','MSE','RMSE','R2'], 
               "Train": [MAE_train, MSE_train, RMSE_train, R2_train],
               "Test":  [MAE_test, MSE_test, RMSE_test, R2_test]}

    results_df = pd.DataFrame(results).round(2)

    return results_df
