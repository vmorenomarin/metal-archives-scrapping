#!/usr/bin/env python3

#author:  Víctor Moreno Marín
#e-mail: vmorenomarin@gmail.com

class bandInfo(object):
    
    def __init__(self, bandname, content):
    
        self.bandname = bandname
        self.content = content

    def bandstats(self):

        stats=[self.bandname]
        for i in range(9):
            item=self.content.findAll('dd')[i].text.replace("\t","").replace("\n","").strip()
            stats.append(item)    
        comment=self.content.find('div',{'class':'band_comment'}).text.replace('\n',"").replace('\t',"").replace('\r',"").strip()
        cols=["Band name","Country","Location","Status","Formed in","Genre","Lyrical themes","Curret label","Years active","Comment"]
        info=pd.DataFrame([stats],index=["Info"],columns=cols)
        
        return info
    
    def currentmembers(self):
        number_currents=len(self.content.find(id='band_tab_members_current').findAll('tr', {"class":'lineupRow'}))

        current_list=[]
        for i in range(number_currents):
            item=self.content.find(id='band_tab_members_current').findAll('tr', {"class":"lineupRow"})[i]
            member=[]
            for j in range(0,2):
                member.append(item.findAll('td')[j].text.replace("\n","").replace("\t","").replace("\xa0"," "))

            a=item.find_next_sibling('tr').text
            if re.search("See also:",a) :
                    member.append(item.findNext('tr',{"class":'lineupBandsRow'}).text.replace("\n","").replace("\t","").replace("\xa0"," "))
            else:
                member.append("")    
            current_list.append(member)

        cols=["Name (or alias)", "Band rol", "Other bands"]
        current_lineup=pd.DataFrame(current_list, index=range(1,number_currents+1), columns=cols)
        pd.set_option('display.max_colwidth', -1)
        
        return current_lineup
    
    def pastmembers(self):
        number_past=len(self.content.find(id='band_tab_members_past').findAll('tr', {"class":'lineupRow'}))

        past_list=[]
        for i in range(number_past):
            item=self.content.find(id='band_tab_members_past').findAll('tr', {"class":"lineupRow"})[i]
            member=[]
            for j in range(0,2):
                member.append(item.findAll('td')[j].text.replace("\n","").replace("\t","").replace("\xa0"," "))

            #a=item.find_next_sibling('tr').text
            if item.find_next_sibling('tr') and re.search("See also:",item.find_next_sibling('tr').text) :
                    member.append(item.findNext('tr', {"class":'lineupBandsRow'}).text.replace("\n","").replace("\t","").replace("\xa0"," "))
            else:
                member.append("")    
            past_list.append(member)
            
        cols=["Name (or alias)", "Band rol", "Other bands"]
        past_lineup=pd.DataFrame(past_list, index=range(1,number_past+1), columns=cols)
        pd.set_option('display.max_colwidth', -1)
        
        return past_lineup  
    
    def banddisco(self):
        
        bandId=self.content.findAll('script')[4].text.split("bandId = ")[1].split(";")[0]
        
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
        pd.set_option('display.max_colwidth', -1)
        
        return discography
        
                