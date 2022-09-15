from flask import Flask, render_template, json, request
from app.api import get_json_response
from app.constants import results_per_page

app = Flask(__name__, static_url_path='/static')

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
  header = render_template('header.html')
  return render_template(
    'article.html',
    header=header,
  )

# Catchall 404 for unknown routes
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
  return '404'

app.run(host='0.0.0.0', port=81)