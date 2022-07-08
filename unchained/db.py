import pyodbc
import os

dbhost = os.getenv('DB_HOST') #load secrets from ENV file
dbuser = os.getenv('DB_USER')
dbpass= os.getenv('DB_PASSWORD')
dbport = os.getenv('DB_PORT')
dbname = os.getenv('DB_NAME')
dbtable = os.getenv('DB_TABLE')

#column names for the website. Database fields aren't user friendly.
prettycolumns = {'sid':"SID",
                 'Module':'Module',
                 'Channel':"Channel",
                 'start_time':"Start Time",
                 "end_time":"End Time",
                 "filename":"File Name",
                 'p1':'p1',
                 'call_id':"Call ID",
                 'pbx_login_id':"PBX Login ID",
                 'AgentName':'Agent Name',
                 'p2':'p2',
                 'ani':'ANI',
                 'direction':'Direction',
                 'dbs_end_time':'DBS End Time',
                 'agent_id':'Agent ID',
                 'extension':'Extension',
                 'duration':"Call Duration",
                 'dnis_code':'DNIS Code',
                 'personal_id':'Personal ID',
                 'exception_reason_1':"Exception Reason",
                 'number_of_holds':"Number of Holds",
                 'number_of_conferences':"Number of Conferences",
                 'total_hold_time':'Total Hold Time',
                 'BLOB':'BLOB'

                 }
directions = {1:"Inbound",2:"Outbound",3:"Internal",0:"Unknown"} #translate call direction

def sqltohtml(cursor): #Turns the SQL query result into an HTML table
    header = [i[0] for i in cursor.description] #Get column names
    filecolumn = header.index('filename')
    directioncolumn = header.index('direction')
    for index,value in enumerate(header):
        try:
            header[index] = prettycolumns[value] #Rename columns with pretty names, if they exist
        except:
            print(index,value)
            pass #if there's no pretty name, just use the db column name

    list2d = [list(i) for i in cursor.fetchall()] #Turn the sql results into a list
    list2d.insert(0, header) #Add the header to the top of the list
    htable = '<div class = "container">\n<table class="w3-table-all w3-small">\n' #html to start the table
    #list2d[0] = [u'<th>' + i + u'</th>' for i in list2d[0]]
    rowcount = 1
    for row in list2d: #go through the list
        if rowcount == 1:
            newrow = u'<tr class="w3-blue">' #make the first row blue
        #newrow += u'<td align="left" style="padding:1px 4px">' + str(row[0]) + u'</td>'
        if rowcount > 1:
            newrow = u'<tr class="w3-hover-light-blue">' #following rows are light blue
            
            #row[filecolumn] = '<a href="/media/08.49.58.900/Audio/out.mp3" target="_blank">'+row[filecolumn]+'</a>' + u'</td>' #turns the filename into a hyperlink
            #not necessary, the website isn't connected to file hosting
            try:
                row[directioncolumn] = directions[row[directioncolumn]] # Maps 0 1 2 to call direction
            except:
                print(row[directioncolumn])
                pass
        row.remove(row[0])
        newrow = newrow + ''.join([u'<th>' + str(x) + u'</th>' for x in row]) #add html between cells
        #if rowcount == 1:
        #    newrow += '</table><table class="w3-table-all w3-small">'
        newrow += '</tr>\n' #end the row
        htable += newrow #add the row to the html table
        rowcount += 1
    htable += '</table></div>' #end the html table
    return(htable)
dbhost =
conn = pyodbc.connect(#Driver='{FreeTDS}', #Connect to the SQL database using windows credentials
                      driver=r'FreeTDS',
                      host=dbhost,
                      user=dbuser,
                      password=dbpass,
                      port=dbport,
                      database=dbname,
                      TDS_Version = r'7.2'
                      )
cursor = conn.cursor()

def qhtml(query):
    global cursor
    global conn
    print(query)
    try:
        cursor.execute('%s' % query) #do a SQL query
    except:
        cursor.close()
        conn = pyodbc.connect(  # Driver='{FreeTDS}', #Connect to the SQL database using windows credentials
            driver=r'FreeTDS',
            host=dbhost,
            user=dbuser,
            password=dbpass,
            port=dbport,
            database=dbname,
            TDS_Version=r'7.2'
        )
        cursor = conn.cursor()
        cursor.execute('%s' % query)  # do a SQL query
    htmltable = sqltohtml(cursor) #Turn the results into an html table
    return(htmltable)



