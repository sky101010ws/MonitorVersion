from urllib.request import urlopen
from html.parser import HTMLParser
import urllib.parse

class ParseVersion(HTMLParser):
    tag1 = ''
    old_version=''
    info=[]
    is_tag1=False

    def __init__(self):
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        if tag == self.tag1:
            self.is_tag1=True

    def handle_endtag(self, tag):
        if tag == self.tag1:
            self.is_tag1=False
            

class ParseUbuntuVersion(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.info=[]
        self.is_h2=False
        self.old_version='Ubuntu 15.10'

    def handle_starttag(self, tag, attrs):
        if tag == 'h2':
            self.is_h2=True
            
    def handle_endtag(self,tag):
        if tag == 'h2':
            self.is_h2=False
        
    def handle_data(self, text):
        if self.is_h2:
            t=text.strip()
            if len(t) > 0 and t.find('Ubuntu') == 0:
                self.info.append(t)

    def get_version(self):
        if len(self.info) > 1:
            if(self.info[1] != self.old_version):
                return "Old="+self.old_version+",New="+self.info[1]
            else:
                return self.info[1]


class ParseGCCVersion(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.info=[]
        self.is_dt=False
        self.count=0
        self.old_version='GCC 5.3 [2015-12-04]'

    def handle_starttag(self, tag, attrs):
        if tag == 'dt':
            self.is_dt=True
            
    def handle_endtag(self,tag):
        if tag == 'dt':
            self.is_dt=False
        
    def handle_data(self, text):
        if self.is_dt:
            t=text.strip()
            if len(t) > 0 and self.count < 15:
                self.info.append(t)
                self.count +=1

    def get_version(self):
        if len(self.info) > 2:
            if(self.info[0] + " " + self.info[2] != self.old_version):
                return "Old="+self.old_version+",New="+self.info[0] + " " + self.info[2];
            else:
                return self.info[0] + " " + self.info[2]
    

class ParseCentOSVersion(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.info=[]
        self.count=0
        self.old_version='CentOS-7-x86_64-DVD-1511'

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (name,value) in attrs:
                if name=='href' and self.count < 3 and value.find('http://isoredirect.centos.org') == 0:
                    self.info.append(value)
                    self.count+=1

    def get_version(self):
        if len(self.info) > 0:
            items=self.info[0].split('/')
            ver=items[len(items) - 1]
            ver=ver.replace(".iso",'')
            if(ver != self.old_version):
                return "Old="+self.old_version+",New="+ver;
            else:
                return ver


class ParseLDVersion(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.info=[]
        self.count=0

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (name,value) in attrs:
                if name=='href' and self.count < 3 and value.find('http://isoredirect.centos.org') == 0:
                    self.info.append(value)
                    self.count+=1

    def get_version(self):
        if len(self.info) > 0:
            if(self.info[0] != self.old_version):
                return "Old="+self.old_version+",New="+self.info[0];
            else:
                return self.info[0]


class ParsePythonVersion(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.info=[]
        self.is_a=False
        self.count=0
        self.old_version='Python 3.5.1'

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            self.is_a=True
            
    def handle_endtag(self,tag):
        if tag == 'a':
            self.is_a=False
        
    def handle_data(self, text):
        if self.is_a:
            t=text.strip()
            if len(t) > 0 and self.count < 2 and t.find('Download Python') == 0:
                self.info.append(t.replace('Download ',''))
                self.count +=1

    def get_version(self):
        if len(self.info) > 0:
            if(self.info[0] != self.old_version):
                return "Old="+self.old_version+",New="+self.info[0];
            else:
                return self.info[0]


class ParseBandwagonhostVersion(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.info=[]
        self.is_td=False
        self.count=0
        self.old_version='$19.99 USD Annually'

    def handle_starttag(self, tag, attrs):
        if tag == 'td':
            self.is_td=True
            
    def handle_endtag(self,tag):
        if tag == 'td':
            self.is_td=False
        
    def handle_data(self, text):
        if self.is_td:
            t=text.strip()
            if len(t) > 0 and self.count < 2 and t.find('USD Annually') > 0:
              self.info.append(t)
              self.count +=1

    def get_version(self):
        if len(self.info) > 0:
            if(self.info[0] != self.old_version):
                return "Old="+self.old_version+",New="+self.info[0];
            else:
                return self.info[0]

class ParseGDBVersion(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.info=[]
        self.is_td=False
        self.count=0
        self.old_version='gdb-7.10.1 2015-12-05 10:40'

    def handle_starttag(self, tag, attrs):
        if tag == 'td':
            self.is_td=True
            
    def handle_endtag(self,tag):
        if tag == 'td':
            self.is_td=False
        
    def handle_data(self, text):
        if self.is_td:
            t=text.strip()
            if len(t) > 0 and self.count < 4:
                self.count +=1
                self.info.append(t)

    def get_version(self):
        if len(self.info) > 3:
            ver = self.info[2]
            ver = ver[0:ver.find('.tar.')] + " " + self.info[3]
            
            if(ver != self.old_version):
                return "Old="+self.old_version+",New="+ver;
            else:
                return ver

class ParseRARVersion(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.info=[]
        self.is_b=False
        self.count=0
        self.old_version='WinRAR and RAR 5.31 beta version'

    def handle_starttag(self, tag, attrs):
        if tag == 'b':
            self.is_b=True
            
    def handle_endtag(self,tag):
        if tag == 'b':
            self.is_b=False
        
    def handle_data(self, text):
        if self.is_b:
            t=text.strip()
            if len(t) > 0 and self.count < 4:
                self.count +=1
                self.info.append(t)

    def get_version(self):
        if len(self.info) > 0:
            ver = self.info[0]
            if(ver != self.old_version):
                return "Old="+self.old_version+",New="+ver;
            else:
                return ver


class ParseLAODVersion(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.info=[]
        self.is_h2=False
        self.count=0
        self.old_version='HOST 2016-01-31'

    def handle_starttag(self, tag, attrs):
        if tag == 'h2':
            self.is_h2=True
            
    def handle_endtag(self,tag):
        if tag == 'h2':
            self.is_h2=False
        
    def handle_data(self, text):
        if self.is_h2:
            t=text.strip()
            if len(t) > 0 and self.count < 4 and t.find('2016 Google hosts 持续更新') == 0:
                self.count +=1
                self.info.append("HOST "+t[27:37])

    def get_version(self):
        if len(self.info) > 0:
            ver = self.info[0]
            if(ver != self.old_version):
                return "Old="+self.old_version+",New="+ver;
            else:
                return ver


class ParseFirefoxVersion(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.info=[]
        self.is_h2=False
        self.is_a=False
        self.count=0
        self.old_version='HOST 2016-01-31'

    def handle_starttag(self, tag, attrs):
        if tag == 'th':
            self.is_h2=True

        if tag == 'a':
            self.is_a=False
            
    def handle_endtag(self,tag):
        if tag == 'th':
            self.is_h2=False

        if tag == 'a':
            self.is_a=False
        
    def handle_data(self, text):
        if self.is_h2:
            t=text.strip()
            if len(t) > 0:
                self.count +=1
                self.info.append(t)

    def get_version(self):
        if len(self.info) > 0:
            ver = self.info[0]
            if(ver != self.old_version):
                return "Old="+self.old_version+",New="+ver;
            else:
                return ver
            
    
urlDict = {'Ubuntu':['http://www.ubuntu.com/download/desktop',ParseUbuntuVersion(),'utf-8'],
           'CentOS':['https://www.centos.org/download/',ParseCentOSVersion(),'utf-8'],
           'GCC':['https://gcc.gnu.org/',ParseGCCVersion(),'utf-8'],
           'LD':['http://laod.cn/hosts/',ParseLAODVersion(),'utf-8'],
           'Python':['https://www.python.org/downloads/',ParsePythonVersion(),'utf-8'],
           'bandwagonhost':['https://bandwagonhost.com/cart.php?a=confproduct&i=0',ParseBandwagonhostVersion(),'utf-8'],
           'gdb':['http://ftp.gnu.org/gnu/gdb/?C=M;O=D',ParseGDBVersion(),'utf-8'],
           'rar':['http://www.rarsoft.com/',ParseRARVersion(),'utf-8']}
'''
for key in urlDict:
    if urlDict[key][1]:
        text=urlopen(urlDict[key][0]).read()
        urlDict[key][1].feed(text.decode(urlDict[key][2]))
        urlDict[key][1].close()
        print(urlDict[key][1].get_version())
'''
url='https://www.mozilla.org/en-US/firefox/all/'

text=urlopen(url).read()
#print(text.decode("utf-8"))
tp=ParseFirefoxVersion()
tp.feed(text.decode("utf-8"))
tp.close()
print(tp.info)

print(tp.get_version())

