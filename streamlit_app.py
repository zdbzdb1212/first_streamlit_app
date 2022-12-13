import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Menu')
streamlit.text('Omega 3 & Blueberry Oatmeal')
streamlit.text('Kale, Spinach & Rocket Smoothie')
streamlit.text('Hard Boiled Free Range Egg')

streamlit.header('Build Your Own Fruit Smoothie')
my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

fruits_selected = streamlit.multiselect('Pick some fruits:', list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits = my_fruit_list.loc[fruits_selected]

streamlit.dataframe(fruits)

def get_fruityvice_data(user_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + user_fruit_choice)
  fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

streamlit.header('Fruityvice Fruit Advice!')
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    back_from_fn = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_fn)

except URLError as e:
  streamlit.stop()
  
streamlit.header("The fruit load list contains:")
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("use warehouse compute_wh")
    my_cur.execute("select * from fruit load list")
    return my_cur.fetchall
  
if streamlit.button('Get Fruit Load List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  streamlit.dataframe(my_data_rows)
  
  def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
      my_cur.execute("use warehouse compute_wh")
      my_cur.execture("insert into fruit_load_list values ('from streamlit')")
      return "Thanks for adding " + new_fruit
    

add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a Fruit to the List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  back_from_fn = insert_row_snowflake(add_my_fruit)
  streamlit.text(back_from_function)
