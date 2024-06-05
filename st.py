from app import linkedin_latest
import streamlit as st


site = st.text_input("Enter linkedin URL")
n_days = st.number_input("Enter number of days upto 50", max_value=50, step=1)


if st.button('Run'):
    output = linkedin_latest(site, n_days)
    new_posts = output["data"]["response"]["new_posts"]
    new_comments = output["data"]["response"]["new_comments"]
    posts= '''
New Posts:<br>

'''
    for i in new_posts:
        record = f'''
<div style="border-style:solid; border-color: gainsboro;border-radius: 0px; margin:5px; padding:5px">
Type of post: {i['is_reposted']}<br>
{i['post']}<br><br>
Posted at: {i['time']}<br>
No. of reactions:{i['num_reactions']}   &nbsp; &nbsp;   No. of comments:{i['num_comments']}  &nbsp; &nbsp;     No. of reposts: {i['num_reposts']}<br>
Post URL: <a href="{i['postUrl']}">{i['postUrl']}</a><br>

'''     
        posts = posts + record
        if i['image_url'] != []:
            posts = posts + '<img src="{url}" style="display: block; margin: auto;width: 50%;border-color: gainsboro;border-radius: 0px;">'.format(url = i['image_url'][0]['url'])
        posts=posts+"</div>"
    
    st.html(posts)