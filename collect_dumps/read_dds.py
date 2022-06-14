#!/usr/bin/python3

import sys
import re
import os


if len(sys.argv) != 3 or '--help' in sys.argv or '-h' in sys.argv:
    print("""
    Usage:
       %s InfoLogFile.txt DirectoryName

    To be used on the login machine. It will create /tmp/epnlog/DirectoryName/epn***/
    copying in each of the them the decoder logs and eventually the raw dumps.
    """%(sys.argv[0]))
    exit()

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
        os.system('ssh epnlog@epn'+EPN[i]+' cp '+DDSPath[i]+'/slots/*/rawdump_ITS*.raw '+outputdir+'/epn'+EPN[i])
        print('EPN '+EPN[i]+': '+str(len(os.listdir('/tmp/epnlog/'+outputdir+'/epn'+EPN[i]))-len(loglist))+' DUMP RAW FILES')
    else:
        print('EPN '+EPN[i]+': NO (!!) LOG FILES. REMOVING IT.')
        os.system('ssh epnlog@epn'+EPN[i]+' remove '+outputdir+'/epn'+EPN[i])


infile.close()

try:
    runXX = re.search('run[0-9]{6}',outputdir).group(0)
except:
    runXX = 'runXXXXXX'
print("YOU CAN COPY ON epnits0 WITH")
print("ssh valle@epnits0.cern.ch 'mkdir -p /data/nvalle/"+runXX+"/'; scp -r /tmp/epnlog/"+outputdir+"/ valle@epnits0.cern.ch:/data/nvalle/"+runXX+"/.")
print("AND YOU CAN REMOVE DIRECTORY ON login machine WITH")
print("ssh epnlog@epn"+EPN[0]+" remove "+outputdir)


               

