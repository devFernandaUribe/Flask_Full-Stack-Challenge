import os
from unittest import result
from flask import current_app as app, session
from app.helpers import get_json_from_file
from app.constants import results_per_page

def get_json_response(label = None, page = 1, **kwargs):
  if label=='recommended': 
    data=session['recommended']
    print('session +++++++++++++++',session['user_preferences'])
  else  :
    filepath = os.path.join(app.static_folder, 'json', label + '.json')
    data = get_json_from_file(filepath, page)
  num_per_page = 3
  if label in results_per_page:
    num_per_page = results_per_page[label]
  return filter_by_page(data, page, num_per_page)

def filter_by_page(data = {}, page = 1, num_per_page = 3):
  if 'results' in data:
    first = (page - 1) * num_per_page
    last = first + num_per_page
    return data['results'][first:last]
  return data

def get_selected_article(path, page = 1, **kwargs):
  labels=["trending","latest"]
  selected_article="NN"
  for label in labels:
    filepath = os.path.join(app.static_folder, 'json', label + '.json')
    data = get_json_from_file(filepath, page)
  
    for item in data['results']:
      if(item.get("canonical_path","NN ") == "/"+path):
        selected_article=item 
        selected_article["web_tag"]=label
        break 
  return selected_article

def update_recommend_articles(path, page = 1, **kwargs):
    
  filepathLatest = os.path.join(app.static_folder, 'json', 'latest' + '.json')
  filepathTrending = os.path.join(app.static_folder, 'json', 'trending' + '.json')
  
  dataLatest = asign_score(get_json_from_file(filepathLatest, page),'latest',path)
  dataTrending =asign_score( get_json_from_file(filepathTrending, page),'trending',path)

  data=dataLatest|dataTrending
  data={"results":sorted(data['results'], key=lambda x: x['score'], reverse=True)}
  unique_data={}
  unique_data['results'] =[]

  for item in data['results']:
    if item not in unique_data['results']:
        unique_data['results'].append(item)

  session['recommended'] = unique_data 
  print(session['user_preferences']) 
  
  return data 

def asign_score(data,origin,path):
  criteria=['categories','authors','type']
  if not session.get("user_preferences",False): 
      session["user_preferences"] = {}

  for item in data['results']:
    item['web_tag']=origin
    if(item.get('canonical_path',"NN")!="NN"):
      author=item['authors'][0]['username']
    else:
      author='NN'

    single_article_info={'categories':item.get('category','NN'),'authors': author,'type':origin} 

    if not item.get('score',False):
      item['score']=0

    for points in criteria:
      item['score']+=session["user_preferences"][points].get(single_article_info[points],0)

  return data