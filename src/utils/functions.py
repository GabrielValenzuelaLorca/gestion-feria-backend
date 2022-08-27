def cleanIds(list):
  for element in list:
    element['id'] = str(element.pop('_id'))