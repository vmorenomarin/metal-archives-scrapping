#!/usr/bin/python3
# -*- coding: utf-8 -*-

#author:  Víctor Moreno Marín
#email: vmorenomarin@gmail.com

#Importing libraries
import bs4
import urllib
import pandas as pd
import numpy as np
from sys import exit
from funcs import *
from class_ma import *
import warnings 
import re

warnings.filterwarnings('ignore')

"""
Abbreviations 
- bn: band name

"""
category = menu()
id = input("Write word for {0}: ".format(category))

if ' ' in id:
    id=id.replace(' ',"_")
    
ids = (id,category)
url = "https://www.metal-archives.com/{1}/{0}".format(ids[0],ids[1])

site = urllib.request.urlopen(url).read()
content = bs4.BeautifulSoup(site)
content_p = content.prettify

#Band statistics

bandId=content.findAll('script')[4].text.split("bandId = ")[1].split(";")[0]
bn = content.div.h1.text
co = content.findAll('dd')[0].text
lo = content.findAll('dd')[1].text
st = content.findAll('dd')[2].text
fo = content.findAll('dd')[3].text
ge = content.findAll('dd')[4].text
th = content.findAll('dd')[5].text
la = content.findAll('dd')[6].text
ya = content.findAll('dd')[7].text.replace("\t","").replace("\n","").replace(" ","").strip()

file_gen(id,content_p)

stats=[bn,co,lo,st,fo,ge,th,la,ya]

cols=["Band name","Country","Location","Status","Formed in","Genre","Lyrical themes","Curret label","Years active"]
info=pd.DataFrame([stats],index=["Info"],columns=cols)
info

#Band discography

url_disc='https://www.metal-archives.com/band/discography/id/{0}/tab/all'.format(bandId)
discog=urllib.request.urlopen(url_disc).read()

disc_content=bs4.BeautifulSoup(discog)

list_album=disc_content.tbody.findAll('tr')
number_album=len(list_album)

list_album=[]

for i in range(number_album):
    disc=disc_content.tbody.findAll('tr')[i]
    album=[]
    for j in range(0,3):
        album.append(disc.findAll('td')[j].text)
    list_album.append(album)

cols=['Name','Type','Year']    
discography = pd.DataFrame(list_album, index=range(1,number_album+1), columns=cols)

discography

# Band members

#currents
number_currents=len(content.find(id='band_tab_members_current').findAll('tr', {"class":'lineupRow'}))

member_current=content.find(id='band_tab_members_current').tr.findAll('td')[0].text.replace("\n","").replace("\t","")
member_rol=content.find(id='band_tab_members_current').tr.findAll('td')[1].text.replace("\n","").replace("\t","")
member_other_bands=content.find(id='band_tab_members_current').findAll('tr', {"class":'lineupBandsRow'})[1].text.replace("\n","").replace("\t","")

current_list=[]
for i in range(number_currents):
    item=content.find(id='band_tab_members_current').findAll('tr', {"class":"lineupRow"})[i]
    member=[]
    for j in range(0,2):
        member.append(item.findAll('td')[j].text.replace("\n","").replace("\t","").replace("\xa0"," "))
    
    a=item.find_next_sibling('tr').text
    if re.search("See also:",a) :
            member.append(content.findAll('tr', {"class":'lineupBandsRow'})[i].find('td').text.replace("\n","").replace("\t","").replace("\xa0"," "))
    else:
        member.append("")    
    current_list.append(member)

pd.set_option('display.max_colwidth', -1)
cols=["Name (or alias)", "Band rol", "Other bands"]
current_lineup=pd.DataFrame(current_list, index=range(1,number_currents+1), columns=cols)
current_lineup