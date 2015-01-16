import uuid
import copy
import webob.exc
from sqlalchemy.exc import IntegrityError

from jae import wsgi
from jae import base
from jae.common.timeutils import isotime
from jae.common.response import Response, ResponseObject
from jae.common import log as logging

LOG = logging.getLogger(__name__)

class Controller(base.Base):

    def __init__(self):
	super(Controller,self).__init__()

    def index(self,request):
        """
        List all repos by `project_id`.
   
        This method returns a dictionary list and each dict contains the following keys:
            - id
            - repo_path
            - created
         
        If no repos was found, a empty list will be returned.
        """
        repos=[]
        project_id = request.GET.get('project_id')
        project = self.db.get_project(project_id)
        if not project:
            LOG.error("no such project %s" % project_id)
            return webob.exc.HTTPNotFound() 

        for item in project.repos: 
            repo={
                'id':item.id,
                'repo_path':item.repo_path,
                'created':isotime(item.created),
                }
            repos.append(repo)

        return ResponseObject(repos) 

    def show(self,request,id):
        """
        Show the repo detail according repo `id`.
 
        This method returns a dictionary with following keys:
            - id
            - repo_path
            - project_id
            - created

        If no repos was found, a empty dictionary will be returned.
        """
        query = self.db.get_repo(id)
        if query is None:
	    return {}
        repo={'id':query.id,
              'repo_path':query.repo_path,
              'project_id':query.project_id,
              'created':isotime(query.created)}

	return ResponseObject(repo)

    def create(self,request,body):
        """create repos by body dict."""
        project_id=body.pop('project_id')
        repo_path=body.pop('repo_path')
        project = self.db.get_project(id=project_id)
	try:
            self.db.add_repo(dict(
		id = uuid.uuid4().hex,
                repo_path= repo_path),
                project = project)
        except IntegrityError,err:
	    LOG.error(err)
	    return webob.exc.HTTPInternalServerError() 

        return webob.exc.HTTPCreated() 

    def delete(self,request,id):
        """delete repos by id."""
        try:
            self.db.delete_repo(id)
        except:
            raise

        """return webob.exc.HTTPNoContent seems more better."""
        return webob.exc.HTTPNoContent()

def create_resource():
    return wsgi.Resource(Controller())

