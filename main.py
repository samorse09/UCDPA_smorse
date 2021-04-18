import pandas as pd
import numpy as np

file1 = '/Users/smorse/Documents/GitHub/UCDPA_smorse/Data/SCMData1.csv'
data1 = pd.read_csv(file1, header=0)
print(data1.head(5))
print(data1.shape)
# count the number of missing values in each column
missing_values_count = data1.isnull().sum()
print(missing_values_count[0:25])
# droprows = data1.dropna()
# print(data1.shape, droprows.shape)
# convert to dataframe
df1 = pd.DataFrame(data1)
# remove unnecessary columns (zipcode)
df1 = df1.drop(['Customer Zipcode'], axis=1)
print(df1.shape)
print(df1.head(5))
header_data = df1.set_index('Unique ID').sort_index()
print(header_data.head(2))
hd_keys = header_data.keys()
print(hd_keys)

# Create subset to count number of individual customers
hd_cusnum = header_data.drop_duplicates(subset='Customer Id')
count_hd_cusnum = header_data.value_counts('Customer Id')
print(count_hd_cusnum)

#number of orders by customer
cusords = header_data['Customer Id'].value_counts()
print(cusords)

#create subsets by late or on time
dstatus_num = header_data['Late_delivery_risk'].value_counts()
print(dstatus_num)
#add column for number of days late
header_data['days_late'] = header_data['Days for shipment (scheduled)'] - header_data['Days for shipping (real)']
print(header_data.head(5))

#add column for late status
status =  []
for value in header_data['Late_delivery_risk']:
    if value == 1:
        status.append("Late")
    else:
        status.append('On_Time')
header_data['Late_Status'] = status
print(header_data.head())

file2 = '/Users/smorse/Documents/GitHub/UCDPA_smorse/Data/SCMData2.csv'
data2 = pd.read_csv(file2, header=0)

#avgdays_late = is_late['days_late'].mean()
#print(avgdays_late)

df2 = pd.DataFrame(data2)
order_data = df2.set_index('Unique ID').sort_index()
order_data = order_data.drop(columns='Order Id')
order_data = order_data.drop(columns='Order Item Id')
order_data = order_data.drop(columns='Order Status')
print(order_data.head(5))

#merge the two data frames
all_data = header_data.merge(order_data, on='Unique ID')
print(all_data.head(5))

is_late = all_data[all_data['Late_Status'] == 'Late']
on_time = all_data[all_data['Late_Status'] == 'On_Time']

print(np.shape(is_late))
print(np.shape(on_time))

lates_region = is_late['Order Region'].value_counts()
print(lates_region)

ontime_region = on_time['Order Region'].value_counts()
print(ontime_region)

total_byregion = all_data['Order Region'].value_counts()
print(total_byregion)

percent_byregion = lates_region / total_byregion
print(percent_byregion)

lates_customer = is_late['Customer Id'].value_counts()
print(lates_customer)

print(cusords)

percent_bycus = lates_customer / cusords
#print(percent_bycus)

lates_market = is_late['Market'].value_counts()
total_bymarket = all_data['Market'].value_counts()
percent_bymarket = lates_market / total_bymarket
#print(percent_bymarket)

import matplotlib.pyplot as plt

market_alldata = all_data[['Market','Customer Id','order date (DateOrders)','shipping date (DateOrders)','Late_Status','Department Name']]
#print(market_alldata.head(5))
#market_alldata = all_data.set_index("Market")
#min and max dates for each market
market_group = market_alldata.groupby('Market')['order date (DateOrders)'].agg([min,max])
#print(market_group)

#africa_orders = all_data[all_data['Market'] == "Africa"]
#print(africa_orders)
#africa_markets = africa_orders['Department Name'].value_counts()
#print(africa_markets)

markets = all_data.groupby('Market')

africa = markets.get_group('Africa')
asia = markets.get_group('Pacific Asia')
latam = markets.get_group('LATAM')
europe = markets.get_group('Europe')
usca = markets.get_group('USCA')

#print(africa['Department Name'].value_counts())
#print(usca['Department Name'].value_counts())
#print(africa.groupby('Department Name')['Order Item Total'].sum())
#africa_sales = africa.groupby('Department Name')
#africa_sales['Sales Total'] = africa.groupby('Department Name')['Order Item Total'].sum()


fraud = all_data[all_data['Order Status'] == "SUSPECTED_FRAUD"]
fraud_market = fraud['Market'].value_counts()
print(fraud_market)
print(total_bymarket)
perc_fraud = fraud_market / total_bymarket
print(perc_fraud)

print(lates_market)
print(percent_bymarket)
print(markets['Department Name'].value_counts())
