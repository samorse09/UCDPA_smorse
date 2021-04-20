import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

file1 = '/Users/smorse/Documents/GitHub/UCDPA_smorse/Data/SCMData1a.csv'
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
# remove unnecessary column (zipcode)
df1 = df1.drop(['Customer Zipcode'], axis=1)
print(df1.shape)
print(df1.head(5))
#set Unique ID as the Index
header_data = df1.set_index('Unique ID').sort_index()
print(header_data.head(2))
#check the column names / keys for further reference
hd_keys = header_data.keys()
print(hd_keys)

sns.set_theme(style='ticks')

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
header_data['days_late'] = header_data['Days for shipping (real)'] - header_data['Days for shipment (scheduled)']
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

#read the second data set
file2 = '/Users/smorse/Documents/GitHub/UCDPA_smorse/Data/SCMData2.csv'
data2 = pd.read_csv(file2, header=0)
#create dataframe for second data set, dropping unnecessary columns
df2 = pd.DataFrame(data2)
order_data = df2.set_index('Unique ID').sort_index()
order_data = order_data.drop(columns='Order Id')
order_data = order_data.drop(columns='Order Item Id')
order_data = order_data.drop(columns='Order Status')
print(order_data.head(5))

#merge the two data frames
all_data = header_data.merge(order_data, on='Unique ID')
print(all_data.head(5))

#break out orders by late and on time
is_late = all_data[all_data['Late_Status'] == 'Late']
on_time = all_data[all_data['Late_Status'] == 'On_Time']

print(np.shape(is_late))
print(np.shape(on_time))

lates_region = is_late['Order Region'].value_counts()
print(lates_region)

orders_by_seg = all_data['Customer Segment'].value_counts

palette1 = ['b','y','r']
palette2 = ['c','m','b']

#number of late orders vs. total number of orders by customer segment
orders_by_seg_plot = sns.countplot(x='Customer Segment', data=all_data,palette=palette1, saturation=.8).set_title('# Orders Late Out of Total')
late_by_seg_plot = sns.countplot(x='Customer Segment',data=is_late,saturation=0.99,palette=palette2)
plt.show()



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

market_alldata = all_data[['Market','Customer Id','YEAR OF ORDER','Late_Status','Department Name','Shipping Mode','Order Profit Per Order','Category Name']]
#print(market_alldata.head(5))
#market_alldata = all_data.set_index("Market")
#min and max dates for each market
market_group = market_alldata.groupby('Market')['YEAR OF ORDER'].agg([min,max])
print(market_group)

markets = all_data.groupby('Market')

africa = markets.get_group('Africa')
asia = markets.get_group('Pacific Asia')
latam = markets.get_group('LATAM')
europe = markets.get_group('Europe')
usca = markets.get_group('USCA')


print(lates_market)
print(percent_bymarket)
markets_dept = markets['Department Name'].value_counts()
print(markets_dept)


pt1 = all_data.pivot_table(values='Order Profit Per Order',index='Market',columns='YEAR OF ORDER',aggfunc=np.sum, fill_value=0)
print(pt1)

#sns.countplot(x='Department Name',data=all_data)
#plt.show()

#count of orders by department in each market
#sns.countplot(x='Department Name',data=all_data,hue='Market')
#plt.show()

#average profit per order based on department in each market
#sns.catplot(x='Market',y='Order Profit Per Order',data=all_data,kind='bar',hue='Department Name',ci=none)
#plt.show()

#sns.catplot(x='Department Name',y='Order Profit Per Order',data=all_data,kind='bar',ci=none)
#plt.show()

#mall_date = market_alldata.sort_values('YEAR OF ORDER')
#plot_a = sns.catplot(x='Department Name',data=mall_date,kind='count',hue='YEAR OF ORDER',col='Market', col_wrap=3)
#plt.xticks(rotation=45)
#plt.tight_layout()
#plt.show()

plot_b = sns.catplot(x='Shipping Mode',data=all_data,kind='count',hue='Late_Status')
plt.show()

plot_mode_region = sns.catplot(x='Market', kind='count',col='Shipping Mode', col_wrap=2, hue='Late_Status',data=all_data).set_xticklabels()
plt.show()