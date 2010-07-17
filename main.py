from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import simplejson as json
import util

#import urllib
#from google.appengine.api import urlfetch

import urllib, urllib2, Cookie
from google.appengine.api import urlfetch

#http://everydayscripting.blogspot.com/2009/08/google-app-engine-cookie-handling-with.html
class URLOpener:
  def __init__(self):
      self.cookie = Cookie.SimpleCookie()
    
  def open(self, url, data = None):
      if data is None:
          method = urlfetch.GET
      else:
          method = urlfetch.POST
    
      while url is not None:
          response = urlfetch.fetch(url=url,
                          payload=data,
                          method=method,
                          headers=self._getHeaders(self.cookie),
                          allow_truncated=False,
                          follow_redirects=False,
                          deadline=10
                          )
          data = None # Next request will be a get, so no need to send the data again. 
          method = urlfetch.GET
          self.cookie.load(response.headers.get('set-cookie', '')) # Load the cookies from the response
          url = response.headers.get('location')
    
      return response
        
  def _getHeaders(self, cookie):
      headers = {
                 'Host' : 'www.google.com',
                 'User-Agent' : 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.2) Gecko/20090729 Firefox/3.5.2 (.NET CLR 3.5.30729)',
                 'Cookie' : self._makeCookieHeader(cookie)
                  }
      return headers

  def _makeCookieHeader(self, cookie):
      cookieHeader = ""
      for value in cookie.values():
          cookieHeader += "%s=%s; " % (value.key, value.value)
      return cookieHeader



class MainPage(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Hello, webapp World!')

class Wave(webapp.RequestHandler):
    def post(self, wave_id):
        self.get(wave_id)
        
    def get(self, wave_id):
        from waveapi import events
        from waveapi import robot
        from waveapi import ops
        import passwords
        
        wave_id = urllib.unquote(wave_id)
        robot = robot.Robot('gae-run', 'http://a3.twimg.com/profile_images/250985893/twitter_pic_bigger.jpg')
        
        #works  #new wave sandbox
#        robot.setup_oauth(passwords.CONSUMER_KEY, passwords.CONSUMER_SECRET, server_rpc_base='http://www-opensocial-sandbox.googleusercontent.com/api/rpc')
#        wave = robot.new_wave(domain='wavesandbox.com', participants=['drewlesueur@wavesandbox.com'])
#        robot.submit(wave)
       
       
        #works #new wave preview
#        robot.setup_oauth(passwords.CONSUMER_KEY, passwords.CONSUMER_SECRET, server_rpc_base='http://www-opensocial.googleusercontent.com/api/rpc')
#        wave = robot.new_wave(domain='googlewave.com', participants=['drewalex@googlewave.com'])
#        robot.submit(wave)


#        robot.setup_oauth(passwords.CONSUMER_KEY, passwords.CONSUMER_SECRET, server_rpc_base='http://www-opensocial.googleusercontent.com/api/rpc')
#        wavelet = robot.fetch_wavelet('googlewave.com!w+ZycJbrZksH','googlewave.com!conv+root', 'drew')
#        robot.submit(wavelet)
#        self.response.out.write(wavelet.creator)

        robot.setup_oauth(passwords.CONSUMER_KEY, passwords.CONSUMER_SECRET, server_rpc_base='http://www-opensocial.googleusercontent.com/api/rpc')
        #wavelet = robot.fetch_wavelet('googlewave.com!w+Pq1HgvssD','googlewave.com!conv+root')
        wavelet = robot.fetch_wavelet(wave_id, 'googlewave.com!conv+root')
        # robot.submit(wavelet)
        
        if wavelet.creator == "drewalex@googlewave.com":
            code = wavelet.root_blip.text
            code = code.split('\n')
            code = code[2:] #remove first line
            code = "\n".join(code)
            compiled = compile(code, '<string>', 'exec')
            exec compiled in {'self':self, 'req': self.request, 'resp' : self.response, 'echo': self.response.out.write}
#           for id in wavelet.blips:
#               blip = wavelet.blips[id]
#               self.response.out.write(blip.text + "<hr />")


"""
#progroums code
def post(self):
        code = self.request.params['_code'].replace("\r\n", "\n") + "\n"
        code = "from google.appengine.api.urlfetch import fetch\n%s" % code
        compiled = compile(code, '<string>', 'exec')
        old_stderr, old_stdout = sys.stderr, sys.stdout
        try:
            sys.stderr, sys.stdout = self.response.out, self.response.out
            exec compiled in {'req': self.request, 'resp': self.response}
        finally:
            sys.stderr, sys.stdout = old_stderr, old_stdout

"""

        
class Gist(webapp.RequestHandler):
    def get_gist(self,gist):
        url = "http://gist.github.com/raw/"+gist+"/index.py"
        result = urlfetch.fetch(url)
        if result.status_code == 200:
            return result.content 


    def get_gist_owner(self,gist):
        url = "http://gist.github.com/api/v1/json/" + gist
        result = urlfetch.fetch(url)
        if result.status_code == 200:
            ret = json.loads(result.content)
            owner = ret['gists'][0]['owner']
            return owner
        return ""
    
    def post(self, gist):
        self.get(gist)
        
    def get(self, gist):
        owner = self.get_gist_owner(gist)
        if owner == 'drewlesueur':
            code = self.get_gist(gist)
            compiled = compile(code, '<string>', 'exec')
            exec compiled in {'self':self, 'req': self.request, 'resp' : self.response, 'echo': self.response.out.write}


class Doc(webapp.RequestHandler):
    def get(self, url):
        url = urllib.unquote(url)
        opener = URLOpener()
        result = opener.open(url)
        
        my_json = util.find_sandwich(result.content,'<script type="text/javascript">KX_mutations = ','; KX_modelChunkLoadStart')
        
        obj = json.loads(my_json)
        
        #self.response.out.write(obj["mutations"][0]["s"])
        code = (obj["mutations"][0]["s"])
        
        #fixing the pretty quotes
        code = code.replace(u'\u201C', '"').replace(u'\u201D','"') #replacing quotes
        
        author = obj["editedBy"]
        if author != "drewalex":
            return
        
        compiled = compile(code, '<string>', 'exec')
        exec compiled in {'self':self, 'req': self.request, 'resp' : self.response, 'echo': self.response.out.write}

            
application = webapp.WSGIApplication(
                                     [('/', MainPage), 
                                     (r'/gist/(.*)$',Gist),
                                     (r'/wave/(.*)$', Wave),
                                     (r'/doc/(.*)$', Doc)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()