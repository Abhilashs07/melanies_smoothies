# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie :cup_with_straw: {st.__version__}")
st.write("""Choose the fruits you want in your custom Smoothie!""")

name_on_order = st.text_input('Name on smoothie:')
st.write('The name on the smoothie will be:', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()

# Select both FRUIT_NAME and SEARCH_ON columns
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON')).to_pandas()

# Single multiselect widget
ingredients_list = st.multiselect('choose upto 5 ingredients:',
                                 my_dataframe['FRUIT_NAME'].tolist(), max_selections=5)

# Remove st.stop() to allow the rest of the code to execute
# st.dataframe(my_dataframe)  # Optional: show dataframe for debugging

if ingredients_list: 
    ingredients_string = ''
    
    for fruit_chosen in ingredients_list:  # Fixed variable name
        ingredients_string += fruit_chosen + ' '
        
        # Get search value for the fruit
        search_on = my_dataframe.loc[my_dataframe['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen, ' is ', search_on, '.')
        
        # Display nutrition information
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{search_on}")
        
        if smoothiefroot_response.status_code == 200:
            st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
        else:
            st.write("Nutrition information not available for this fruit.")
    
    st.write("Selected ingredients:", ingredients_string)
    
    # Insert statement
    my_insert_stmt = f"""insert into smoothies.public.orders(ingredients, name_on_order)
                values ('{ingredients_string.strip()}', '{name_on_order}')"""
    
    # Submit button
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        if name_on_order:  # Check if name is provided
            session.sql(my_insert_stmt).collect()
            st.success('Your Smoothie is ordered!', icon="✅")
        else:
            st.error("Please enter a name for your smoothie order.")
