import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('Class/IntroPy/European_Ski_Resorts.csv')


df = df.sort_values(by='TotalSlope', ascending=False)

grouped = df.groupby('Resort')['Country'].apply(lambda x: x.mode()[0])
print('Printing Grouped')
print(grouped)

austria_df = df[df['Country'] == 'Austria']
df['TotalLifts'].plot(kind='hist')
plt.title('Lifts in Austria')
plt.xlabel('')
plt.ylabel('')
plt.show()