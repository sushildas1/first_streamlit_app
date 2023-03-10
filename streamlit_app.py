import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents new Healthy Diner')

streamlit.header('Breakfast Favorites')
streamlit.text('🥣Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

#creating a function block
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json()) #normalizes the above json data
    return fruityvice_normalized

#new section to import fruityvice api response
streamlit.header('Fruityvice Fruit Advice!')
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
        streamlit.error('Please select a fruit to get more information')
    else:
        function_returned_result = get_fruityvice_data(fruit_choice)
        streamlit.dataframe(function_returned_result)
        
except URLError as e:
    streamlit.error()
  
#import snowflake.connector

streamlit.header("View Our Fruit List - Add Your Favorites!")

def get_fruit_load_list():
    my_cur = my_cnx.cursor()
    my_cur.execute("SELECT * FROM pc_rivery_db.public.FRUIT_LOAD_LIST")
    return my_cur.fetchall()
    
if streamlit.button('Get Fruit List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    my_cnx.close()
    streamlit.dataframe(my_data_rows)
    
#Do not run anything past here until debugging happens
#streamlit.stop()

#allow end user to add a fruit to the list
def insert_row_snowflake(new_fruit_choice_to_add):
    my_cur = my_cnx.cursor()
    my_cur.execute("insert into pc_rivery_db.public.FRUIT_LOAD_LIST values('"+new_fruit_choice_to_add+"')")
    return 'Thanks for adding ' + new_fruit_choice_to_add


new_fruit_choice = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a Fruit to the List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    function_returned_result = insert_row_snowflake(new_fruit_choice)
    streamlit.text(function_returned_result)
