import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import requests
import json


st.title('Airbnb Listings Map')
with st.sidebar:
     selected = option_menu(
            "Main Menu",
            ["Home", "price distribution by property type","Review Scores Analysis",
             "Price vs. Number of Guests","Comparison of Prices Across Different Cities",
             "Price Trend by Month"])
            




cleaned_data=r"C:\Users\Shanmugam.V\Desktop\Airbnb\cleaned_dataset.csv" 
df_cleaned = pd.read_csv(cleaned_data)

def extract_date_from_reviews(reviews):
    try:
        # Convert the 'reviews' string into a list of dictionaries
        review_data = eval(reviews)
        # Ensure review_data is a list and not empty
        if isinstance(review_data, list) and len(review_data) > 0:
            # Extract date from the first review, if it exists
            review_date = review_data[0].get('date')
            # Return the date, defaulting to '1970-01-01' if it's not present
            return pd.to_datetime(review_date, errors='coerce') or pd.to_datetime('1970-01-01')
        return pd.to_datetime('1970-01-01')
    except Exception as e:
        # Log the error for debugging purposes
        print(f"Error extracting date: {e}")
        return pd.to_datetime('1970-01-01')
    

if selected=="Home":
    st.header("Welcome to the Airbnb project")
    
# Create a box plot to visualize the price distribution by property type   
elif selected=="price distribution by property type":    
    fig_1 = px.box(df_cleaned, x="property_type", y="monthly_price", title="Price Distribution by Property Type")
    st.plotly_chart(fig_1)
    
elif selected=="Review Scores Analysis":
    df_cleaned['review_scores_accuracy'] = df_cleaned['review_scores'].apply(lambda x: eval(x).get('review_scores_accuracy', 0))    
    fig_2 = px.scatter(df_cleaned, x="review_scores_accuracy", y="monthly_price", 
    title="Review Scores vs. Monthly Price",
    labels={'review_scores_accuracy': 'Review Scores', 'monthly_price': 'Monthly Price'},
    hover_data={'review_scores_accuracy': True, 'monthly_price': True})
    st.plotly_chart(fig_2)
    
elif selected=="Price vs. Number of Guests":
    fig_3 = px.scatter(df_cleaned, x="guests_included", y="monthly_price", title="Price vs. Number of Guests")
    st.plotly_chart(fig_3)
    
elif selected=="Comparison of Prices Across Different Cities":
    df_cleaned['city'] = df_cleaned['address'].apply(lambda x: eval(x).get('suburb', 'Unknown'))
    fig_4 = px.box(df_cleaned, x="city", y="monthly_price", title="Price Comparison Across Cities")
    st.plotly_chart(fig_4)
    
elif selected=="Price Trend by Month":
    df_cleaned['date'] = df_cleaned['reviews'].apply(extract_date_from_reviews)
    df_cleaned['month'] = df_cleaned['date'].dt.to_period('M')
    avg_price_by_month = df_cleaned.groupby('month')['monthly_price'].mean().reset_index()
    avg_price_by_month['month'] = avg_price_by_month['month'].astype(str)
    fig_5 = px.line(avg_price_by_month, x="month", y="monthly_price", 
                title="Price Trend by Month",
                labels={'month': 'Month', 'monthly_price': 'Average Monthly Price'},
                markers=True)
    st.plotly_chart(fig_5)
    

    

    