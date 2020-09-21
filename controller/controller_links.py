import json
import cherrypy
from src.link_analysis import (get_links)
import settings


class GetRelatedLinks(object):
    """
        @class: GetCanisterInfo
        @createdBy: Govind Savara
        @createdDate: 9/28/2016
        @lastModifiedBy: Govind Savara
        @lastModifiedDate: 9/28/2016
        @type: class
        @param: object
        @desc:  get all the links for the keyword
    """
    exposed = True

    def GET(self, keyword=None):
        if keyword is None:
            return json.dumps({"error": "No keyword", "status": "failure"})

        data = get_links(keyword)

        cherrypy.response.headers['Access-Control-Allow-Origin'] = 'http://localhost:9004'

        if not data:
            response = json.dumps({"error": "No data available.", "status": "failure"})
        else:
            response = json.dumps({"status": "success", "data": data})

        return response
