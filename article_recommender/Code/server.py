# Launch with
#
# gunicorn -D --threads 4 -b 0.0.0.0:5000 --access-logfile server.log --timeout 60 server:app glove.6B.300d.txt bbc

from flask import Flask, render_template
from doc2vec import *
import sys

app = Flask(__name__)

@app.route("/")
def articles():
    """Show a list of article titles"""
    return render_template("articles.html",articles_links=articles_links)

# article = [filename,title,article_text_minus_title,wordvec]

@app.route("/article/<topic>/<filename>")
def article(topic,filename):
    """
    Show an article with relative path filename. Assumes the BBC structure of
    topic/filename.txt so our URLs follow that.
    """
    
    for i in range(len(articles)):
        if topic+'/'+filename in articles[i][0]:
            article = articles[i]
    title = article[1]
    article_text = article[2].split("\n")
    recommend=recommended(article,articles,5)
    recommend_lst=[]
    for fa in recommend:
        path = fa[0].split("/")[-2:]
        path = '/'.join(path)
        recommend_lst.append([fa[1],f'/article/{path}'])
    return render_template('article.html', title=title, article_text = article_text,recommend_lst=recommend_lst)

i = sys.argv.index('server:app')
glove_filename = sys.argv[i+1]
articles_dirname = sys.argv[i+2]


# gloves = load_glove('glove.6B.300d.txt')
# articles = load_articles('bbc', gloves)
articles_links = [['/article/'+f[0].split('/',1)[1],f[1]] for f in articles]


# app.run()