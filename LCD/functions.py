import models

def has_crush(source, target):
    carl2carl = models.Carl2Carl.all()
    carl2carl.filter("source =", source)
    carl2carl.filter("target =", target)
    carl = carl2carl.get()
    return carl

def get_user_by_CID(username):
    carl = models.Carl.all()
    carl.filter("carletonID =",username)
    return carl.get()

def generate_pair_code():
    import random, string
    N = 20
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(N))
