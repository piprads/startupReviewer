import time, random
from xgoogle.search import GoogleSearch, SearchError
import csv
import sys

arguments = str(sys.argv)
company_name = sys.argv[1]
print company_name

file_name = "companies/%s.csv" % (company_name)
print file_name
search_string = 'site:linkedin.com/pub/ OR site:linkedin.com/in/ \"at %s\"' % (company_name)
print search_string

ofile  = open(file_name, "wb")
writer = csv.writer(ofile, delimiter='\t', quotechar='"', quoting=csv.QUOTE_ALL)

max_pages = 58; # 58 times
for page in range (0, max_pages):
  wt = random.uniform(2, 5)
  try:
    #gs = GoogleSearch("quick and dirty")
    #gs = GoogleSearch("site:linkedin.com/pub/ Experience healthtap")
    gs = GoogleSearch("site:linkedin.com/pub/ OR site:linkedin.com/in/ \"at %s\"" % (company_name))
    gs.results_per_page = 10
    gs.page = page
    results = gs.get_results()
    #Try not to annnoy Google, with a random short wait
    time.sleep(wt)
    for res in results:
      print res.title.encode("utf8")
      print res.desc.encode("utf8")
      print res.url.encode("utf8")
      print
      writer.writerow([res.title.encode("utf8"), res.desc.encode("utf8"), res.url.encode("utf8")])
  except SearchError, e:
    print "Search failed: %s" % e

print "Done"
ofile.close()