#!/usr/bin/env python

import requests
import urllib.request
import numpy as np
import time
from bs4 import BeautifulSoup
from datetime import datetime as dt


# 'prid=2292', '2296', '2297', '2298', '2300', '2302', '2304', '2307', '2311', '2312', '2317' '2319', '2323', '2325', '2329'
prid = '2362'
url = 'http://publichealth.lacounty.gov/phcommon/public/media/mediapubhpdetail.cfm?prid=' + prid

response = requests.get(url)
print(response)
soup = BeautifulSoup(response.text, features="lxml")
#print(soup)

laData = soup.findAll('ul')
print(len(laData))
#print(soup.findAll('b'))

#nline = len(laData)
#for iline in range(nline):
#    print("the %d line: "%(iline))
#    print(laData[iline])

# get the data for Long Beach and Pasadena
resLbPas = str(laData[0].findAll('li')).split(',')
print(resLbPas)
cityData = []

lbcity = resLbPas[1][5:15]
lbnumb = int(resLbPas[1][19:-7])
pscity = resLbPas[2][5:13]
psnumb = int(resLbPas[2][17:-7])

# Long Beach population: 469450
# Pasadana population: 138101
popu_lb, popu_ps = 469450., 138101.,
rate_lb = float(str(lbnumb / popu_lb * 100000)[0:5])
cityData.append([lbcity, lbnumb, rate_lb])

rate_ps = float(str(psnumb / popu_ps * 100000)[0:5])
cityData.append([pscity, psnumb, rate_ps])
print(cityData)

# get the data of other cities in Los Angeles county  
resultSet = laData[7].findAll('li')
numLine = len(resultSet) - 1 
#for iline in range(1, numLine):
for iline in range(numLine):
    
    #print(str(resultSet[iline]).split('  '))
    ctData = str(resultSet[iline]).split('  ')[1].split('\t')
    #print(iline, ctData)
    #print(iline, ctData[0], ctData[1], ctData[3])

    cityData.append([ctData[0], ctData[1], ctData[3]])

cityData = np.array(cityData)
for idt in range(len(cityData)):
    if cityData[idt, 1] == "--":
        cityData[idt, 1] = "0"
        cityData[idt, 2] = "0"
 
    cityData[idt, 0] = str(cityData[idt, 0]).replace("City of ", "")
    cityData[idt, 0] = str(cityData[idt, 0]).replace("Unincorporated - ", "")
    cityData[idt, 0] = str(cityData[idt, 0]).replace("Los Angeles - ", "")


todate = dt.today()
print(todate.strftime("%y%m%d"))

# save all the data to file
fname = "la_covid19_case_" + todate.strftime("%y%m%d") +".csv"
np.savetxt(fname, cityData, fmt='%s, %s, %s', header='city, number, rate',
           delimiter=', ', newline='\n')


