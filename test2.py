import debadgr
import re

print '-'*50

renames = {\
	'madbaddangeroustoknowbyronsylviebenicenov282010intellectualpropertyrightsretained': 'Lord Byron',
	'madbaddangeroustoknowbyronsylviebe nicenov282010intellectualpropertyrightsretained': 'Lord Byron',
	'&amp;quote;ua': 'URBAN ARTE',
	'www.flickr.com/groups/la_creme_de_la_creme': 'La creme de la creme',
	'NUMBER 9 DREAM &#9824; Post 1 - Comment on 1&#9824; ': "Number 9 Dream",
	' [NUMBER 9 DREAM &#9824; Post 1 - Comment on 1&#9824; ': "Number 9 Dream",
	'Crazy &amp; Geniuses Shot&quot;&gt;A Crazy &amp; Geniuses Image!!! ~ ': 'folli e geni',
	' This great piece of Street Art was seen in &quot;Street Photography and Photographers rights - Post 1 - Comment 1 &quot;': "Street Photo &amp; Photographers Rights",
	'www.flickr.com/groups/flickrfavoritecityandstreet/pool/': 'Favorite City &amp; Street',
	'2201606@N24': 'Unsuspecting Protagonists',
	' <a> [blackandwhite the essence</a> [ 2 awards? Please post here!': 'Essence of Black &amp; White',
	' abstract_ photo/ post 1 = comment 2': 'Abstract Photo',
	' ...e x q u i s i t e a c h i e v e m e n t ! THANK YOU FOR POSTING IT.': '!Art and Photography',
	'www.flickr.com/groups/ivory_and_ebony/': 'Ivory and Ebony',
	'1575512@N25': 'Creative B&W Artwork' }


def oy(L,s):
	try:
		print L,'(',s,')'
	except:
		print '(unijunk)'

def seek_badge_data_old(Txt,Candidate,Level):
	# img inside link
	defaultName = re.sub(r'(\s|<(br|hr)>)+',' ',Candidate,flags=re.IGNORECASE|re.DOTALL)
	defaultName = '' if defaultName == ' ' else defaultName
	name = defaultName
	if (Level > 5):
		return (name,'Overflow')
	nl = Level + 1
	# newText = Txt
	b = Txt.encode('ascii','ignore')
	b = re.sub(r'</*(b|i|s|u)>','',b,flags=re.IGNORECASE|re.DOTALL)
	b = re.sub(u'[\u2000-\u2670\xa8*]',' ',b,flags=re.U)
	newText = re.sub(r'(\s|<(br|hr)>)+',' ',b,flags=re.IGNORECASE|re.DOTALL)
	m = re.search(r'youtube',newText)
	if m is not None:
		return ('youtube','done')
	#oy('NewText(%s)'%(name),newText)
	m = re.search(r'(.*)(<a\s+href="([^"]*)"[^>]*>(.*)(<img\s+(alt="([^"]*|\B)")*[^>]*(src="([^"]*)")[^>]*(alt="([^"]*|\B)")*[^>]*>)([^<]*)</a>)(.*)',newText,flags=re.DOTALL|re.IGNORECASE)
	if m is not None:
		L = '?'
		if m.group(7) is not None: # alt A
			L = 'LinkAlt A'
			name = m.group(7)
		elif m.group(11) is not None: # alt B
			L = 'LinkAlt B'
			name = m.group(11)
		elif m.group(12) != '' and m.group(12) != ' ': #img-trailing text
			L = 'Link Trail'
			name = m.group(12)
		elif m.group(4) != '' and m.group(4) != ' ': #img-leading text
			L = 'Link Lead'
			name = m.group(4)
		elif name == '': # only go to link if there's no name yet
			L = 'LinkLink'
			name = m.group(3) # link -- what about link title?
			name = re.sub('https://www.flickr.com/groups/','',name)
			name = re.sub('/$','',name)
		link = m.group(3)
		name = defaultName if name == ' ' else name
		name = renames.get(name,name)
		rem = ('[%s %s badge]'%(L,name)).join(list(m.group(1,13)))
		#if re.search('Blue M',newText):
		#	print '\n'.join(['%s'%(g) for g in m.groups()])
		name,newText = seek_badge_data_old(rem,name,nl)
		# oy('LinkAlt ',rem)
		return (name,newText)
	m = re.search(r'(.*)(<a\s+href="([^"]*)"[^>]*>(.*)</a>)(.*)',newText,flags=re.DOTALL|re.IGNORECASE)
	if m is not None:
		name = m.group(4)
		name = defaultName if name == ' ' else name
		rem = ('[Link %s badge]'%(name)).join(list(m.group(1,5)))
		try:
			name,newText = seek_badge_data_old(rem,name,nl)
		except:
			# print 'whoa %s' % (newText)
			name = defaultName
			newText = "done"
		# oy('Link ',rem)
		return (name,newText)
	m = re.search(r'(.*)(<img\s+(alt="[^"]*")*.*(src="[^"]*").*(alt="[^"]*")*[^>]*>)(.*)',newText,flags=re.DOTALL|re.IGNORECASE)
	if m is not None:
		if m.group(3) is not None: # alt A
			name = m.group(3)
		elif m.group(5) is not None: # alt B
			name = m.group(5)
		elif name == '':   # use link of nothig better is around
			name = m.group(4) # link
		link - m.group(4)
		name = defaultName if name == ' ' else name
		rem = ('[Aly %s badge]'%(name)).join(list(m.group(1,6)))
		try:
			name,newText = seek_badge_data_old(rem,name,nl)
		except:
			# print 'huh?'
			name = defaultName
			newText = "done"
		# oy('Alt ',rem)
		return (name,newText)
	# oy('OOPS: ',Txt)
	return (name,newText)




