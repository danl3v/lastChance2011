from models import models

def has_crush(source, target):
    crushes = models.Crush.all()
    crushes.filter("source =", source)
    crushes.filter("target =", target)
    carl = crushes.get()
    return carl

def get_user_by_CID(username):
    carl = models.Carl.all()
    carl.filter("carletonID =",username)
    return carl.get()

def generate_pair_code():
    import random, string
    N = 20
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(N))

def update_matches():
    crushes = models.Crush.all()
    db.delete(models.Match.all())
    matches = [crush for crush in crushes if functions.has_crush(crush.target, crush.source)]
    for match in matches:
        new_match = models.Match()
        new_match.source = match.source
        new_match.target = match.target
        new_match.put()
    return matches
