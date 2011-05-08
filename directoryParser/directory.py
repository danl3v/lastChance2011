#import urllib
from BeautifulSoup import BeautifulSoup

'''
params = urllib.urlencode({'year': "2011"})
f = urllib.urlopen("http://apps.carleton.edu/campus/directory/", params)
html = f.read()
'''

file = open("data.html")
html = file.read()

soup = BeautifulSoup(html)

people = zip([name.string for name in soup.findAll("li", { "class": "personName"})], [email.find("a").string for email in soup.findAll("li", { "class": "personEmail"})])

string = ""

for person in people:
    names = person[0].split(" ")
    email = person[1].split("@")
    #print names[0] + "," + names[1] + "," + email[0]
    string += email[0] + " "

print string
