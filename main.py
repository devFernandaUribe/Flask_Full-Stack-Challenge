# from urllib import response
from flask import Flask, Response, render_template, json, request, make_response,redirect, session
from flask_session import Session

from app.api import get_json_response, get_selected_article, update_recommend_articles
from app.constants import results_per_page

app = Flask(__name__, static_url_path='/static')
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def save_preferences(path):
  
  criteria=['categories','authors','type']
  # article=get_selected_article(path,label='trending')
  # type='trending'
  # if(article=='NN'):
  article=get_selected_article(path)
  type=article['web_tag']

  category = article['category']
  authors = article['authors'][0]['username']
  single_article_info={'categories':category,'authors': authors,'type':type}
  
  if not session.get("user_preferences",False): 
    session["user_preferences"] = {}
 
  for item in criteria:  
    if not session["user_preferences"].get(item,False): 
      session["user_preferences"][item] = {}
    session["user_preferences"][item][single_article_info[item]] = session["user_preferences"][item].get(single_article_info[item],0) + 1

  update_recommend_articles(path)
  # print(session)

# Default, task description
@app.route('/')
def index():
 
  header = render_template('header.html')
  return render_template('index.html', header=header)

# Feed page
@app.route("/feed", strict_slashes=False)
def feed():
  header = render_template('header.html')
  return render_template(
    'feed.html',
    header=header,
    wireframes=results_per_page,
  )

# API routes
@app.route('/api/<label>', strict_slashes=False)
def api(label):
  
  page = request.args.get('p', default = 1, type = int)
  data = get_json_response(
    label=label,
    page=page,
  )
  return app.response_class(
    response=json.dumps(data),
    status=200,
    mimetype='application/json'
  )

# Article page
@app.route("/article/<path:path>", strict_slashes=False)
def article(path):
  save_preferences(path)

  header = render_template('header.html')
  response=make_response(render_template(
    'article.html',
    header=header,
  ))
  return response

# Catchall 404 for unknown routes
@app.route('/', defaults={'path': ''})

@app.route('/<path:path>')
def catch_all(path):
  return '404'

app.run(host='0.0.0.0', port=81)

