import flickr_api as f
import sys
import re

names = False

u = f.Person.findByUserName('What Photos Look Like')

badges = {}
for p in u.getPhotos(tags=['liquidity'],per_page=3):
    n = 0 
    print '--- %s -------' % (p.title)
    for c in p.getComments():
        m = re.search(r'(.*)(<img.*src="([^"]*)[^>]*>)(.*)',c.text)
        if m is not None:
            n += 1
            if names:
                k = c.realname
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
            #try:
            #    print ":: %s<%s>%s"%(m.group(1),k,m.group(4))
            #except:
            #    print "oops"
            # print dir(c)

            #try:
            #    print c.text
            #except:
            #    pass
    #if n > 0:
    #    print "%s: %d picture comments" % (p.title,n)

# print dir(c)

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
