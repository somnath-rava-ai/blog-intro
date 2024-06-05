import requests
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

def linkedin_latest(linkedin_url, n_days=1):
    days_before = datetime.now() - timedelta(days=n_days)
    def to_nodays(var):
            try:
                num = int(len(var)/2)
                val, scale = int(var[:num]), var[num:]
                if scale =='h':
                    return 0
                elif scale == "d":
                    return val
                elif scale == "w":
                    return val*7
                elif scale == "mo":
                    return val*30
                elif scale == "yr":
                    return val*365
            except : 
                return None

    name = linkedin_url.rstrip('/').split('/')[-1]  
    # headers = {
    #         "content-type": "application/json",
    #     }
    #r_posts = requests.get('http://127.0.0.1:5000/get_data/one', params= {"username":name}, headers=headers)
    #r_comments = requests.get('http://127.0.0.1:5000/get_data/three', params ={"username":name}, headers=headers)

    posts_url = "https://linkedin-api8.p.rapidapi.com/get-profile-posts"
    comments_url = "https://linkedin-api8.p.rapidapi.com/get-profile-comments"
    querystring = {"username":name}

    headers = {
    	#"X-RapidAPI-Key": "dacc93bfecmsh336023176beccabp1fa929jsnbf31d1fec909",
        "x-rapidapi-key": "09d61ce8a3msh24d4486b9ca172fp1976bajsn4db23774373a",
    	"X-RapidAPI-Host": "linkedin-api8.p.rapidapi.com"
    }
    
    r_posts = requests.get(posts_url, headers=headers, params=querystring)
    r_comments = requests.get(comments_url, headers=headers, params=querystring)
    data_posts = pd.DataFrame(r_posts.json()['data'])
    data_comments = pd.DataFrame(r_comments.json()['data'])
    data_comments['postedDaysAgo'] = data_comments['postedAt'].apply(lambda x: to_nodays(x))
    new_posts = data_posts.loc[data_posts['postedDateTimestamp'].apply(lambda x: datetime.fromtimestamp(x/1000)) > days_before]
    new_comments = data_comments.loc[data_comments['postedDaysAgo'] < n_days]

    new_posts_json =[]
    for _,i in new_posts.iterrows():
        time = datetime.fromtimestamp(float(i['postedDateTimestamp'])/1000.0).strftime("%m/%d/%Y, %H:%M")
        is_reposted ='Self Posted'
        if i['reposted'] == True:
            is_reposted = 'Reposted'
        images=[]
        if i['image'] is not np.nan:
            images = i['image']
        try:
            reposts = str(i['repostsCount'])
        except:
            reposts =0
        try:
            reacts = str(i['totalReactionCount'])
        except:
            reacts =0
        try:
            comments = str(i['commentsCount'])
        except:
            comments =0
        new_posts_json.append({
                            "post":i['text'],  "time":time,  "num_reactions":reacts,  "num_comments":comments, 
                            "num_reposts":reposts, "image_url":images,  "postUrl":i['postUrl'],  "is_reposted":is_reposted
                                })
    print(new_posts_json)
    new_comments_json =[]
    print(new_comments)
    for _,i in new_comments.iterrows():
        post_commented_on=i['text']
        print(i["author"])
        try:
            post_commented_on_author = i['author']['firstName'] +' '+ i['author']['lastName']
        except:
            post_commented_on_author = ''
        comment=i['highlightedComments'][0]
        new_comments_json.append({"post_commented_on": post_commented_on, "post_commented_on_author": post_commented_on_author, "comment": comment})


    return {"status":200, "data":{"response":{"new_posts": new_posts_json,"new_comments": new_comments_json}}}