# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col    

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw: {st.__version__}")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """)

#import streamlit as st

name_on_order = st.text_input('Name on smoothie:')
st.write('The name on the smoothie will be:', name_on_order)

#option = st.selectbox(
#    "What is your favorite fruit?",
#    ("Banana", "Strawberries", "Peaches"),
#)

#st.write("You selected:", option)

cnx =st.connection("snowflake")
session = cnx.session()

#session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select (col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect('choose upto 5 ingredients:',
                                 my_dataframe, max_selections=5)
if len(ingredients_list) > 5:
    st.warning(f"You selected {len(ingredients_list)} ingredients. Only the 5 will be used from the dropdown.")
    ingredients_list = ingredients_list[:5]

if ingredients_list: 
    #st.write(ingredients_list)
    #st.text(ingredients_list)
    ingredients_string = ''
    for fruit_choosen in ingredients_list:
        ingredients_string += fruit_choosen + ' '

    st.write(ingredients_string)
    

my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """', '"""+name_on_order+"""')"""

#st.write(my_insert_stmt)
#st.stop()

st.write(my_insert_stmt)
time_to_insert = st.button('Submit Order')
if time_to_insert:
    session.sql(my_insert_stmt).collect()
    
#if ingredients_string:
 #   session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!', icon="✅")

#New section to display smoothiefroot nutrition information
import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
#st.text(smoothiefroot_response.json())
sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

