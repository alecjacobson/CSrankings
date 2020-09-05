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

counter = 0
d = []
confdict = {}

def build_dicts():
    global areadict
    global confdict
    global facultydict
    global aliasdict
    global d
    # Build a dictionary mapping conferences to areas.
    # e.g., confdict['CVPR'] = 'vision'.
    confdict = {}
    venues = []
    for k, v in areadict.items():
        for item in v:
            confdict[item] = k
            venues.append(item)
    facultydict = csv2dict_str_str('faculty-affiliations.csv')
    aliasdict = csv2dict_str_str('dblp-aliases.csv')
    
    # Count and report the total number of faculty in the database.
    totalFaculty = 0
    for name in facultydict:
        # Exclude aliases.
        if name in aliasdict:
            continue
        totalFaculty += 1
    print("Total faculty members currently in the database: "+str(totalFaculty))

def keep_siggraph(_,article):
  global counter
  global d
  global confdict
  global TOG_SIGGRAPH_Volume
  global TOG_SIGGRAPH_Asia_Volume
  counter += 1
  try:
      if counter % 10000 == 0:
          print(len(d))
          print(str(counter)+ " papers processed.")
      if 'booktitle' in article:
          confname = article['booktitle']
      elif 'journal' in article:
          confname = article['journal']
      else:
          return True

      volume = article.get('volume',"0")
      number = article.get('number',"0")
      url    = article.get('url',"")
      year   = int(article.get('year',"-1"))
      pages  = ""
      
      if confname in confdict:
          areaname = confdict[confname]
          if confname == 'ACM Trans. Graph.':
              if year in TOG_SIGGRAPH_Volume:
                  (vol, num) = TOG_SIGGRAPH_Volume[year]
                  if (volume == str(vol)) and (number == str(num)):
                      confname = 'SIGGRAPH'
                      areaname = confdict[confname]
              if year in TOG_SIGGRAPH_Asia_Volume:
                  (vol, num) = TOG_SIGGRAPH_Asia_Volume[year]
                  if (volume == str(vol)) and (number == str(num)):
                      confname = 'SIGGRAPH Asia'
                      areaname = confdict[confname]

      if confname == 'SIGGRAPH' or confname == 'SIGGRAPH Asia':
        d.append(article)
  except TypeError:
      raise
  except:
      print(sys.exc_info()[0])
      raise

  return True

def main():
    global d
    build_dicts()
    gz = gzip.GzipFile('dblp.xml.gz')
    xmltodict.parse(gz, item_depth=2, item_callback=keep_siggraph)
    print(len(d))
    with open('siggraph.xml', 'wb') as result_file:
      result_file.write(xmltodict.unparse({'dblp':{'article':d}}).encode('utf-8'))

if __name__== "__main__":
  main()


#  result_file.write(xmltodict.unparse(doc))
