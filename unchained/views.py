from django.shortcuts import render
from django.shortcuts import HttpResponse
from . import db
from datetime import datetime
from django.core.exceptions import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
import os
import pathlib

fields = {'standard':'''"sid","start_time", "end_time","Channel", "Module", "AgentName", "extension", "ANI",  "direction","filename"''',
          'all': '''"Module", "Channel", "start_time", "end_time", "AgentName", "extension", "ani",  "direction","personal_id","filename"'''}
#Fields that appear in the Standard and All views

@login_required(login_url='/accounts/login/') #You have to log in before you can do a query
def update(request):
    os.system('git fetch --all')
    os.system("git pull origin master")
    pathlib.Path('unchained/urls.py').touch()
    return HttpResponse("Updated from github")
@login_required(login_url='/accounts/login/') #You have to log in before you can do a query
def query(request):
    options = {'fields': 'standard','start_time':"2004-01-01T00:00",'end_time':"2022-12-31T23:59"} #Set defaults if first time loading page
    if request.method == 'POST': #Get settings from webpage
        options['AgentName'] = request.POST.get('AgentName', None) #doesn't let you search by agent id
        options['ANI'] = request.POST.get('ANI', None)
        options['Module'] = request.POST.get('Module', None)
        options['Channel'] = request.POST.get('Channel', None)
        options['call_id'] = request.POST.get('call_id', None)
        options['direction'] = request.POST.get('direction', None)
        options['dnis_code'] = request.POST.get('dnis_code', None)
        options['duration'] = request.POST.get('duration', None)
        options['end_time'] = request.POST.get('end_time', "2022-12-31T23:59")
        options['extension'] = request.POST.get('extension', None)
        options['p1'] = request.POST.get('p1', None)
        options['p2'] = request.POST.get('p2', None)
        options['p3'] = request.POST.get('p3', None)
        options['pbx_login_id'] = request.POST.get('pbx_login_id', None)
        options['personal_id'] = request.POST.get('personal_id', None)
        options['sid'] = request.POST.get('sid', None)
        options['start_time'] = request.POST.get('start_time', "2004-01-01T00:00")
        options['total_hold_time'] = request.POST.get('total_hold_time', None)
        options['limit'] = request.POST.get('limit', '500')
        options['fields'] = request.POST.get('fields','standard') #radio button for standard/all fields
        print(options)
        options['query'] = str(buildquery(options)) #Use the data from the webpage to build a SQL query
        options['results'] = db.qhtml(options['query']) #Do the query and turn it into an html table. Call it 'results'
        if options['fields'] == 'standard': #sets value of radio button
            options['standard'] = 'checked'
            options['all'] = ''
        else:
            options['all'] = 'checked'
            options['standard'] = ''
    return render(request, 'form.html', options) #send button values and 'results' back to the webpage for rendering

def buildquery(options): #builds the SQL query
    ignore = ('limit','start_time','end_time','fields','results','query', 'panel2','direction') # Special rules for certain fields

    #datetime.strptime(options['startdate'],"%Y-%m-%dT%H:%M").strftime()
    print(fields[options['fields']])
    #querystring = 'SELECT top %s %s from [combined].[dbo].[year] inner join [combined].[dbo].[agents] on [combined].[dbo].[year].agent_id = [combined].[dbo].[year].agent_id where ' % (options['limit'],fields[options['fields']])
    #don't need agent id lookup anymore
    querystring = "SELECT top %s %s from [combined].[dbo].[year] where " % (
    options['limit'], fields[options['fields']]) #basic query
    for i in options.keys(): #add parameters
        if options[i] is not None and i not in ignore and len(options[i]) > 0:
            querystring += "%s = '%s' AND " % (i, options[i]) #add AND between parameters
    if querystring.endswith('AND '): #at the end, remove the last AND
        querystring = querystring[:-5]
    if options['direction']: #convert direction name to direction number
        if options['direction'] != 'None':
            directions = {"Inbound":1,"Outbound":2,"Internal":3,"Unknown":0}
            if not querystring.endswith('where '):
                querystring += " AND "
            querystring += "direction = '%s'" % directions[options['direction']]

    if options['start_time']: #Convert start_time and end_time to proper SQL queries
        if not querystring.endswith('where '):
            querystring += " AND "
        dbstart_time = options['start_time'].replace('T', ' ')
        querystring += " start_time > '%s'" % dbstart_time
    if options['end_time']:
        if not querystring.endswith('where '):
            querystring += " AND "
        dbend_time = options['end_time'].replace('T', ' ')
        querystring += " end_time < '%s'" % dbend_time
    if querystring.endswith('where '): #Don't end the query with where if no options.
        querystring = querystring[:-6]
    print(querystring)
    return(querystring)
