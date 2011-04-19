import string
import random

def generate_installation_key():
    gen = lambda length: "".join( [random.choice(string.digits+string.letters) for i in xrange(length)])
    return '%s-%s-%s-%s' % (gen(4), gen(4), gen(4), gen(4))