import urllib
import urllib2   
  
url = 'http://physics.nist.gov/cgi-bin/Xcom/xcom3_1-t' 
values = {'ZSym' : 'Fe', 'Energies': 0.01}    

#user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' 
headers = {'User-Agent': 'Googlebot/2.1 (+http://www.google.com/bot.html)',
'Referer':'http://physics.nist.gov/cgi-bin/Xcom/xcom2-t'}
data = urllib.urlencode(values) 

req = urllib2.Request(url, data, headers) 

response = urllib2.urlopen(req)
the_page = response.read()
print the_page 
print response.geturl()

