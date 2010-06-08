from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import urlfetch
import simplejson as json
import urllib

import sys
import logging
#import events #needed?

class Capabilities(webapp.RequestHandler):
    def get(self):
        self.response.out.write("""<w:robot xmlns:w="http://wave.google.com/extensions/robots/1.0"> 
<w:version>0xe49de7b</w:version> 
<w:protocolversion>0.21</w:protocolversion> 
<w:capabilities> 
<w:capability name="ANNOTATED_TEXT_CHANGED"/>
<w:capability name="BLIP_CONTRIBUTORS_CHANGED"/>
<w:capability name="BLIP_SUBMITTED"/>
<w:capability name="DOCUMENT_CHANGED"/>
<!--<w:capability name="EVENT"/>-->
<w:capability name="FORM_BUTTON_CLICKED"/>
<w:capability name="GADGET_STATE_CHANGED"/>
<w:capability name="OPERATION_ERROR"/>
<w:capability name="WAVELET_BLIP_CREATED"/>
<w:capability name="WAVELET_BLIP_REMOVED"/>
<w:capability name="WAVELET_CREATED"/>
<w:capability name="WAVELET_FETCHED"/>
<w:capability name="WAVELET_PARTICIPANTS_CHANGED"/>
<w:capability name="WAVELET_SELF_ADDED"/>
<w:capability name="WAVELET_SELF_REMOVED"/>
<w:capability name="WAVELET_TAGS_CHANGED"/>
<w:capability name="WAVELET_TITLE_CHANGED"/>
</w:capabilities> 
</w:robot>""")



class MainPage(webapp.RequestHandler):
    def handle(self, wave_id):
        from waveapi import events
        from waveapi import robot
        from waveapi import ops
        import passwords
        
        robot = robot.Robot('gae-run', 'http://a3.twimg.com/profile_images/250985893/twitter_pic_bigger.jpg')
        robot.setup_oauth(passwords.CONSUMER_KEY, passwords.CONSUMER_SECRET, server_rpc_base='http://www-opensocial.googleusercontent.com/api/rpc')
        wavelet = robot.fetch_wavelet(wave_id, 'googlewave.com!conv+root')
        if wavelet.creator == "drewalex@googlewave.com":
             code = wavelet.root_blip.text
             toHex = lambda x:"".join(["." + hex(ord(c))[2:].zfill(2) for c in x])
             logging.info(toHex(code))
             code = code.split('\n')
             
             code = code[2:] #remove first line
             code = "\n".join(code)
             #logging.info("code is:" + str(code))
             compiled = compile(code, '<string>', 'exec')
             exec compiled in {'a':1}
             
        
    def get(self):
        wave_id = self.request.get('name')
        wave_id = urllib.unquote(wave_id)
        self.handle(wave_id)
    
    def post(self):
        json_body = self.request.body
        json_body = unicode(json_body, 'utf8')
        body = json.loads(json_body)
        saved_stdout, sys.stdout = sys.stdout, sys.stderr
        logging.info('Incoming :): %s', json_body)
        
        sys.stdout = saved_stdout

        logging.info("test: hello")
        if 'proxyingFor' in body:
            wave_id = urllib.unquote(body['proxyingFor'])
            logging.info("wave_id: %s", wave_id)
            self.handle(wave_id)
        else:
            logging.info("no proxyFor")
application = webapp.WSGIApplication(
                                     [('.*/_wave/capabilities\.xml', Capabilities),
                                      ('.*', MainPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()