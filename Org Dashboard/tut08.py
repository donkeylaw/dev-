import os, os.path, random, string, cherrypy, psycopg2

def connect(thread_index):
	conn_string = "host='dbcore.dev.porch.com' dbname='application_data' port='5434' user='donl' password='catch-22'"
	#create a connection and store it
	cherrypy.thread_data.db = psycopg2.connect(conn_string)

#call connect for each thread every time cherrypy starts
cherrypy.engine.subscribe('start_thread', connect)

DB_STRING = "host='dbcore.dev.porch.com' dbname='application_data' port='5434' user='donl' password='catch-22'"

class StringGenerator(object):
    @cherrypy.expose
    def index(self):
        return file('index.html')

class StringGeneratorWebService(object):
     exposed = True

     @cherrypy.tools.accept(media='text/plain')
     def GET(self):
         with sqlite3.connect(DB_STRING) as c:
             c.execute("SELECT value FROM user_string WHERE session_id=?",
                       [cherrypy.session.id])
             return c.fetchone()

     def POST(self, searchQuery=''):
         some_string = str(searchQuery)
         with psycopg2.connect(DB_STRING) as c:
	     query = """
		select count(*), organization_nm 
		from (
			select cco.company_key, org.organization_nm 
				from core.organization org 
					join core.company_linkto_organization clo using (organization_key) 
					join core.company cco using (company_key) 
				where org.organization_nm = ?
			) x
		group by organization_nm
	        """"
             c.execute(query, [some_string])
         return some_string

def setup_database():
     """
     Create the `user_string` table in the database
     on server startup
     """
     with sqlite3.connect(DB_STRING) as con:
         con.execute("CREATE TABLE user_string (session_id, value)")


 if __name__ == '__main__':
     conf = {
         '/': {
             'tools.sessions.on': True,
             'tools.staticdir.root': os.path.abspath(os.getcwd())
         },
         '/generator': {
             'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
             'tools.response_headers.on': True,
             'tools.response_headers.headers': [('Content-Type', 'text/plain')],
         },
         '/static': {
             'tools.staticdir.on': True,
             'tools.staticdir.dir': './public'
         }
     }

     cherrypy.engine.subscribe('start', setup_database)
     cherrypy.engine.subscribe('stop', cleanup_database)

     webapp = StringGenerator()
     webapp.generator = StringGeneratorWebService()
     cherrypy.quickstart(webapp, '/', conf)
