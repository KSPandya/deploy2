#importing libraries
import streamlit as st
import streamlit_authenticator as stauth
from streamlit_option_menu import option_menu
import yaml
import sqlite3 
import os
import glob
import pandas as pd
from transformers import pipeline
import random
from serpapi import GoogleSearch
from datetime import date
import streamlit.components.v1 as components
import numpy as np
from auth import *
files = os.listdir("./statistics")
print(files)
files_list = []
for root, directories, files in os.walk("./statistics"):
   for name in files:
      files_list.append(os.path.join(root, name))
print(files_list)
y = 'children'
file_list = glob.glob("./statistics/y*.xlsx")
print(file_list)
from streamlit_elements import elements, mui, html
from st_aggrid import AgGrid

import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import plotly_express as px
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
today = date.today()
import base64

#from google_trans_new import google_translator
#from googletrans import Translator
from googletrans import Translator
translator=Translator()
#trans=Translator()
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'
#translator = google_translator()
st.set_page_config(layout='wide')
from pandas import json_normalize


with open('./config.yaml') as file:
    config = yaml.load(file,Loader=yaml.SafeLoader)
hashed_passwords = stauth.Hasher([]).generate()
@st.experimental_memo
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

#Change path
img_background = get_img_as_base64("./misc/wallpaper.jpg")

