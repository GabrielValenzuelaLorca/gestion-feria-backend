def cleanIds(list):
  for element in list:
    element['id'] = str(element['_id'])
    del element['_id']