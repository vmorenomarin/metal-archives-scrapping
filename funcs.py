#!/usr/bin/env python3

#author:  Víctor Moreno Marín
#email: vmorenomarin@gmail.com

#Importing libraries
import urllib3 
import bs4
import pandas as pd
import numpy as np
from sys import exit


#Menu for input search word and searching category.

def menu():
    print("Search for:")
    opt=None
    while opt not in ("b","a","ar","l","s","e"):
        print("")
        print(" (b)and \n (a)lbum \n (ar)tist \n (l)abel \n (s)ong \n (e)xit \n"  )
        opt=input("Input letter in parenthesis: ")
        if opt=="b":
            category="bands"
        elif opt=="a":
            category="album_title"
        elif opt=="ar":
            category="artists"
        elif opt=="l":
            category="label"  
        elif opt=="s":
            category="song_name"
        elif opt=="e":
            category=None
            print("\n ====================== \n    Go to hell!! \\m/ \n ====================== \n")
            exit()
    return category

#def getDisco(id):
    
def file_gen(id,content_p):
    file=open('{0}.txt'.format(id),'w')
    file.write('{0}'.format(content_p))
    file.close()
    return file

def band_stat(content):

    bandId=content.findAll('script')[4].text.split("bandId = ")[1].split(";")[0]
    bn = content.div.h1.text

    stats=[bn]
    for i in range(8):
        item=content.findAll('dd')[i].text.replace("\t","").replace("\n","").strip()
        stats.append(item)
    
    cols=["Band name","Country","Location","Status","Formed in","Genre","Lyrical themes","Curret label","Years active"]
    info=pd.DataFrame([stats],index=["Info"],columns=cols)
    return stats, bandId, cols