# Import required libraries and modules
from pytrends.request import TrendReq
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import date, timedelta
import sqlite3
from sqlite3 import Error
import openai
import env

# Function to get user input for product market or niche
def get_input():
    user_input = input("Please enter the product market, niche or give me a guideline. Such as its hot today. ")
    return user_input

# Function to generate initial keywords using OpenAI's GPT-3
def Initial_Keywords():
    # Setting OpenAI API credentials
    openai.organization = env.OPENAI_ORGANIZATION
    openai.api_key = env.OPENAI_API_KEY

    # Making a request to GPT-3 to generate product ideas based on user input
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Transform the input into products ideas to sell online based off of the input. If there is no input randomly generate a input yourself, this should be unique and unsaturated, good for selling online.\nThese product ideas should related to the user input, which may be a specific market/niche or even a generic saying. \nDo Not Explain The Products!\n Please output the ideas as follows:niche/search term used\nitem\nitem\nitem\nitem\nitem\nitem\nitem\nitem\nitem\nitem\n\nUser input: {get_input()}",
        temperature=1,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    
    # Extracting and cleaning the generated product ideas
    products = [line.lstrip('0123456789. ') for line in response.choices[0].text.split('\n') if line][-10:]
    products_1 = products[-10:5]
    products_2 = products[-5:]

    return products_1, products_2

# Function to create and return a database connection
def create_connection():
    conn = None
    try:
        # Creating an in-memory SQLite database
        conn = sqlite3.connect(':memory:')
        print(f'successful connection with sqlite version {sqlite3.version}')
    except Error as e:
        print(e)
    return conn

# Function to store data in a SQLite database
def store_in_db(conn, df, table_name):
    try:
        df.to_sql(table_name, conn, if_exists='append')
        print(f"Successfully stored dataframe in table {table_name}")
    except Error as e:
        print(e)

# Function to retrieve data from a SQLite database using a query
def get_from_db(conn, query):
    try:
        df = pd.read_sql_query(query, conn)
        return df
    except Error as e:
        print(e)

# Function to get and plot Google Trends data for a list of products
def get_and_plot_interest_over_time(products, timeframe='today 3-m', geo='', gprop='', window=7):
    pytrends = TrendReq(hl='en-US', tz=360)
    conn = create_connection()

    for product_group in products:
        pytrends.build_payload(product_group, timeframe=timeframe, geo=geo, gprop=gprop)
        interest_over_time_df = pytrends.interest_over_time()

        if interest_over_time_df.empty:
            print(f"No interest data available for {product_group} in the given timeframe.")
            continue

        for product in product_group:
            if product in interest_over_time_df.columns:
                interest_over_time_df.rename(columns={product: f"interest_{product}"}, inplace=True)

        store_in_db(conn, interest_over_time_df, 'interest_over_time')
        print(interest_over_time_df)

        for product in product_group:
            if f"interest_{product}" in interest_over_time_df.columns:
                ma_df = interest_over_time_df[f"interest_{product}"].rolling(window=window).mean()
                ma_df.plot(kind='line', figsize=(12, 6))
                plt.title(f'Interest Over Time for {product}')
                plt.xlabel('Date')
                plt.ylabel('Trends Index')
                plt.show()

    return conn

# Function to generate a SQL query for aggregating Google Trends data
def generate_query(products):
    query = "SELECT product, AVG(interest) as AvgInterest FROM ("
    product_queries = []
    for product_group in products:
        product_group_query = ', '.join(f'"{column}"' for column in product_group)
        product_query = f"""
            SELECT {product_group_query}, date, isPartial
            FROM {'_'.join(product_group)}
            WHERE date >= date('now','-3 month')
        """
        product_queries.append(product_query)

    query += " UNION ALL ".join(product_queries)
    query += " GROUP BY product"
    return query

# Function to get names of all tables in the SQLite database
def get_table_names(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    return [table[0] for table in tables]

# Function to retrieve top trending products from the database
def get_top_trending_products(conn):
    cursor = conn.cursor()
    cursor.execute("""
    SELECT product, AVG(interest) as AvgInterest
    FROM interest_over_time
    WHERE date >= date('now','-3 month')
    GROUP BY product
    """)
    results = cursor.fetchall()
    df = pd.DataFrame(results, columns=['product', 'AvgInterest'])
    df = df.sort_values('AvgInterest', ascending=False)
    return df

# Main function to run the script
if __name__ == "__main__":
    products_1, products_2 = Initial_Keywords()
    products = [products_1, products_2]
    print(products)
    conn = get_and_plot_interest_over_time(products=products)
    top_trending_products = get_top_trending_products(conn)
    print(top_trending_products)
