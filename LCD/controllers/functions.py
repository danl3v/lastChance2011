from models import models
from google.appengine.ext import db
import session

def has_crush(source, target):
    crushes = models.Crush.all()
    crushes.filter("deleted =", False)
    crushes.filter("source =", source)
    crushes.filter("target =", target)
    carl = crushes.get()
    return carl

def get_user_by_CID(username):
    carl = models.Carl.all()
    carl.filter("carletonID =", username)
    return carl.get()

def generate_pair_code():
    import random, string
    N = 20
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(N))

def update_matches():
    crushes = models.Crush.all().filter("deleted =", False)
    db.delete(models.Match.all())
    matches = [crush for crush in crushes if has_crush(crush.target, crush.source)] # we still calculate matches for opted out users in case they want to opt in at the last minute or something
    for match in matches:
        new_match = models.Match()
        new_match.source = match.source
        new_match.target = match.target
        new_match.put()
    return matches

def get_site_status(): # make a get setting function and a set setting function
    site_status = models.Setting.all().filter("name =", "site_status").get()
    if not site_status:
        site_status = models.Setting()
        site_status.name = "site_status"
        site_status.value = "open"
        site_status.put()
    if not site_status.value:
        site_status.value = "open"
        site_status.put()
    return site_status.value

def set_site_status(new_site_status):
    if new_site_status not in ["pre", "open", "calculating", "showing"]:
        return '{"success":1, "status":"' + new_site_status + '"}'
    else:
        site_status = models.Setting.all().filter("name =", "site_status").get()
        if not site_status:
            site_status = models.Setting()
            site_status.name = "site_status"
            site_status.value = new_site_status
            site_status.put()
        else:
            site_status.value = new_site_status
            site_status.put()
        return '{"success":0, "status":"' + new_site_status + '"}'

def get_statistic(name):
    statistic = models.Statistic.all().filter("name =", name).get()
    if statistic: return statistic.value
    else: return 0
    
def set_statistic(name, value):
    statistic = models.Statistic.all().filter("name =", name).get()
    if not statistic:
        statistic = models.Statistic()
        statistic.name = name
    statistic.value = value
    statistic.put()

def only_if_site_not_pre(f):
    def helper(self):
        if get_site_status() != "pre": return f(self)
        self.redirect("/")
    return helper

def only_if_site_open(f):
    def helper(self):
        if get_site_status() == "open": return f(self)
        else: self.response.out.write('You can\'t enter crushes anymore on Last Chance Dance. <a href="/">Head on back home</a>.')
    return helper
    
def only_if_site_showing(f):
    def helper(self):
        if get_site_status() == "showing": return f(self)
        else: self.response.out.write('The matches are not out yet. <a href="/">Head on back home</a>.')
    return helper
    
def only_if_paired_opted_in(f):
    def helper(self):
        if session.isPaired() and session.opted_in(): return f(self)
        else: self.response.out.write('{"success":1}')
    return helper
