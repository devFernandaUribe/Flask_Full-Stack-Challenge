import os
from flask import current_app as app
from app.helpers import get_json_from_file
from app.constants import results_per_page

def get_json_response(label = None, page = 1, **kwargs):
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
