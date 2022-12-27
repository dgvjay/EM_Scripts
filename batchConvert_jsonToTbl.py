#! /usr/bin/env/python
from EMAN2 import *
import os
import sys
import getopt
import argparse


parser=argparse.ArgumentParser(description='''Will batch read all EMAN2's json file (they should have boxes_3d in them) in the input directory (-d with \ end) and read the coordinates from it and convert it into Dynamo's .tbl (which can be converted into .star using Alister Burt's dynamo2m. Example: batchConvert_jsonToTbl.py -j /data/info/''', epilog="""For questions, contact at digvijay.in1 at gmail.com.""")

requiredNamed = parser.add_argument_group('Required arguments')
requiredNamed.add_argument('-j', '--json_directory', help='Directory containing info files you want converted into .tbls', required=True)
args=parser.parse_args()

opts, args = getopt.gnu_getopt(sys.argv[1:], 'j:',
                               ['json_directory' ])
for opt, arg in opts:
 if opt in ('-j', '--json_directory'):
  json_directory = arg
  

for file in glob.glob(json_directory + "*_info.json"):
 if file.endswith("_info.json"):
  db=js_open_dict(file)
  x=[]
  y=[]
  z=[]
  if db["boxes_3d"]:
   for box in db["boxes_3d"]:
    x.append((box[0]))
    y.append((box[1]))
    z.append((box[2]))
   if x:
    textfile = open(file+'.tbl', "w")
    TBL=zip([i * 0 for i in x],[i * 0 for i in x],[i * 0 for i in x],[i * 0 for i in x],[i * 0 for i in x],[i * 0 for i in x],[i * 0 for i in x],[i * 0 for i in x],[i * 0 for i in x],[i * 0 for i in x],[i * 0 for i in x],[i * 0 for i in x],[i * 0 for i in x],[i * 0 for i in x],[i * 0 for i in x],[i * 0 for i in x],[i * 0 for i in x],[i * 0 for i in x],[i * 0 for i in x],[i * 0 for i in x],[i * 0 for i in x],[i * 0 for i in x],[i * 0 for i in x],x,y,z,[i * 0 for i in x],[i * 0 for i in x],[i * 0 for i in x],[i * 0 for i in x],[i * 0 for i in x],[i * 0 for i in x],[i * 0 for i in x],[i * 0 for i in x],[i * 0 for i in x],[i * 0 for i in x],[i * 0 for i in x],[i * 0 for i in x],[i * 0 for i in x],[i * 0 for i in x],[i * 0 for i in x],[i * 0 for i in x],[i * 0 for i in x],[i * 0 for i in x],[i * 0 for i in x])
    for row in TBL:
     textfile.write(' '.join(str(s) for s in row)+ '\n')
    textfile.close()
    print("Wrote: "+file+'.tbl')
   
  

