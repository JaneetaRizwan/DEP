import pandas as pd
import matplotlib.pyplot as plt

data = {
    'city': ['Karachi', 'Lahore', 'Faisalabad', 'Rawalpindi', 'Multan', 
             'Peshawar', 'Islamabad', 'Quetta', 'Sialkot', 'Gujranwala'],
    'population': [15741000, 12188000, 3203846, 2098231, 1871843, 
                   1970042, 1095064, 1001205, 920000, 2027001]
}

df = pd.DataFrame(data)
print(df)
print(df.describe())

plt.figure(figsize=(10, 6))
plt.plot(df['city'], df['population'], marker='o')
plt.title('Population of Cities in Pakistan - Line Chart')
plt.xlabel('City')
plt.ylabel('Population')
plt.grid(True)
plt.show()


plt.figure(figsize=(10, 6))
plt.bar(df['city'], df['population'], color='skyblue')
plt.title('Population of Cities in Pakistan - Bar Chart')
plt.xlabel('City')
plt.ylabel('Population')
plt.xticks(rotation=45)
plt.show()


plt.figure(figsize=(10, 6))
plt.pie(df['population'], labels=df['city'], autopct='%1.1f%%', startangle=140)
plt.title('Population Distribution of Cities in Pakistan - Pie Chart')
plt.axis('equal')  
plt.show()
