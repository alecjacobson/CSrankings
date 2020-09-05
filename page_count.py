import json
import numpy as np
import scipy.io as sio

# s/sa year pagecount
M = np.empty((0,3), int)

with open('articles.json') as json_file:
  data = json.load(json_file)
  for d in data:
    if d['conf'] == 'SIGGRAPH' or d['conf'] == 'SIGGRAPH Asia':
      ssa = 0 if d['conf'] == 'SIGGRAPH' else 0.5
      pc = d['pageCount']
      y = d['year']
      M = M = np.vstack((M,np.array([ssa,y,pc])))
    if np.size(M,0) % 100:
      print('Processed: ',np.size(M,0))

sio.savemat('siggraph-pagecount.mat',{'M':M})
