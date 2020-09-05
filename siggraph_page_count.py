import gzip
import xmltodict
import collections
import json
import csv
import re
import sys
import operator

# TOG special handling to count only SIGGRAPH proceedings.
# Assuming all will be in the same issues through 2021.
TOG_SIGGRAPH_Volume = {2021: (40, 4),
                       2020: (39, 4),
                       2019: (38, 4),
                       2018: (37, 4),
                       2017: (36, 4),
                       2016: (35, 4),
                       2015: (34, 4),
                       2014: (33, 4),
                       2013: (32, 4),
                       2012: (31, 4),
                       2011: (30, 4),
                       2010: (29, 4),
                       2009: (28, 3),
                       2008: (27, 3),
                       2007: (26, 3),
                       2006: (25, 3),
                       2005: (24, 3),
                       2004: (23, 3),
                       2003: (22, 3),
                       2002: (21, 3)
                       }


# TOG special handling to count only SIGGRAPH Asia proceedings.
# Assuming all will be in the same issues through 2021.
TOG_SIGGRAPH_Asia_Volume = {2021: (40, 6),
                            2020: (39, 6),
                            2019: (38, 6),
                            2018: (37, 6),
                            2017: (36, 6),
                            2016: (35, 6),
                            2015: (34, 6),
                            2014: (33, 6),
                            2013: (32, 6),
                            2012: (31, 6),
                            2011: (30, 6),
                            2010: (29, 6),
                            2009: (28, 5),
                            2008: (27, 5)
                            }

counter = 0
successes = 0
failures = 0

def do_it():
#    gz = gzip.GzipFile('dblp-original.xml.gz')
    gz = gzip.GzipFile('dblp.xml.gz')
    xmltodict.parse(gz, item_depth=2, item_callback=handle_article)

def handle_article(_, article):
    global counter
    global failures
    global TOG_SIGGRAPH_Volume
    global TOG_SIGGRAPH_Asia_Volume
    counter += 1
    try:
        if counter % 10000 == 0:
            print(str(counter)+ " papers processed.")
        year   = int(article.get('year',"-1"))
        volume = article.get('volume',"0")
        number = article.get('number',"0")
        doi = article.get('ee',"")
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
        if confname == 'SIGGRAPH' or confname == 'SIGGRAPH Asia':
            print(doi)
    except TypeError:
        raise
    except:
        print(sys.exc_info()[0])
        failures += 1
        raise
    return True

def main():
    #build_dicts()
    do_it()
    #dump_it()
    #print("Total papers counted = "+str(totalPapers))

if __name__== "__main__":
  main()
