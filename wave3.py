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
    def handle(self):
        from waveapi import events
        from waveapi import robot
        from waveapi import ops
        import passwords
        robot = robot.Robot('gae-run', 'http://a3.twimg.com/profile_images/250985893/twitter_pic_bigger.jpg')
        robot.setup_oauth(passwords.CONSUMER_KEY, passwords.CONSUMER_SECRET, server_rpc_base='http://www-opensocial.googleusercontent.com/api/rpc')
        wavelet = robot.fetch_wavelet('googlewave.com!w+g2tJlP3LB','googlewave.com!conv+root')
        code = wavelet.root_blip.text
        code = code.split('\n')
        code = code[2:] #remove first line
        code = "\n".join(code)
        logging.info(code)
        compiled = compile(code, '<string>', 'exec')
        exec compiled in {'a':1}
             
        
    def get(self):
        self.handle()
    
    def post(self):
        self.handle()

application = webapp.WSGIApplication([('.*/_wave/capabilities\.xml', Capabilities),('.*', MainPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
