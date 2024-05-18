import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_extras.add_vertical_space import add_vertical_space
from src.analyzer import Analyzer


# Streamlit Configuration Setup
# page configuration
def streamlit_config():
    st.set_page_config(page_title='Resume Analyzer AI', layout="wide")

    # page header transparent color
    page_background_color = """
    <style>

    [data-testid="stHeader"] 
    {
    background: rgba(0,0,0,0);
    }

    </style>
    """
    st.markdown(page_background_color, unsafe_allow_html=True)

    # title and position
    st.markdown(f'<h1 style="text-align: center;">AI-Powered Resume Analyzer</h1>',
                unsafe_allow_html=True)

# Streamlit Configuration Setup
streamlit_config()

with st.sidebar:

    add_vertical_space(1)

    option = option_menu(menu_title='', options=['Analyze'],
                         icons=['house-fill'])

def resume_analyze():

        with st.form(key='Analyze'):

            # User Upload the Resume
            add_vertical_space(1)
            pdf = st.file_uploader(label='Upload Your Resume', type='pdf')
            add_vertical_space(1)

            # Enter OpenAI API Key
            col1,col2 = st.columns([0.6,0.4])
            add_vertical_space(2)

            # Click on Submit Button
            submit = st.form_submit_button(label='Submit')
            add_vertical_space(1)
        
        add_vertical_space(3)
        if submit:
            if pdf is not None:
                try:
                    with st.spinner('Processing...'):
                        analysis = Analyzer.analyze(pdf)
                    
                    st.markdown(f'<h4 style="color: orange;">Analysis:</h4>', unsafe_allow_html=True)
                    st.write(analysis)

                except Exception as e:
                    st.markdown(f'<h5 style="text-align: center;color: orange;">{e}</h5>', unsafe_allow_html=True)

            elif pdf is None:
                st.markdown(f'<h5 style="text-align: center;color: orange;">Please Upload Your Resume</h5>', unsafe_allow_html=True)
                
                
if option == 'Analyze':

    resume_analyze()    