# #######################################################################



def seek_badge_data(Txt,Candidate,Level,Link):
	# img inside link
	defaultName = re.sub(r'(\s|<(br|hr)>)+',' ',Candidate,flags=re.IGNORECASE|re.DOTALL)
	defaultName = '' if defaultName == ' ' else defaultName
	name = defaultName
	link = Link
	if (Level > 5):
		return (name,'Overflow',link)
	nl = Level + 1
	# newText = Txt
	b = Txt.encode('ascii','ignore')
	b = re.sub(r'</*(b|i|s|u)>','',b,flags=re.IGNORECASE|re.DOTALL)
	b = re.sub(u'[\u2000-\u2670\xa8*]',' ',b,flags=re.U)
	newText = re.sub(r'(\s|<(br|hr)>)+',' ',b,flags=re.IGNORECASE|re.DOTALL)
	"""
	m = re.search(r'youtube',newText)
	if m is not None:
		return ('youtube','done',link)
	"""
	# oy('NewText(%s)'%(name),newText)
	# just kill all image links
	m = re.search(r'(.*)(<img\s+(alt="[^"]*")*.*(src="[^"]*")[^>]*(alt="[^"]*")*[^>]*>)(.*)',newText,flags=re.DOTALL|re.IGNORECASE)
	if m is not None:
		if m.group(3) is not None: # alt A
			name = m.group(3)
		elif m.group(5) is not None: # alt B
			name = m.group(5)
		name = defaultName if name == ' ' else name
		rem = ' '.join(list(m.group(1,6)))
		try:
			name,newText,link = seek_badge_data(rem,name,nl,link)
		except:
			# print 'huh?'
			name = defaultName
			newText = "done"
		# oy('Alt ',rem)
		return (name,newText,link)
	"""
	m = re.search(r'(.*)(<a\s+href="([^"]*)"[^>]*>(.*)(<img\s+(alt="([^"]*|\B)")*[^>]*(src="([^"]*)")[^>]*(alt="([^"]*|\B)")*[^>]*>)([^<]*)</a>)(.*)',newText,flags=re.DOTALL|re.IGNORECASE)
	if m is not None:
		L = '?'
		if m.group(7) is not None: # alt A
			L = 'LinkAlt A'
			name = m.group(7)
		elif m.group(11) is not None: # alt B
			L = 'LinkAlt B'
			name = m.group(11)
		elif m.group(12) != '' and m.group(12) != ' ': #img-trailing text
			L = 'Link Trail'
			name = m.group(12)
		elif m.group(4) != '' and m.group(4) != ' ': #img-leading text
			L = 'Link Lead'
			name = m.group(4)
		elif name == '': # only go to link if there's no name yet
			L = 'LinkLink'
			name = m.group(3) # link -- what about link title?
			name = re.sub('https://www.flickr.com/groups/','',name)
			name = re.sub('/$','',name)
		name = defaultName if name == ' ' else name
		name = renames.get(name,name)
		rem = ('[%s %s badge]'%(L,name)).join(list(m.group(1,13)))
		#if re.search('Blue M',newText):
		#	print '\n'.join(['%s'%(g) for g in m.groups()])
		name,newText,link = seek_badge_data(rem,name,nl,link)
		# oy('LinkAlt ',rem)
		return (name,newText,link)
	"""
	m = re.search(r'(.*)(<a\s+href="([^"]*)"[^>]*>(.*|\B)</a>)(.*)',newText,flags=re.DOTALL|re.IGNORECASE)
	if m is not None:
		if m.group(4) is not None:
			name = m.group(4)
			name = defaultName if name == ' ' else name
		link = m.group(3)
		rem = ('[%s badge]'%(name)).join(list(m.group(1,5)))
		if  name == '': # no name?
			name = re.sub('https://www.flickr.com/groups/','',link)
			name = re.sub('/$','',name)
		name = renames.get(name,name)	
		try:
			name,newText,link = seek_badge_data(rem,name,nl,link)
		except:
			# print 'whoa %s' % (newText)
			name = defaultName
			newText = "done"
		# oy('Link ',rem)
		return (name,newText,link)
	# oy('OOPS: ',Txt)
	return (name,newText,link)

