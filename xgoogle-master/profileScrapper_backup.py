# from bs4 import BeautifulSoup
# #from BeautifulSoup import BeautifulSoup          # For processing HTML
# from BeautifulSoup import BeautifulStoneSoup     # For processing XML
# import BeautifulSoup
# import urllib2

# page = urllib2.urlopen("http://www.linkedin.com/in/radheshgupta")

# soup = BeautifulSoup(page)
# print soup.prettify()
# for incident in soup('td', width="90%"):
#     where, linebreak, what = incident.contents[:3]
#     print where.strip()
#     print what.strip()
#     print


import mechanize
from bs4 import BeautifulSoup
import csv
import re
import sys

company_name_param = sys.argv[1]
print company_name_param

employee_all_data_file_name = 'companies/%s_employees_detail.csv' % (company_name_param)
print employee_all_data_file_name
#employee_all_data_file  = open('companies/bdna_employees_detail.csv', "wb")
employee_all_data_file  = open(employee_all_data_file_name, "wb")
employee_all_data_writer = csv.writer(employee_all_data_file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_ALL)

company_employee_data_file_name = 'companies/%s_employees.csv' % (company_name_param)
print company_employee_data_file_name
company_employee_data_file  = open(company_employee_data_file_name, "wb")
company_employee_data_writer = csv.writer(company_employee_data_file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_ALL)

br = mechanize.Browser()
#br.set_all_readonly(False)    # allow everything to be written to
br.set_handle_robots(False)   # ignore robots
br.set_handle_refresh(False)  # can sometimes hang without this
br.addheaders = [('User-agent', 'Firefox')]


company_name_file = 'companies/%s.csv' % (company_name_param)
profile_urls = csv.reader(open(company_name_file, 'rb'), delimiter='\t')

for url in profile_urls:
	print url[2]

	try:
	  response = br.open(str(url[2]))
	#response = br.open("http://www.linkedin.com/pub/dir/Kathy/Donahue")
	  page = response.read()
	  #print page      # the text of the page
	  #response1 = br.response()  # get the response again
	  #print response1.read()     # can apply lxml.html.fromstring()

	  soup = BeautifulSoup(page)
	  employee_name = "default_name"
	  try:
	    employee_name = soup.find(class_ = "full-name").text
	    print employee_name
	  except:
	    pass
	
	except:
	  pass


	#class = background-experience

	#picking the first from result set
	background_experience_rs = soup.find_all(id="background-experience")

	if len(background_experience_rs) > 0:
	  background_experience_soup = background_experience_rs[0]
	  experience_count = len(background_experience_soup.find_all(class_ = "editable-item"))
	  experience_rs = background_experience_soup.find_all(class_ = "editable-item")

	  #for i in range(0, experience_count):
	  for my_index in range (0, experience_count):
	    print my_index
	    try:
	      company_name = experience_rs[my_index].find_all("h5")[1].text
	      title = experience_rs[my_index].find_all("h4")[0].text
	      experience_times = experience_rs[my_index].find(class_ = "experience-date-locale").find_all("time")
	      start_time = experience_times[0].text
	      end_time = "present"
	      if len(experience_times) == 2:
	        end_time = experience_times[1].text
	      print company_name
	      print start_time
	      print end_time

	      employee_all_data_writer.writerow([employee_name, company_name, title, start_time, end_time])
	      if re.search(company_name_param, company_name, re.IGNORECASE):
	        company_employee_data_writer.writerow([company_name, employee_name, title, start_time, end_time])
	    except :
	      pass

	else:
	  print "Invalid page"

	background_education_rs = soup.find_all(id="background-education")

	if len(background_education_rs) > 0:
	  background_education_soup = background_education_rs[0]
	  education_count = len(background_education_soup.find_all(class_ = "editable-item"))
	  print "education count" + str(education_count)
	  education_rs = background_education_soup.find_all(class_ = "editable-item")

	  #for i in range(0, experience_count):
	  for my_index in range (0, education_count):
	    print my_index
	    try:
	      college_name = education_rs[my_index].find_all("h4")[0].text
	      education_times = education_rs[my_index].find_all("time")
	      start_time = education_times[0].text
	      end_time = "present"
	      if len(education_times) == 2:
	        end_time = re.findall(r'\d+', education_rs[1].find_all("time")[1].text)[0]
	      print college_name
	      print start_time
	      print end_time

	      employee_all_data_writer.writerow([employee_name, college_name, start_time, end_time])
	    except :
	      pass

	else:
	  print "Invalid page"


company_employee_data_file.close()
employee_all_data_file.close()