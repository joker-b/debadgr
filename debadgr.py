import flickr_api as f
import sys
import re

names = False

class Badge(object):
    def __init__(self,Name):
        self.pic = None
        self.name = Name
        self.link = None
        self.posters = []
        self.count = 0
    def find_match(self,Cmnt):
        "see if this badge matches text in the comment"
        return False

badges = {}

def match_badge(Cmt):
    m = re.search(r'(.*)(<img.*src="([^"]*)[^>]*>)(.*)',Cmt.text)
    if m is not None:
        n += 1
        if names:
            k = Cmt.realname
        else:
            k = m.group(3)
            q = re.search(r'<img.*alt="([^"]*)[^>]*>',m.group(2))
            if q is not None:
                k = 'Alt:%s' % (q.group(1))
            else:
                q = re.search(r'/([^/]*)\.jpg',m.group(3))
                if q is not None:
                    k = q.group(1)
        badges[k] = 1 + badges.get(k,0)


def tagged_pix(Who='What Photos Look Like',Tags=['liquidity'],PerPage=400):
    u = f.Person.findByUserName(Who)
    return u.getPhotos(tags=Tags,per_page=PerPage)

def find_all():
    for p in tagged_pix():
        n = 0 
        # print '--- %s -------' % (p.title)
        for c in p.getComments():
            match_badge(c)

def report():
    bk = badges.keys()

    t = 0
    for b in bk:
        t += badges[b]

    print '%d badges in total with %d different images' % (t,len(bk))


    for b in sorted(bk, key=lambda b: badges[b]):
        try:
            print "'%s': %d badges" % (b,badges[b])
        except:
            print "(goofy name): %d badges" % (badges[b])
