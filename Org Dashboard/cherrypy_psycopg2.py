import os, os.path, random, string, cherrypy, psycopg2, matplotlib.pyplot as plt

def connect(thread_index):
	conn_string = "host='dbcore.dev.porch.com' dbname='application_data' port='5434' user='donl' password='catch-22'"
	#create a connection and store it
	cherrypy.thread_data.db = psycopg2.connect(conn_string)

#call connect for each thread every time cherrypy starts
cherrypy.engine.subscribe('start_thread', connect)

class Root: 
    def index(self): 
        # Sample page that displays the number of records in "table" 
        # Open a cursor, using the DB connection for the current thread 
        c = cherrypy.thread_data.db.cursor()
	query = """
	select count(*), organization_nm 
		from (
			select cco.company_key, org.organization_nm 
				from core.organization org 
					join core.company_linkto_organization clo using (organization_key) 
					join core.company cco using (company_key) 
				where org.organization_nm = 'NARI'
			) x
		group by organization_nm
	""" 
        c.execute(query)
        data = c.fetchall()
        c.close()
	print data


        return """<html>
		<head>
			<link href="/static/css/core.css" rel="stylesheet">		
		</head>
		<body>
<div class="org-report-header">
<div class="home-header-search container">
    <div class="row">
        <div class="heading-text">
            <h1><span style="text-align:center;">Organization Ingestion Report (<i>Alpha</i>)</span></h1>
        </div>
        <form class="search-bar" data-interaction-id="home-page_search-bar" onsubmit="return onSearchFormSubmit();">
            <div class="row">
                <div class="col-sm-12">
                        <span class="pair search-query-pair">
                            <label for="searchQuery">Organization Name:</label>
                            <span class="twitter-typeahead" style="position: relative; display: inline-block;"><input class="tt-hint" type="text" autocomplete="off" spellcheck="off" disabled="" style="position: absolute; top: 0px; left: 0px; border-color: transparent; box-shadow: none; background: -webkit-linear-gradient(top, rgba(255, 255, 255, 0), rgba(255, 255, 255, 0)) 0%% 0%% / auto repeat scroll padding-box border-box rgb(255, 255, 255);"><input id="searchQuery" name="searchQuery" type="text" class="search-query-input form-control tt-query" value="" placeholder="Pella Windows, NARI, etc." data-interaction-id="home-page_search-query" autocomplete="off" spellcheck="false" dir="auto" style="position: relative; vertical-align: top; background-color: transparent;"><span style="position: absolute; left: -9999px; visibility: hidden; white-space: nowrap; font-family: 'Whitney SSm 5r', 'Whitney SSm A', 'Whitney SSm B', sans-serif; font-size: 14px; font-style: normal; font-variant: normal; font-weight: 500; word-spacing: 0px; letter-spacing: 0px; text-indent: 0px; text-rendering: auto; text-transform: none;"></span><span class="tt-dropdown-menu" style="position: absolute; top: 100%%; left: 0px; z-index: 100; display: none;"></span></span>
                        </span>
                        </span>
                    <button class="btn btn-secondary btn-block home-search-btn" type="submit" data-interaction-id="home-page_search-button" style="margin-left:20px;">Go</button>
		<h2> There are <span style="color: lightseagreen;">%s</span> profiles for <span style="color: #3878d8;">%s</span> on Porch.</h2>
                </div>
            </div>
        </form>
    </div>
</div>
</div>
</body>
</html>""" % (str(data[0][0]), data[0][1])



    index.exposed = True

if __name__ == '__main__':
	conf = {
         '/': {
             'tools.sessions.on': True,
             'tools.staticdir.root': os.path.abspath(os.getcwd())
         },
         '/static': {
             'tools.staticdir.on': True,
             'tools.staticdir.dir': './public'
         }
     }
	cherrypy.quickstart(Root(), '/', conf)
