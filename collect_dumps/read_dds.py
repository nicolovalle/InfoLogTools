
import sys
import re
import os

infilename = str(sys.argv[1])
outputdir = str(sys.argv[2])

infile = open(infilename,'r')
lines = infile.readlines()



ReadingError = False
DDSPath = []
EPN = []

for il in lines:
    try:
        ddspath = re.search('/tmp/wn_dds/.*_epn[0-9]{3}/',il).group(0)
        DDSPath.append(ddspath)
        epn = re.search('_epn[0-9]{3}/',ddspath).group(0).replace('_epn','').replace('/','')
        EPN.append(epn)
        
    except:
        print('ERROR READING ddspath FROM: ',il)
        ReadingError = True


for i in range(len(DDSPath)):
    print(DDSPath[i])
    print(EPN[i])


print('--> RUNNING FAKE COMMAND TO CREATE DIRECTORY')
print('ssh epnlog@epn'+EPN[0]+' cp '+DDSPath[0]+'version '+outputdir)
DirCreated = os.path.exists('/tmp/epnlog/'+outputdir+'/version')
if not DirCreated:
    print('DIRECTORY NOT CREATED. EXIT')
    exit()
else:
    print('DIRECTORY /tmp/epnlog/'+outputdir+' CREATED') 
               


    
    




