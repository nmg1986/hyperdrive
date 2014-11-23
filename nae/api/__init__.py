from nae import wsgi
from nae.api import containers
from nae.api import images
from nae.api import projects
from nae.api import users 
from nae.api import repos 
import routes

class APIRouter(wsgi.Router):
    def __init__(self):

        self.mapper=routes.Mapper()
	self._setup_route()
	super(APIRouter,self).__init__(self.mapper)

    def _setup_route(self):
        self.mapper.resource('container','containers',
			     controller=containers.create_resource(),
			     member={'start':'POST',
				     'stop':'POST',
                                     'reboot':'POST',
				     'commit':'POST',
                                     'destroy':'POST'})
        self.mapper.resource('image','images',
			     controller=images.create_resource(),
			     member={'start':'POST',
				     'stop':'POST',
                                     'reboot':'POST',
				     'commit':'POST',
                                     'destroy':'POST'})
        self.mapper.resource('project','projects',
			     controller=projects.create_resource())

        self.mapper.resource('user','users',
			     controller=users.create_resource())

        self.mapper.resource('repository','repos',
			     controller=repos.create_resource())
