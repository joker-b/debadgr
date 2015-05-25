import flickr_api as f
import sys
import re


u = f.Person.findByUserName('What Photos Look Like')

badges = {}
for p in u.getPhotos(tags=['liquidity'],per_page=400):
    n = 0 
    for c in p.getComments():
        m = re.search(r'<img.*src="([^"]*)[^>]*>',c.text)
        if m is not None:
            n += 1
            k = m.group(1)
            q = re.search(r'<img.*alt="([^"]*)[^>]*>',m.group(0))
            if q is not None:
                k = 'Alt:%s' % (q.group(1))
            else:
                q = re.search(r'/([^/]*)\.jpg',m.group(1))
                if q is not None:
                    k = q.group(1)
            badges[k] = 1 + badges.get(k,0)
            #try:
            #    print c.text
            #except:
            #    pass
    #if n > 0:
    #    print "%s: %d picture comments" % (p.title,n)

t = 0
for b in badges:
    t += badges[b]

print '%d badges in total' % (t)

for b in sorted(badges, key=lambda b: badges[b]):
    try:
        print "'%s': %d badges" % (b,badges[b])
    except:
        print "(goofy name): %d badges" % (badges[b])
