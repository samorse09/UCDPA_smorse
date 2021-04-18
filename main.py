import pandas as pd
import numpy as np
file1 = '/Users/smorse/Documents/GitHub/UCDPA_smorse/Data/SCMData1.csv'
data1 = pd.read_csv(file1, header = 0)
print(data1.head(5))
print(data1.shape)
#count the number of missing values in each column
missing_values_count = data1.isnull().sum()
print(missing_values_count[0:25])
#droprows = data1.dropna()
#print(data1.shape, droprows.shape)
#convert to dataframe
df1 = pd.DataFrame(data1)
#remove unnecessary columns (zipcode)
df1 = df1.drop(['Customer Zipcode'], axis = 1)
print(df1.shape)
print(df1.head(5))
header_data = df1.set_index('Unique ID')
print(header_data.head(2))
group_customer = header_data()
