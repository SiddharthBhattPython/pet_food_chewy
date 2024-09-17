import streamlit as st

from st_aggrid import *

from IPython.display import HTML, display
import re

from ingredient_analyzer_utils import *
from ingredient_analyzer_dictionaries import *

from dog_food_analyzer_utils import *
from dog_food_analyzer_dictionaries import *


import pandas as pd


# show screen in wide mode while launching the app
st.set_page_config(layout="wide")

# styling with css for margin and padding
st.markdown("""
        <style>
               .css-18e3th9 {
                    padding-top: 1rem;
                    padding-bottom: 1rem;
                    padding-left: 1rem;
                    padding-right: 1rem;
                }
        </style>
        """, unsafe_allow_html=True)

# defining a function to read data in minimum time
# @st.cache(allow_output_mutation=True)
def data_read(file):
    return pd.read_csv(file, sep='|', encoding='utf-8')


# main_data = data_read(
#     "D:\\Pet Food Reader\\Streamlit\\Data\\Streamlit\\Data\\data_for_streamlit_reduced_20_07_23.csv")



tabs = ["Introduction", 'Ingredient Analyzer', "Eco Analyzer"]
whitespace = 23
intro, ingredient_analyzer, eco_analyzer = st.tabs(
    [s.center(whitespace, "\u2001") for s in tabs])


#1st page
with intro:
    st.markdown("## What is this App for?")
    st.markdown(
"""
The app does mainly two things:
1. Categorizes ingredients entered by the user of any pet food in simple categories
2. Calculates the environmental impact of the food based on different parameters.

You just have to enter the ingredients in the Ingredient Analyzer section along with the type of food (dry or wet)""")

  
st.markdown("")
st.markdown("")
st.markdown("")

st.markdown("""
*References*:
- *[Environmental impact of diets for dogs and cats](https://www.nature.com/articles/s41598-022-22631-0)*
- *[Greenhouse Gases Equivalencies Calculator - Calculations and References](https://www.epa.gov/energy/greenhouse-gases-equivalencies-calculator-calculations-and-references#miles)*
"""
)


# 2nd page
with ingredient_analyzer:

    space, diet_category_col, space_1, ingredient_col, space_2 = st.columns([0.2, 1, 0.1, 3, 0.2])
    
    with diet_category_col:
        st.markdown('#### Select Food Category:')
        diet_category = st.radio('Selected Category:', [
                                'Dry', 'Wet'], label_visibility='collapsed', horizontal=True)
    
    
    with ingredient_col:
        st.markdown('#### Enter Ingredient List:')
        ing_str = st.text_area('Enter Ingredient List:', height= 220,  label_visibility = 'collapsed', key='ia') 
        
        if ing_str == '':
            st.error('Please enter the ingredient list.')
            ing_str ='.'
            
            
        ing_result = preprocess_ingredients(ing_str)
        # st.write(ing_result)
        
        
    with diet_category_col:
    
        if len(ing_result) != 0:
            
            st.markdown('#### Select Category:')
            selected_p_c = st.radio('Selected Category:', ing_result.keys(), label_visibility = 'collapsed')
            
                
    with ingredient_col:
    
        if len(ing_result) != 0:
        
            if list(ing_result[selected_p_c].values())[0] != '':
                st.markdown('#### Selected category definition:')
                st.markdown(f"###### {list(ing_result[selected_p_c].values())[0]}")
                
            st.markdown('#### Ingredients from selected categories:')
            
            if list(ing_result[selected_p_c].keys())[0] != 'Description':
                st.write(', '.join(list(ing_result[selected_p_c].values())))
            else:
                st.write(', '.join(list(ing_result[selected_p_c].values())[1:]))
                
# 3rd page
with eco_analyzer:
    
    space_1, ingredient_text_col, space_2, ingredients_res_col = st.columns([0.1, 1, 0.1, 0.6])
    
    with ingredient_text_col:
        
        st.markdown('#### Your Ingredient Panel:')
        ing_str_2 = ing_str
        st.markdown(ing_str_2)
        # st.text_area('Enter Ingredient List:', height= 220,  label_visibility = 'collapsed', key ='dfa') 
        
    with ingredients_res_col:
        
        dfa_result_1 = co2_emissions_from_ingredients(ing_str_2, diet_category)
        
        if len(dfa_result_1) > 1:
            
            st.markdown('#### Major Emitters:')
            st.markdown(f"###### {', '.join(dfa_result_1['highlighting_ingredients'])}")
            
    with ingredient_text_col:
        
        st.markdown('#### Environmental Impact Equivalence:')
        
        progress_bar = st.progress(0.0)
        
        if len(dfa_result_1) > 1:
        
            for i in range(threshold_of_ingredient_dict[diet_category][1]):
                
                progress_bar.progress(dfa_result_1['co2_emission_from_ingredients_per_day'] /threshold_of_ingredient_dict[diet_category][1])
                
            st.markdown(f"###### This is equivalant to {dfa_result_1['miles']} miles driven by an average gasoline passenger vehicle\n")
            
    with ingredients_res_col:
        
        if len(dfa_result_1) > 1:
            st.markdown('### CO2 emission in kg (for a typical pet dog):')   
            # st.markdown(f"###### Daily threshold: {threshold_of_ingredient_dict[diet_category][1]} kg")
            # st.markdown(f"Daily CO2 emission of the product if consumed by a typical 10 kg dog:")
            st.markdown(f"#### Daily Emissions: {dfa_result_1['co2_emission_from_ingredients_per_day']} kg")
            # st.markdown("")
            # st.markdown(f"Yearly CO2 emission of the product if consumed by a typical 10 kg dog:\n")
            st.markdown(f"#### Yearly Emissions: {dfa_result_1['co2_emission_from_ingredients_per_year']} kg")
