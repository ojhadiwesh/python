# -*- coding: utf-8 -*-
"""
Created on Thu Dec  6 12:27:01 2018

@author: dojha
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 16:46:11 2018

@author: dojha
"""
from robobrowser import RoboBrowser 
import config 
import re
USERNAME = 'username'
PASSWORD = 'password'
LOGIN_URL = config.JB_LOGIN_URL

result_no = 0
br = RoboBrowser()
br.open(LOGIN_URL)
#print(br)
form =(br.get_form())
#print(form)
form['username']= config.JB_USERNAME
form['password']= config.JB_PASSWORD
print(form.submit_fields)
br.submit_form(form, submit=form['submit'])

br.open(config.JB_SEARCH_URL)
print(br.parsed())
search_form = br.get_form()
print(search_form)
search_form['ctl00$cphMain$ddlOCountry'] = config.CHR_ORIGIN_COUNTRY
search_form['ctl00$cphMain$ddlOState'] = config.CHR_ORIGIN_STATE
search_form['ctl00$cphMain$txtOCity'] = config.CHR_ORIGIN_CITY
br.submit_form(search_form, submit=search_form['ctl00$cphMain$btnSubmit'])

print(br.select)

print(search_form.submit_fields)
print(search_form)
src = (br.parsed())
print(src)
start = '<div class="x-grid-cell-inner " style="text-align:left;">'
end = '</div></div>'
result = re.search('%s(.*)%s' %(start, end), src)
print(result)
import sys, time, os
from robobrowser import RoboBrowser 
LOGIN_URL = 'https://ssoauth.jbhunt.com/cas-server/login?service=https%3A%2F%2Fportalredirect.jbhunt.com%2Fportalredirect%2F'
USERNAME = 'JBHJ2020'
PASSWORD = '@3200Its!'
SEARCH_URL = 'https://carriers360.jbhunt.com/360/#!loadboard/search?'
FIXED_QUERY = """maxLoadWeight=100000&minDrivingMiles=0&maxDrivingMiles=10000&maxLoads=1&
                    maxStops=40&earliestStartDate=2018-12-05&minOffers=0&maxOffers=500&minBookNowPrice=0&
                    maxBookNowPrice=50000&originState=New%20York&originStateCode=NY&"""
VARIABLE_QUERY = ['equipmentType=%s' % equipmentType for equipmentType in
                                   ('All',
                                    'Dry Van',
                                    'Reefer',
                                    'Flatbed')]
                                   
def fetch(): 
    USERNAME = 'username'
    PASSWORD = 'password'
    result_no = 0
    br = RoboBrowser()
    br.open(LOGIN_URL)
    print(br)
    br.get_form(id="fm1")
    br['username'].value = USERNAME
    br['password'].value = PASSWORD
    resp = br.submit()

# Automatic redirect sometimes fails, follow manually when needed
    if 'Redirecting' in br.title():
        resp = br.follow_link(text_regex='click here')
        print(resp)
# Loop through the searches, keeping fixed query parameters
    for actor in VARIABLE_QUERY:
    # I like to watch what's happening in the console
        print >> sys.stderr, '***', actor
    # Lets do the actual query now
        br.open(SEARCH_URL + FIXED_QUERY + actor)
    # The query actually gives us links to the content pages we like,
    # but there are some other links on the page that we ignore
        nice_links = [l for l in br.links()
                        if 'good_path' in l.url
                        and 'credential' in l.url]
        if not nice_links:    # Maybe the relevant results are empty
            break
        for link in nice_links:
          
                response = br.follow_link(link)
                # More console reporting on title of followed link page
                print(sys.stderr, br.title())
                # Increment output filenames, open and write the file
                result_no += 1
                out = open('result%d'  %result_no, 'w')
                print ( out, response.read())
                out.close()
                # Nothing ever goes perfectly, ignore if we do not get page
              #  except RoboBrowser:
              #     print(sys.stderr, "Response error (probably 404)")
              # Let's not hammer the site too much between fetches
                time.sleep(1)
                
                
                
                
fetch()