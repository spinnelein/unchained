import pyodbc

def qhtml(sid=None):
    if sid:
        sid = str(sid)
        cursor.execute('SELECT top 10 * from  [combined].[dbo].[combined] where sid = %s;' % sid)
    else:
        cursor.execute('SELECT top 10 * from  [combined].[dbo].[combined];')
    header = [i[0] for i in cursor.description]
    list2d = [list(i) for i in cursor.fetchall()]
    list2d.insert(0, header)

    htable = u'<table border="1" bordercolor=000000 cellspacing="0" cellpadding="1" style="table-layout:fixed;vertical-align:bottom;font-size:13px;font-family:verdana,sans,sans-serif;border-collapse:collapse;border:1px solid rgb(130,130,130)"'
    list2d[0] = [u'<b>' + i + u'</b>' for i in list2d[0]]
    for row in list2d:

        newrow = u'<tr>'
        newrow += u'<td align="left" style="padding:1px 4px">' + str(row[0]) + u'</td>'
        row.remove(row[0])
        newrow = newrow + ''.join([u'<td align="right" style="padding:1px 4px">' + str(x) + u'</td>' for x in row])

        newrow += '</tr>'
        htable += newrow
    htable += '</table>'
    print(htable)
    return(htable)

conn = pyodbc.connect('Driver={SQL Server};'
                      r'Server=localhost\nationalgrid;'
                      'Database = year;'
                      'Trusted_Connection=yes;'
                      )
cursor = conn.cursor()
