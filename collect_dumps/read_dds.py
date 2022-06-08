
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


if len(DDSPath) != len(EPN):
    ReadingError = True

if ReadingError:
    print('THERE ARE ERRORS. EXIT.')
    exit()

        
DirCreated = os.path.isdir('/tmp/epnlog/'+outputdir+'/')
if DirCreated:
    print('DIRECTORY ALREADY EXISTS')
    print('REMOVE IT WITH')
    print('ssh epnlog@epn'+EPN[0]+' remove '+outputdir)
    print('OR CREATE A NEW ONE WITH A DIFFERENT NAME. EXIT.')
    exit()

print('--> RUNNING FAKE COMMAND TO CREATE DIRECTORY')
os.system('ssh epnlog@epn'+EPN[0]+' cp '+DDSPath[0]+'version '+outputdir)
DirCreated = os.path.isdir('/tmp/epnlog/'+outputdir+'/')
if not DirCreated:
    print('DIRECTORY NOT CREATED. EXIT')
    exit()
else:
    print('DIRECTORY /tmp/epnlog/'+outputdir+' CREATED')


for i in range(len(EPN)):
    os.system('ssh epnlog@epn'+EPN[i]+' cp '+DDSPath[i]+'its-stf-decoder*_out.log '+outputdir+'/epn'+EPN[i])
    loglist = os.listdir('/tmp/epnlog/'+outputdir+'/epn'+EPN[i])
    if len(loglist)>0:
        print('EPN '+EPN[i]+': '+str(len(loglist))+' LOG FILES')
    else:
        print('EPN '+EPN[i]+': NO (!!) LOG FILES. REMOVING IT.')
        os.system('ssh epnlog@epn'+EPN[i]+' remove '+outputdir+'/epn'+EPN[i])


infile.close()
        
               

