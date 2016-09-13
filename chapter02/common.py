import urllib2
import urlparse

def download1(url):
    return urllib2.urlopen(url).read()


def download2(url):
    print 'Download:',url
    try:
        html=urllib2.urlopen(url).read()
    except urllib2.URLError as e:
        print 'Download error:',e.reason
        html=None
    return html

def download3(url,num_retries=2):
    print 'Downloading:',url
    try:
        html=urllib2.urlopen(url).read()
    except urllib2.URLError as e:
        print 'Download error:',e.reason
        html=None
        if num_retries>0:
            if hasattr(e,'code') and 500<=e.code<600:
                html=download3(url,num_retries)
    return html

def download4(url,user_agent='wswp',num_retries=2):
    print 'Downloading:',url
    headers={'User-agent':user_agent}
    request=urllib2.Request(url,headers=headers)
    try:
        html=urllib2.urlopen(url).read()
    except urllib2.URLError as e:
        print 'Download error:',e.reason
        html=None
        if num_retries>0:
            if hasattr(e,'code') and 500<=e.code<600:
                html= download4(url,user_agent,num_retries)
    return html
 
def download5(url,user_agent='wswp',proxy=None,num_retries=2):
    print 'Downloading:',url
    headers={'User-agent':user_agent}
    request=urllib2.Request(url,headers=headers)
    opener=urllib2.build_opener()
    if proxy:
        proxy_params={urlparse.urlparse(url).scheme:proxy}
        opener.add_handler(urllib2.ProxyHandler(proxy_params))
    try:
        html=urllib2.urlopen(url).read()
    except urllib2.URLError as e:
        print 'Download error:',e.reason
        html=None
        if num_retries>0:
            if hasattr(0,'code') and 500<=e.code<600:
                html=download5(url,user_agent,proxy,num_retries)
    return html

download=download5
if __name__=='__main__':
    url='http://www.baidu.com'
    print download(url)
  

