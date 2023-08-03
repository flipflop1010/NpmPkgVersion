import urllib.parse
import requests
from bs4 import BeautifulSoup 



# s='@uuid/types    '
# a=urlEncode(s)
# print(a)

class NpmPkg():
    url='https://www.npmjs.com'

    @staticmethod
    def getPkgVersion(pkg_name:str):
        pkg_url=NpmPkg.url+'/package'
        
        if not pkg_name:
            return 
        pkg_name=pkg_name.strip()
        r=requests.get(pkg_url+'/'+pkg_name)
        html=r.text
        soup=BeautifulSoup(html,'html.parser')
        vers=soup.find_all('p',class_='f2874b88 fw6 mb3 mt2 truncate black-80 f4')
        ver=None
        if len(vers):
            ver=vers[0].text
        return ver




# url='https://www.npmjs.com/package/serverless'

# r=requests.get(url)
# html=r.text
# soup=BeautifulSoup(html,'html.parser')

# ver=soup.find_all('p',class_='f2874b88 fw6 mb3 mt2 truncate black-80 f4')[0]
# print(NpmPkg.getPkgVersion('serverless'))



