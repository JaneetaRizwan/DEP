import requests
from bs4 import BeautifulSoup
import pandas as pd

# Define the URL of the website to scrape
url = "https://weather.com/en-PK/weather/today/l/PKXX0006:1:PK?Goto=Redirected"

# Send a GET request to the website
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all articles (example assumes articles are in <article> tags)
    articles = soup.find_all('article')

    # Lists to store the scraped data
    titles = []
    dates = []

    # Loop through each article and extract data
    for article in articles:
        title = article.find('h2').get_text()  # Assuming the title is in <h2> tags
        date = article.find('time').get_text()  # Assuming the date is in <time> tags

        titles.append(title)
        dates.append(date)

    # Create a DataFrame
    data = {'Title': titles, 'Date': dates}
    df = pd.DataFrame(data)

    # Define absolute path to save CSV file
    save_path = "C:/Users/M. Moaaz/Desktop/Janeeta lol/articles.csv"

    # Save the DataFrame to a CSV file at the specified path
    df.to_csv(save_path, index=False)

    print(f"Data has been scraped and saved to {save_path}")
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
