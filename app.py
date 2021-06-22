#!/usr/bin/env python
# coding: utf-8

# In[18]:


import pandas as pd
import difflib
import flask
import csv
from flask import Flask, render_template, request
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import sigmoid_kernel


app = flask.Flask(__name__, template_folder='templates')
data=pd.read_csv("youtube.csv")

data = data.reset_index()
indices=pd.Series(data.index,index=data['Title'])
all_titles = [data['Title'][i] for i in range(len(data['Title']))]

tfv=TfidfVectorizer(min_df=3,max_features=None,ngram_range=(1,3))
tfv_matrix=tfv.fit_transform(data['corpus'])
sig2 = sigmoid_kernel(tfv_matrix,tfv_matrix)




def rec_tit(title):
    sig = sigmoid_kernel(tfv_matrix,tfv_matrix)
    idx=indices[title]
    sig_scores=list(enumerate(sig[idx]))
    #sortbased on sigmoid values
    sig_scores=sorted(sig_scores,key=lambda x :x[1],reverse=True)
    
    sig_scores=sig_scores[0:11]
    
    title_indices=[i[0] for i in sig_scores]
    
    Video_tit=data['Title'].iloc[title_indices]
    tumb=data['Tumbnails'].iloc[title_indices]
    score=data['Custom_score'].iloc[title_indices]
    Url=data['VideoURL'].iloc[title_indices]
    views=data['Views'].iloc[title_indices]
    likes=data['Likes'].iloc[title_indices]
    dislike=data['Dislike'].iloc[title_indices]        
    rec_df=pd.DataFrame({'VIdeo':Video_tit,'Tumbnails':tumb,'Score':score,'Video_url':Url,
                        'View':views,'Likes':likes,'Dislike':dislike})
    return rec_df
    
        
            
def get_suggestions():
    df2 = pd.read_csv('youtube.csv')
    #df2=df2.sort_values('Custom_score',ascending=False)
    return list(df2['Title'])

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    suggestions = get_suggestions()
    return flask.render_template('home.html',suggestions=suggestions)

@app.route('/positive', methods=['GET', 'POST'])
def main():
    if flask.request.method == 'GET':
        return(flask.render_template('home.html'))

    if flask.request.method == 'POST':
        m_name = flask.request.form['title_name']
        #m_name = m_name.title()
        
    title1=0   
    count=data['Title'].str.contains(m_name,case=False).sum()
    if count == 0:
         return(flask.render_template('negative.html',name=m_name))
    else:
        rec=data['Title'].loc[data["Title"].str.contains(m_name,case=False)][:1]
        for ele in rec.values:
            title1=ele
            result_final = rec_tit(title1)
            title = []
            tumbn = []
            c_score=[]
            v_url=[]
            vw = []
            lk = []
            dl= []
            for i in range(len(result_final)):
                title.append(result_final.iloc[i][0])
                tumbn.append(result_final.iloc[i][1])
                c_score.append(result_final.iloc[i][2])
                v_url.append(result_final.iloc[i][3])
                vw.append(result_final.iloc[i][4])
                lk.append(result_final.iloc[i][5])
                dl.append(result_final.iloc[i][6])
            suggestions = get_suggestions() 
            return flask.render_template('positive.html',Title=title,tumbnail=tumbn,custom_score=c_score,V_Url=v_url,
                                         Views=vw,Likes=lk,Dislike=dl,search_name=m_name)
    
        if m_name not in all_titles:
            return(flask.render_template('negative.html',name=m_name))
        else:
            #with open('VideoR.csv', 'a',newline='') as csv_file:
                #fieldnames = ['Videos']
                #writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                #writer.writerow({'Videos': m_name})
            result_final = rec_tit(m_name)
            title = []
            tumbn = []
            c_score=[]
            v_url=[]
            vw = []
            lk = []
            dl= []
            for i in range(len(result_final)):
                title.append(result_final.iloc[i][0])
                tumbn.append(result_final.iloc[i][1])
                c_score.append(result_final.iloc[i][2])
                v_url.append(result_final.iloc[i][3])
                vw.append(result_final.iloc[i][4])
                lk.append(result_final.iloc[i][5])
                dl.append(result_final.iloc[i][6])
            suggestions = get_suggestions() 
            return flask.render_template('positive.html',Title=title,tumbnail=tumbn,custom_score=c_score,V_Url=v_url,
                                         Views=vw,Likes=lk,Dislike=dl,search_name=m_name)


if __name__ == '__main__':
    app.run()


# In[ ]:




