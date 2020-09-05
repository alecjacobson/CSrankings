import gzip
import xmltodict
import collections
import json
import csv
import re
import sys
import operator
# from typing import Dict
from csrankings import *
import pycurl
from io import BytesIO


# Consider pubs in this range only.
nodois = 0
counter = 0
f = []

def doi_from_ee(ee):
  def doi_from_url(url):
    prefix = "https://doi.org/"
    if url.startswith(prefix):
      return True, url[len(prefix):]
    return False, ""
  if isinstance(ee, list): 
    for url in ee:
      has_doi, doi = doi_from_url(url)
      if has_doi:
        return True, doi
    return False, ""
  else:
    return doi_from_url(ee)

def handle_article(_,article):
  global counter
  global nodois
  global confdict
  global TOG_SIGGRAPH_Volume
  global TOG_SIGGRAPH_Asia_Volume
  global f
  has_doi, doi = doi_from_ee(article['ee'])
  counter += 1
  if counter % 20 == 0:
    print(str(counter)+ " papers processed.")
  year   = int(article.get('year',"-1"))
  volume = article.get('volume',"0")
  number = article.get('number',"0")
  if 'booktitle' in article:
      confname = article['booktitle']
  elif 'journal' in article:
      confname = article['journal']
  else:
      return True
  if confname == 'ACM Trans. Graph.':
      if year in TOG_SIGGRAPH_Volume:
          (vol, num) = TOG_SIGGRAPH_Volume[year]
          if (volume == str(vol)) and (number == str(num)):
              confname = 'SIGGRAPH'
      if year in TOG_SIGGRAPH_Asia_Volume:
          (vol, num) = TOG_SIGGRAPH_Asia_Volume[year]
          if (volume == str(vol)) and (number == str(num)):
              confname = 'SIGGRAPH Asia'
              year += 0.5
  if has_doi:
    crl = pycurl.Curl()
    b_obj = BytesIO()
    crl.setopt(crl.URL, 'api.crossref.org/works/'+doi)
    crl.setopt(crl.WRITEDATA, b_obj)
    crl.perform()
    message = json.loads(b_obj.getvalue())['message']
    page = 0
    refcount = 0
    if 'reference-count' in message:
      refcount = message['reference-count']
    if 'page' in message:
      page = message['page']
      if page.find("-") >= 0:
        first_page = int(page[:page.find("-")])
        last_page = int(page[page.find("-")+1:])
        page = last_page-first_page+1
      else:
        page = int(page)
    if refcount > 1 and page > 1 and year > 0:
      f.write(str(year)+","+str(refcount)+","+str(page)+"\n")
  else:
    nodois += 1
  return True
  

def main():
    global d
    global f
    f = open('siggraph-year-refcount-pagecount.csv', 'w')
    with open('siggraph.xml', 'r') as result_file:
      xmltodict.parse(result_file, item_depth=2, item_callback=handle_article)
    print(str(nodois)+" papers with no doi out of "+str(counter))
    f.close();

if __name__== "__main__":
  main()


#  result_file.write(xmltodict.unparse(doc))
