from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import urlfetch
import simplejson as json
import urllib


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
            
application = webapp.WSGIApplication(
                                     [('/', MainPage), 
                                     (r'/gist/(.*)$',Gist),
                                     (r'/wave/(.*)$', Wave)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()