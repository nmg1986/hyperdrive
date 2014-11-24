import requests
from nae.common import cfg
from nae.common.cfg import Str, Int
import requests

CONF=cfg.CONF

class API(object):
    def __init__(self):
	self.host = Str(CONF.host)
	self.port = Int(CONF.port)
        self.url = "http://%s:%s" % (self.host,self.port) 
        self.headers={'Content-Type':'application/json'}
    def image_create(self,name,data):
        _url = "%s/images/create?name=%s" % \
	       (self.url,name)
        return requests.post(_url,
		    data=data)
	
    def image_inspect(self,name):
        _url = "%s/images/%s/json" % \
	       (self.url,name)
        return requests.get(_url)

    class container(object):
        @classmethod
        def create(cls,name,data):
            _url = "%s/containers/create?name=%s" % \
	       (self.url,name)
            return request.post(_url,
			    data=data)

	@classmethod
        def start(cls,id,data):
            _url="%s/containers/%s/start" % \
	     (self.url,id)
            return request.post(_url,
			    data=data) 
	@classmethod
        def stop(self,id):
            _url="%s/containers/%s/stop?t=10" % \
	     (self.url,id)
	    return requests.post(_url)	
	@classmethod
        def inspect(self,id):
	    _url="%s/containers/%s/json" % \
	     (self.url,id)
	    return requests.get(_url) 

	@classmethod
        def delete(self,id):
            _url="%s/containers/%s" % \
	     (self.url,id)
	    return requests.delete(_url)

   	@classmethod 
        def destroy(self,name):
            self.stop(name)
            self.delete(name)