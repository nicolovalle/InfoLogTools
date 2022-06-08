

import os
import re

maindir = str(sys.argv[1])

maindir = '/tmp/epnlog/'+maindir+'/'

epndirlist = [d for d in os.listdir(maindir) if 'epn' in d and os.path.isdir(os.path.join(maindir,d))]

epndirlist = [maindir+d for d in epndirlist]

print(epndirlist)