for p in debadgr.tagged_pix(PerPage=400):
	ct = 0
	bct = 0
	for c in p.getComments():
		# print '......'
		n,t,l = seek_badge_data(c.text,'',0,'')
		if (n == ''):
			if (ct == 0):
				pass
				# print '-- %s %s ' % (p.title,'-'*50)
			ct += 1
			#print 'Comment "%s"' % (c.text.encode('ascii','ignore')) # hide
		else:
			if (bct == 0):
				print '-- %s %s ' % (p.title,'-'*50)
			bct += 1
			# pass
			if l != '':
				print '<a href="%s">%s</a>' % (l,n)
			else:
				print '<!-- %s -->' % (n)
			# oy('** Badge:','"%s" (%s)'%(n,l))
			# oy('Text: ',t)


# FIND IMAGE ONLY:
#  m = re.search(r'(.*)(<img\s+(alt="[^"]*")*.*(src="[^"]*").*(alt="[^"]*")*[^>]*>)(.*)',a,flags=re.DOTALL)
# 'xx'.join(list(m.group(1,6))) #$ rest of the comment
# print '\n'.join(['%s'%(g) for g in m.groups()])

# LINK title but... no filtering. there might be an img in there
#  m = re.search(r'(.*)(<a\s+href="([^"]*)"[^>]*>(.*)</a>)(.*)',a,flags=re.DOTALL|re.IGNORECASE)
# m.group(4) link innerHTML

# IMG INSIDE LINK
#  m = re.search(r'(.*)(<a\s+href="([^"]*)"[^>]*>(.*)(<img\s+(alt="([^"]*)")*.*(src="([^"]*)").*(alt="([^"]*)")*[^>]*>)(.*)</a>)(.*)',a,flags=re.DOTALL|re.IGNORECASE)
# 'xx'.join(list(m.group(1,13))) #$ rest of the comment
# m.group(3) # link addr
# m.group(7) # img alt A - may be None
# m.group(11) # img alt B - may be None
# m.group(4) img-leading inner text
# m.group(12) img-trailing inner text