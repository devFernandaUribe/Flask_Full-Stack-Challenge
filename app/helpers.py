import json

def get_json_from_file(filepath = None, page = 1, **kwargs):
  data = {}
  if filepath:
    try:
      with open(filepath) as test_file:
        data = json.load(test_file)
    except Exception as e:
      print(e) # debug in server logs
  return data
