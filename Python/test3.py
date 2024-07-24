import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import missingno as msno

diabetes_data = pd.read_csv('diabetes.csv')

# for col in data.columns:
#     missing_data = data[col].isna().sum()
#     missing_percent = missing_data / len(data) * 100
#     print(f'Column: {col} has {missing_percent} %')
diabetes_data_copy = diabetes_data.copy(deep = True)
diabetes_data_copy[['Glucose','BloodPressure','SkinThickness','Insulin','BMI']] = diabetes_data_copy[['Glucose','BloodPressure','SkinThickness','Insulin','BMI']].replace(0,np.NaN)

## showing the count of Nans
print(diabetes_data_copy.isnull().sum())
diabetes_data_copy['Glucose'].fillna(diabetes_data_copy['Glucose'].mean())
diabetes_data_copy['BloodPressure'].fillna(diabetes_data_copy['BloodPressure'].mean())
diabetes_data_copy['SkinThickness'].fillna(diabetes_data_copy['SkinThickness'].median())
diabetes_data_copy['Insulin'].fillna(diabetes_data_copy['Insulin'].median())
diabetes_data_copy['BMI'].fillna(diabetes_data_copy['BMI'].median())
#p = diabetes_data_copy.hist(figsize = (20,20))
# plt.show()
# diabetes_data_shape = diabetes_data.shape
# print(diabetes_data_shape)
# data type analysis
# plt.figure(figsize=(5,5))
# sns.set(font_scale=2)
# sns.countplot(y=diabetes_data.dtypes ,data=diabetes_data)
# plt.xlabel("count of each data type")
# plt.ylabel("data types")
# plt.show()
# p=msno.bar(diabetes_data)
# plt.show()
color_wheel = {1: "#0392cf",
               2: "#7bc043"}
colors = diabetes_data["Outcome"].map(lambda x: color_wheel.get(x + 1))
print(diabetes_data.Outcome.value_counts())
p=diabetes_data.Outcome.value_counts().plot(kind="bar")
plt.show()
import pandas.tools.plotting
p=scatter_matrix(diabetes_data,figsize=(25, 25))