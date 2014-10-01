import psycopg2, sys, pprint

def main():
	#define the connection string
	conn_string = "host='dbcore.qa.porch.com' dbname='application_data' port='5435' user='donl' password='catch-22'"

	#print the connection string
	print "Connecting to database\n ->%s" % (conn_string)
	
	#get a connection - or raise an exception if it fails
	conn = psycopg2.connect(conn_string)

	#this creates a cursor that will be used to perform queries
	cursor = conn.cursor()

	#execute query function
	cursor.execute("select * from public.org_ingestion_report('NARI')")
	records = cursor.fetchall()

	#print output records
	pprint.pprint(records)
	

if __name__ == "__main__":
	main()
