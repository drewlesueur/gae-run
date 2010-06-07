"""
import myweb
print 'Content-Type: text/plain'
_get = myweb.get_get_vars()
if 'st' in _get and _get['st'] == '800':
  print "AOijR2eS6WhD_RW6ujxWbkH32qdwwJ8qwTfBr72Vafp6oGJcfwd2zMlCYXW2oaCDPkD07S518MNwAM5W1djQwiOHldAI6200n2T2DZcdBwRI1k_PJwPrpll3B2u0lEO78NeZ5Nc9xoqtdnD944gZ9iZCS3Dzsaf_8Q=="
else:
  print "no can do"
"""


from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app


class Verify(webapp.RequestHandler):
    def get(self):
        st = self.request.get('st')
        self.response.headers['Content-Type'] = 'text/plain'
        if st == '7202':
            self.response.out.write('AOijR2dAUDPVtbxzVCwyXjFxfsV9_8DDSESQqciw6KogSt4J8_7uYD-Xw_VugGyq_WVjZlxK7vvi7lJCxiUTQ-8BN-1i-EZzzgIWOlPv-9xNMtsEfwcJsY_xeqRKxWVGi5vdbpczZE-WLrDWl1E9ACE1r_Ex3cnbbw==')
        else:
            self.response.out.write('no can do')
            

application = webapp.WSGIApplication(
                                     [('/_wave/verify_token', Verify)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()