#=========================================================
page_bg_img = f"""
<style>

[data-testid="stAppViewContainer"] > .main {{
background-image: url("data:image/jpg;base64,{img_background}");
background-size: 100%;
background-position: top left; /*center*/
 background-repeat: no-repeat;
  background-attachment: fixed;
}}

[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}

[data-testid="stToolbar"] {{
right: 2rem;
}}

[data-testid="stVerticalBlock"] {{
background-color: rgba(0,0,0,0);
}}

</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)
if 'user_id' not in st.session_state:
                            st.session_state['user_id'] = 'user_id'
if 'user_email' not in st.session_state:
                            st.session_state['user_email'] = 'user_email'


########################## LANDING PAGE ##############################################
st.sidebar.image('./bckgrnd.png')

selected = option_menu(None, ["🏠Home", "🙋QnA","📊View Statistics","💻Cybercrimes","📰Read Recent Tweets"], 
        default_index=0,orientation='horizontal')


########################## HOME PAGE ##############################################
if selected == '🏠Home':
    
    st.markdown("<h1 style='text-align: center; color: black;'>Prevention of Cybercrimes against Women and Children</h1>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    selected2 = option_menu(None, ['✅Login','✏️Signup'], 
        #icons=['house', 'cloud-upload'], 
    menu_icon="cast", default_index=0, orientation="horizontal")
    authenticator = stauth.Authenticate(
            config['credentials'],
            config['cookie']['name'],
            config['cookie']['key'],
            config['cookie']['expiry_days'],
            config['preauthorized']
        )

########################## LOGIN ##############################################
    if selected2 == '✅Login':
            with st.sidebar:
   
        
             name, authentication_status, username = authenticator.login('Login', 'main')
            
             if authentication_status:
                authenticator.logout('Logout', 'main')
                st.write(f'Welcome *{name}*')

             elif st.session_state["authentication_status"] == False:
                st.error('Username/password is incorrect')
             elif st.session_state["authentication_status"] == None:
                st.warning('Please enter your username and password')
        
########################## SIGN UP ##############################################
    if selected2 == '✏️Signup':
            if st.session_state["authentication_status"]:
                st.warning("Log out and try again")
            else:
                try:
                    if authenticator.register_user('Register user', preauthorization=False):
                        st.success('User registered successfully')
                except Exception as e:
                    st.error(e)
                with open('./config.yaml', 'w') as file:
                    yaml.dump(config, file, default_flow_style=False)
       

########################## MAKING DATABASE FOR QNA ##############################################
if st.session_state["authentication_status"]:
    def create_table():
            c.execute('CREATE TABLE IF NOT EXISTS blogtable(author TEXT,title TEXT,article TEXT,postdate DATE)')

    def create_qs_table():
            c.execute('CREATE TABLE IF NOT EXISTS qstable(author TEXT,title TEXT,article NVARCHAR,postdate DATE)')

    def add_data(author,title,article,postdate):
            c.execute('INSERT INTO blogtable(author,title,article,postdate) VALUES (?,?,?,?)',(author,title,article,postdate))
            conn.commit() 

    def add_qs_data(author,title,article,postdate):
            c.execute('INSERT INTO qstable(author,title,article,postdate) VALUES (?,?,?,?)',(author,title,article,postdate))
            conn.commit() 

    def view_all_notes():
            c.execute('SELECT * FROM blogtable')
            data = c.fetchall()
            return data


    def view_all_qs():
        c.execute('SELECT * FROM qstable')
        data = c.fetchall()
        return data


    def view_all_titles():
            c.execute('SELECT DISTINCT title FROM blogtable')
            data = c.fetchall()
            return data

    def view_all_auths():
        c.execute('SELECT DISTINCT author FROM blogtable')
        data = c.fetchall()
        return data



    def view_all_qstitles():
            c.execute('SELECT DISTINCT title FROM qstable ORDER BY postdate DESC')
            data = c.fetchall()
            return data

    def get_blog_by_title(title):
            c.execute('SELECT * FROM blogtable WHERE title="{}"'.format(title))
            data = c.fetchall()
            return data

    def get_qs_by_title(title):
            c.execute('SELECT * FROM qstable WHERE title="{}"'.format(title))
            data = c.fetchall()
            return data

    def create_reply_table():
        c.execute('CREATE TABLE IF NOT EXISTS replytable(author TEXT,title TEXT,article NVARCHAR,postdate DATE)')


    def add_reply_data(author,title,article,postdate):
            c.execute('INSERT INTO replytable(author,title,article,postdate) VALUES (?,?,?,?)',(author,title,article,postdate))
            conn.commit() 

    def get_blog_by_author(author):
            c.execute('SELECT * FROM blogtable WHERE author="{}"'.format(author))
            data = c.fetchall()
            return data


    def get_qs_by_author(author):
            c.execute('SELECT * FROM qstable WHERE author="{}"'.format(author))
            data = str(c.fetchall())
            return data

    def get_replies(title):
            c.execute('SELECT * FROM replytable WHERE title="{}"'.format(title))
            data = c.fetchall()
            return data


    def delete_data(title):
            c.execute('DELETE FROM blogtable WHERE title="{}"'.format(title))
            conn.commit()

    def view_all_users():
        c.execute('SELECT * FROM userstable')
        data = c.fetchall()
        return data

    html_temp = """
        <div style="background-color:{};padding:10px;border-radius:10px">
        <h1 style="color:{};text-align:center;">Simple Blog </h1>
        </div>
        """
    title_temp ="""
        <div style="background-color:#00004d;padding:10px;border-radius:10px;margin:10px;">
        <h4 style="color:white;text-align:center;">{}</h1>
        
        <h6>Author:{}</h6>
        <br/>
        <br/> 
        <p style="text-align:justify">{}</p>
        </div>
        """
    article_temp ="""
        <div style="background-color:#00004d;padding:10px;border-radius:5px;margin:10px;box-shadow: 0 15px 60px rgba(0, 0, 0, 0.5);">
        <h4 style="color:white;text-align:center;">{}</h1>

        <h6>Author: {}</h6> 
        <h6>Post Date: {}</h6>
        
        <br/>
        <br/>
        <p style="text-align:justify">{}</p>
        </div>
        """
    head_message_temp ="""
        <div style="padding:10px;border-radius:20px;margin:10px;border:5px;border-color:black;background-color:#f0f0f5;">
        <h4 style="color:black;text-align:center;border:5px;border-color:black;border-radius:20px;">{}</h4>
    
        <h6 style ="color:black;text-align:center;">Author: {}</h6> 
        <h6 style = "color:black;text-align:center;">Post Date: {}</h6> 
        </div>
        
        """
    full_message_temp ="""
        <div style="background-color:#f0f0f5; padding:100px;border-radius:5px;margin:100px;box-shadow: 0 15px 60px rgba(0, 0, 0, 0.5);">
        <p style="text-align:justify;padding:100px">{}</p>
        </div>
        """

    replies_head = """
    <hr>
    <div style = "background-color:#fafafa;padding:10px;border:1px solid black;border-radius:18px;margin:10px;">
    <h6 style ="color:black;text-align:center;">Author:{}</h6> 
    <h6 style = "color:black;text-align:center;">Post Date: {}</h6> 
    <p style="text-align:center;margin:10px;padding:10px;background-color:#fafafa";background-opacity:0.2>{}
    </p>
    </div>
    """
    art= """
    <p style="text-align:center;margin:50px;padding:50px;background-color:#fafafa;background-opacity:0.2;border:2px solid black;border-radius:20px">{}
    </p>
    """
    art_cyb ="""

    <p style="text-align:center;margin:50px;padding:50px;background-color:#fafafa;background-opacity:0.2;border:2px solid black;border-radius:20px;box-shadow:15px 15px 8px gray;">{}
    </p>
    """
    news_temp = """
    <div style="background-color:white;padding:10px;border-radius:5px;margin:10px;border:5px;border-color:black">
    <h4 style="color:black;text-align:center;border:2px solid skyblue; border-radius:5px;">{}</h4>
    </div>
    <hr>
    """
    fetch_news = """
    <div style="background-color:white;padding:10px;border-radius:5px;margin:10px;border:5px;border-color:black">
    <h4 style="color:black;text-align:center;border:2px solid skyblue; border-radius:5px;">{}</h4>
    <h6 style = "color:black;text-align:center;">Post Date: {}</h6> 
    </div>
    <hr>
    """
    new_head="""

    <h5 style="color:black;text-align:center;">{}</h5>
    <hr>
    """

    new_replies="""
    <div>
    <p style="color:black;text-align:center;"><b>Reply</b>:{}
    </p>
    <p style ="color:black;text-align:center;"><b>Author</b>:{}</p> 
    <p style = "color:black;text-align:center;"><b>Post Date</b>: {}</p> 
    </div>
    <hr>
    """
    def html(body):
        st.markdown(body, unsafe_allow_html=True)

    def tryit(a,b):
        return(
            "<style>div.card{position: relative;width: 300px;height: 400px;margin: 0 auto;background: #000;border-radius: 15px;box-shadow: 0 15px 60px rgba(0, 0, 0, 0.5);</style>"
        )

    def card_begin_str(header):
        return (
            "<style>div.card{position: relative;width: 300px;height: 400px;margin: 0 auto;background: #000;border-radius: 15px;box-shadow: 0 15px 60px rgba(0, 0, 0, 0.5);div.face{position: absolute;bottom: 0;left: 0;width: 100%;height: 100%;display: flex;justify-content: center;align-items: center;'};div.face1{box-sizing: border-box;padding: 20px;}h2{margin: 0;padding: 0;}div.java{background-color: #fffc00;-webkit-background-clip: text;-webkit-text-fill-color: transparent;};</style>"
            '<div class="card">'
            '<div class="container">'
            '<div class="face face1">'
            '<div class = "java">'f"{header}"
            # f"<h3><b>{header}</b></h3>"
        )


    def card_end_str():
        return "</div></div>"


    def card(header, body):
        lines = [card_begin_str(header), f"<p>{body}</p>", card_end_str()]
        html("".join(lines))


    def br(n):
        html(n * "<br>")


   
    widget_id = (id for id in range(1, 100000))
    
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
########################## QNA PAGE ##############################################
        
    if selected=='🙋QnA':
    

        
        st.markdown("<h1 style='text-align: center; color: grey;'>QnA</h1>", unsafe_allow_html=True)
    
        with st.sidebar:
            choose = option_menu(None,["✋Ask Question","👀View all Questions"])

        if choose == '✋Ask Question':
            st.markdown("<h4 style='text-align: center; color: grey;'>Ask your question</h4>", unsafe_allow_html=True)
            st.markdown("<hr>",unsafe_allow_html = True)
            create_qs_table()
            blog_title = st.text_input("Enter question")
            #blog_article = st_quill()
            blog_article = st.text_area("Put up the description",height=200)
            d2 = today.strftime("%B %d, %Y")
            if st.button("Add"):
                add_qs_data(st.session_state['username'],blog_title,blog_article,d2)
                st.success("saved")  

    

        if choose == '👀View all Questions':
                                st.markdown("<h4 style='text-align: center; color: grey;'>View all questions</h4>", unsafe_allow_html=True)
                                st.markdown("<hr>",unsafe_allow_html = True)
                                all_titles = [i[0] for i in view_all_qstitles()]
                                #st.write(all_titles)
                                for i in all_titles:
                                    res = get_qs_by_title(i)
                                    #st.write(res)

                                    for j in res:
                                        with st.container():
                                            st.markdown(head_message_temp.format(j[1],j[0],j[3]),unsafe_allow_html=True)
                                            reps = get_replies(j[1])
                                            with st.expander(j[2]):

                                                st.markdown(new_head.format("Replies"),unsafe_allow_html=True)

                                                for k in reps:
                                                    st.markdown(new_replies.format(k[2],k[0],k[3]),unsafe_allow_html=True)
                                                    #reply = st.text_area("Enter your reply",height=200)
                                            if st.checkbox("Reply to this qs",key = next(widget_id)):
                                                create_reply_table()
                                                reply = st.text_area("Enter your reply",height=200)
                                                d2 = today.strftime("%B %d, %Y")
                                                if st.button("Add Reply"):
                                    
                                                    add_reply_data(st.session_state['username'],j[1],reply,d2)
                                                    st.markdown(head_message_temp.format(j[1],st.session_state['username'],d2),unsafe_allow_html=True)
                                                    with st.container():
                                                        st.markdown(art.format(reply),unsafe_allow_html=True)
                                                    st.success("Reply to:{} saved".format(j[1]))

                                        st.markdown("<hr>",unsafe_allow_html = True)
                                            
   
    

########################## VIEWING CYBERCRIME RECORDS ##############################################
    yr = 2017

    print(type(yr))
    print(yr)

    def get_wrecords(yr):
        try:

            print("AAAAAAAAA")
            dir = ".\statistics\women" + "\\"+ str(yr) + "\\"
            print("dirrr",dir)
            file_l = glob.glob(dir + "\*.xlsx" )
            hi = pd.read_excel(file_l[0],index_col=[0],skiprows=[0,1])
            return hi
        except:
            st.error("File has not been updated yet. Please try with different parameters")
            st.stop()
    def get_crecords(yr):
        try:

            print("AAAAAAAAA")
            dir = ".\statistics\children" + "\\"+ str(yr) + "\\"
            print("dirrr",dir)
            file_l = glob.glob(dir + "\*.xlsx" )
            hi = pd.read_excel(file_l[0],index_col=[0],skiprows=[0,1])
            return hi
        except Exception as e:
            st.error("File has not been updated yet. Please try with different parameters")
            st.stop()   

    if selected == '📊View Statistics':
        
        st.markdown("<h1 style='text-align: center; color: grey;'>View Statistics</h1>", unsafe_allow_html=True)
        st.markdown("<hr>",unsafe_allow_html=True)
        chosse = option_menu(None,['Women','Children'],orientation='horizontal')
        if chosse == 'Women':
            #dir = (r'C:\Users\Lenovo\Desktop\Table 9A.10_1.xlsx')
            gg = st.sidebar.slider("Select Year",min_value=2017,max_value=2030,key='myslider')
            # hi = pd.read_excel(dir,index_col=[0],skiprows=[0,1])
            # df = pd.DataFrame(hi)
            ff = get_wrecords(gg)
            df = pd.DataFrame(ff)
            sel_mode = st.sidebar.radio('View Records',options=['single','multiple'],key='myradio')
            gd = GridOptionsBuilder.from_dataframe(df)
            gd.configure_pagination(enabled=True)
            gd.configure_default_column(groupable=True)
            

   
            gd.configure_selection(selection_mode=sel_mode,use_checkbox=True)    
            gridoptions = gd.build()

            data = AgGrid(df,theme='alpine',gridOptions=gridoptions)
                
            selected_rows = data["selected_rows"]
                
            selected_rows = pd.DataFrame(selected_rows)
            

            colls=df.columns.values
            vals=colls[1:]
            
        
            
            c1,c2 = st.columns(2)
            if sel_mode=='multiple':
                        optt=st.sidebar.selectbox('Select Cybercrime',options=vals,key ='mult')
                        if len(selected_rows) != 0:
                            fig = px.bar(selected_rows,'State/UT',color=optt)
                            c1.plotly_chart(fig)
                            fig2 = px.bar(selected_rows,optt,color='State/UT')
                            c2.plotly_chart(fig2)

            if sel_mode == 'single':
                    if len(selected_rows) != 0:
                        fin = []
                        for i in vals:
                            fin.append(int(selected_rows[i].values))
                        
                        fig = px.pie(selected_rows,values=fin,names=vals,width=1000, height=600)
                        st.plotly_chart(fig)

            #st.dataframe(df)
        if chosse == 'Children':
            #dir = (r'C:\Users\Lenovo\Desktop\Table 9A.10_1.xlsx')
            gg = st.sidebar.slider("Select Year",min_value=2017,max_value=2030,key='myslider')
            # hi = pd.read_excel(dir,index_col=[0],skiprows=[0,1])
            # df = pd.DataFrame(hi)
            ff = get_crecords(gg)
            df = pd.DataFrame(ff)
            sel_mode = st.sidebar.radio('View Records',options=['single','multiple'],key='myradio')
            gd = GridOptionsBuilder.from_dataframe(df)
            gd.configure_pagination(enabled=True)
            gd.configure_default_column(groupable=True)
            


            gd.configure_selection(selection_mode=sel_mode,use_checkbox=True)    
            gridoptions = gd.build()

            data = AgGrid(df,theme='alpine',gridOptions=gridoptions)
                
            selected_rows = data["selected_rows"]
                
            selected_rows = pd.DataFrame(selected_rows)
            

            colls=df.columns.values
            vals=colls[1:]
            
        
            
            c1,c2 = st.columns(2)
            if sel_mode=='multiple':
                        optt=st.sidebar.selectbox('Select Cybercrime',options=vals,key ='mult')
                        if len(selected_rows) != 0:
                            fig = px.bar(selected_rows,'State/UT',color=optt)
                            c1.plotly_chart(fig)
                            fig2 = px.bar(selected_rows,optt,color='State/UT')
                            c2.plotly_chart(fig2)

            if sel_mode == 'single':
                    if len(selected_rows) != 0:
                        fin = []
                        for i in vals:
                            fin.append(int(selected_rows[i].values))
                        
                        fig = px.pie(selected_rows,values=fin,names=vals,width=1000, height=600)
                        st.plotly_chart(fig)

    ########################## READ ABOUT CYBERCRIMES ##############################################
    
    @st.cache()
    def return_search(q,num):
        
        summarizer = pipeline("summarization")
        search = GoogleSearch({
        "q": q, 
        "gl":"in",
        "num":num+1,
        "location": "India",
        "api_key": "41b27b8d65ab07bf88da3fb3dd504106f79a307eae068584092258901f9f996c"
    })
        result = search.get_dict()
        organic_results = result["organic_results"]
        #st.write(organic_results)
        df = json_normalize(organic_results)
        #st.write(df)
        #st.write(df.snippet)
        joi = []
        for i in df.snippet:
            joi.append(i.partition('.')[0])
        #st.write(joi)
        joii = ''.join(joi)
        #st.write(joii)
        summary = summarizer(joii,min_length=400)[0]['summary_text']
        #st.write(summary)
    
        return df[['position','title','link','snippet_highlighted_words']],summary,df['link']


    
    if selected == "💻Cybercrimes":
        st.markdown("<h1 style='text-align: center; color: grey;'>Read about Cybercrimes</h1>", unsafe_allow_html=True)
        st.markdown("<hr>",unsafe_allow_html=True)
        with st.sidebar.form(key='cybercrime'):
            sel2= st.selectbox('Select cybercrime',['Cyber Blackmailing','Cyber Pornography','Cyber Stalking','Cyber Defamation','POCSO','Child Grooming','Child Sexual Abuse Material','Sextortion'])
            
            nn = st.slider("Number of articles to show",min_value=5,max_value=15)
            sel1 = st.selectbox('Select the language',['English','Hindi','Bengali','Marathi','Gujarati','Kannada','Tamil','Urdu','Telugu'])
            #sel2 = st.selectbox('Select language',)
            submt = st.form_submit_button("Get")
            p,pp,q = return_search(sel2,nn)
        
        if submt:
                AgGrid(p,fit_columns_on_grid_load=True,theme='alpine')
                
                
                
                if sel1 == 'English':
                    lang = 'en'
                if sel1 == 'Hindi':
                    lang = 'hi'
                if sel1 == 'Bengali':
                    lang = 'bn'
                if sel1 == 'Marathi':
                    lang = 'mr'
                if sel1 == 'Gujarati':
                    lang = 'gu'
                if sel1 == 'Kannada':
                    lang = 'kn'
                if sel1 == 'Telugu':
                    lang = 'te'
                if sel1 == 'Tamil':
                    lang = 'ta'
                if sel1 == 'Urdu':
                    lang = 'ur'
                if sel1 == 'Malayalam':
                    lang = 'ml'

            
    
                
                
                
                m = pp.split('.')
                a = ".".join(m[:-1])
                print(a)
                    
                    
                transl = translator.translate(a,dest=lang)
                st.markdown("<h4 style='text-align: center; color: grey;'>Summary</h4>", unsafe_allow_html=True)
                st.write(art_cyb.format(transl.text),unsafe_allow_html=True)

                c1,c2,c3,c4 = st.columns(4)
                c4.download_button("Download summary as text file",transl.text)
            
                st.markdown("<hr>",unsafe_allow_html=True)
                fig, ax = plt.subplots()

                wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white").generate(a)
                ax.imshow(wordcloud, interpolation='bilinear')
            
                ax.axis("off")
                st.markdown("<h4 style='text-align: center; color: grey;'>Wordcloud</h4>", unsafe_allow_html=True)
                st.pyplot(fig)
                #st.write(trans.translate(pp[:-1],dest=lang))
        

    ########################## TWITTER ##############################################
    
    if selected=='📰Read Recent Tweets':
        st.markdown("<h1 style='text-align: center; color: grey;'>Tweets related to Cybercrimes</h1>", unsafe_allow_html=True)
        st.markdown("<hr>",unsafe_allow_html=True)


        
        
        
        

    
        components.html('<!-- start feedwind code --> <script type="text/javascript" src="https://feed.mikle.com/js/fw-loader.js" preloader-text="Loading" data-fw-param="163705/"></script> <!-- end feedwind code -->',height=600)
        components.html('<!-- start feedwind code --> <script type="text/javascript" src="https://feed.mikle.com/js/fw-loader.js" preloader-text="Loading" data-fw-param="163706/"></script> <!-- end feedwind code -->',height=600)
        components.html('<!-- start feedwind code --> <script type="text/javascript" src="https://feed.mikle.com/js/fw-loader.js" preloader-text="Loading" data-fw-param="163707/"></script> <!-- end feedwind code -->',height=600)
        components.html('<!-- start feedwind code --> <script type="text/javascript" src="https://feed.mikle.com/js/fw-loader.js" preloader-text="Loading" data-fw-param="163708/"></script> <!-- end feedwind code -->',height=600)
        components.html('<!-- start feedwind code --> <script type="text/javascript" src="https://feed.mikle.com/js/fw-loader.js" preloader-text="Loading" data-fw-param="163709/"></script> <!-- end feedwind code -->',height=600)
        components.html('<!-- start feedwind code --> <script type="text/javascript" src="https://feed.mikle.com/js/fw-loader.js" preloader-text="Loading" data-fw-param="163710/"></script> <!-- end feedwind code -->',height=600)
