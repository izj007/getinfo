#!encoding:utf-8

import requests,re,argparse,sys,urllib,base64,tldextract,json
from bs4 import BeautifulSoup
from xpinyin import Pinyin
reload(sys)
sys.setdefaultencoding('utf-8')

headers = {
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	#'Accept-Encoding': 'gzip, deflate, br',
	'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,ceb;q=0.6',
	'Connection': 'keep-alive',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
	'Cookie':'acw_tc=0e77722815507281066478052ea9feac45cd68099147b431a913b47acf; QCCSESSID=l483j1m8to2lrdqnqso8dmr1r6; zg_did=%7B%22did%22%3A%20%221690e991d366f5-030d9a1251cd7e-3c604504-1fa400-1690e991d3779b%22%7D; UM_distinctid=1690e99209c42c-078d669c3e9a78-3c604504-1fa400-1690e99209d6f7; CNZZDATA1254842228=87902333-1550727537-https%253A%252F%252Fwww.baidu.com%252F%7C1550727537; _uab_collina=155072811076072093967107; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1550728111,1550728120; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1550728930; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201550728109369%2C%22updated%22%3A%201550728930175%2C%22info%22%3A%201550728109370%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.baidu.com%22%7D'
}

info = {
	'company_name':'',
	'website':'',
	'cnnames':'',
	'ennames':'',
	'emails':'',
	'subdomains':''
	}
emails = set()
proxy = ''
cnnames = set()
username = set()
proxy_list = set()
proxy_blcacklist = set()

def getContent(url):
	if proxy!='':
		try:
			r = requests.get(url,headers=headers,proxies=proxy,timeout=5)
			r.encoding='utf-8'
			html = r.text
		except Exception as e:
			html = ''
	else:
		try:
			r = requests.get(url,headers=headers,timeout=5)
			r.encoding='utf-8'
			html = r.text
		except Exception as e:
			html = ''
	return html

def getFromBaidu(keyword,pages):
	regex = re.compile(r'([0-9a-zA-Z-_\.]{1,20})<em>@%s' % (keyword))
	print u'[-]百度搜索'
	for page in range(0,pages):
		print u'[*]开始查找第{}页'.format(page+1)
		url = "https://www.baidu.com/s?wd=%40{}&pn={}".format(keyword,page*10)
		html = getContent(url)
		#print html
		results = re.findall(regex,html)
		for result in results:
			email = '{}@{}'.format(result,keyword)
			print email
			emails.add(email)
	# for email in emails:
	# 	info['emails'] = '{}\n{}'.format(info['emails'] , email)

def getFromBing(keyword,pages):
	regex = re.compile(r'([0-9a-zA-Z-_\.]{1,20})<strong>@%s' % (keyword))
	#print regex
	print u'[-]Bing搜索'
	for page in range(0,pages):
		print u'[*]开始查找第{}页'.format(page+1)
		url = "https://cn.bing.com/search?q=%40{}&first={}".format(keyword,page*10)
		#print url
		html = getContent(url)
		#print html
		results = re.findall(regex,html)
		for result in results:
			email = '{}@{}'.format(result,keyword)
			print email
			emails.add(email)
	# for email in emails:
	# 	info['emails'] = '{}\n{}'.format(info['emails'] , email)

def getFromSoGou(keyword,pages):
	regex = re.compile(r'([0-9a-zA-Z-_\.]{1,20})<em><!--red_beg-->@%s' % (keyword))
	#print regex
	print u'[-]搜狗搜索'
	for page in range(1,pages+1):
		print u'[*]开始查找第{}页'.format(page)
		url = "https://www.sogou.com/web?query=%40{}&page={}".format(keyword,page)
		html = getContent(url)
		#print html
		results = re.findall(regex,html)
		for result in results:
			email = '{}@{}'.format(result,keyword)
			print email
			emails.add(email)
	# for email in emails:
	# 	info['emails'] = '{}\n{}'.format(info['emails'] , email)

def getFrom360(keyword,pages):
	regex = re.compile(r'([0-9a-zA-Z-_\.]{1,20})<em>@%s' % (keyword))
	#print regex
	print u'[-]360搜索'
	for page in range(1,pages+1):
		print u'[*]开始查找第{}页'.format(page)
		url = "https://www.so.com/s?q=%40{}&pn={}".format(keyword,page)
		html = getContent(url)
		#print html
		results = re.findall(regex,html)
		for result in results:
			email = '{}@{}'.format(result,keyword)
			print email
			emails.add(email)
	# for email in emails:
	# 	info['emails'] = '{}\n{}'.format(info['emails'] , email)

def getFromGoogle(keyword,pages):
	regex = re.compile(r'([0-9a-zA-Z-_\.]{1,20})@.*?%s' % (keyword))
	#print regex
	print u'[-]谷歌搜索'
	for page in range(0,pages):
		url = "https://www.google.com/search?q=%40{}&start={}&hl=zh-CN".format(keyword,page*10)
		html = getContent(url)
		#print html
		results = re.findall(regex,html)
		for result in results:
			email = '{}@{}'.format(result,keyword)
			print email
			emails.add(email)

def getTarget(keyword):
	regex = r'1\);\" href=\"(/firm_[0-9a-z]{32}.html)\"'
	try:
		url = 'https://www.qichacha.com/search?key={}'.format(keyword)
		html = getContent(url)
		results = re.findall(regex,html)
		url = 'https://www.qichacha.com{}'.format(results[0])
	except Exception as e:
		url = ''
	return url

def domainHandle(url):
	val = tldextract.extract(url)
	domain = "{0}.{1}".format(val.domain, val.suffix)
	return domain

def getDomain(url):
	regex = re.compile(ur'\"进入官网.*?>(.*?)<')
	try:
		html = getContent(url)
		# soup = BeautifulSoup(html,'lxml')
		# #domains = soup.find_all(class_='cvlu')
		# domains = soup.find_all(data-original-title="进入官网")
		# domain = domainHandle(domains[1].get_text().strip())
		domains = re.findall(regex,html)
		domain = domainHandle(domains[0].strip())
	except Exception as e:
		domain = ''
	return domain

def getAdmin(url):
	try:
		html = getContent(url)
		soup = BeautifulSoup(html,'lxml')
		admins = soup.find_all('h2',class_='seo font-20')
		for admin in admins:
			print admin.get_text()
			cnnames.add(admin.get_text())
	except Exception as e:
		pass

def getPerson(url):
	regex = re.compile(ur'\"进入官网.*?>(.*?)<')
	try:
		html = getContent(url)
		domains = re.findall(regex,html)
		if len(domains)>0:
			domain = domains[0].strip()
		else:
			domain = ''
		info['website'] = domain
		soup = BeautifulSoup(html,'lxml')
		company_name = soup.find_all('h1')[0].text
		info['company_name'] = company_name
		touzis = soup.find_all('h3',class_='seo font-14')
		print u'[-]对外投资及公司主要人员'
		if len(touzis)>0:
			for touzi in touzis:
				if len(touzi.contents[0])<=4:
					print touzi.contents[0]
					cnnames.add(touzi.contents[0])
			fenzhihtml = soup.find_all(id='Subcom')
			fenzhis= fenzhihtml[0].find_all('a',class_='c_a')
			print u'[-]分支机构负责人'
			for fenzhi in fenzhis:
				link = 'https://www.qichacha.com{}'.format(fenzhi.get('href'))
				getAdmin(link)
		else:
			touzis = soup.find_all('div',class_='whead-text')
			for touzi in touzis:
				if len(touzi.text.strip().split(' ')[0])<5:
					cnnames.add(touzi.text.strip().split(' ')[0])

		# for name in cnnames:
		# 	info['cnnames'] = '{}{}{}'.format(info['cnnames'] ,'\n', name)
		info['cnnames'] = list(cnnames)
	except Exception as e:
		pass

def getFullPin():
	print u'[-]姓名转全拼'
	pinyin = Pinyin()
	for name in cnnames:
		py = pinyin.get_pinyin(name.strip(),'')
		print '{}---{}'.format(name.strip().decode('utf-8').encode('gbk'),py)
		username.add(py)
	# for enname in username:
	# 	info['ennames'] = '{}\n{}'.format(info['ennames'] , enname)

def getShortPin():
	print u'[-]姓名转缩写'
	pinyin = Pinyin()
	for name in cnnames:
		py = pinyin.get_initials(name.strip(),'').lower()
		print '{}---{}'.format(name.strip().decode('utf-8').encode('gbk'),py)
		username.add(py)
	print u'[-]姓名转姓名全拼'
	for name in cnnames:
		xing = name.strip()[0]
		ming = name.strip()[1:]
		pyxing = pinyin.get_pinyin(xing,'')
		pyming = pinyin.get_initials(ming,'').lower()
		py = '{}{}'.format(pyxing,pyming)
		print '{}---{}'.format(name.strip().decode('utf-8').encode('gbk'),py)
		username.add(py)
	info['ennames'] = list(username)
	# for enname in username:
	# 	info['ennames'] = '{}\n{}'.format(info['ennames'] , enname)

def getSubFromhackertarget(domain):
	url = 'https://hackertarget.com/find-dns-host-records/'
	data = {
	'theinput': '%s' % (domain),
	'thetest': 'hostsearch',
	'name_of_nonce_field': '7762c8b52c',
	'_wp_http_referer': '/find-dns-host-records/'
	}
	try:
		html = requests.post(url,headers=headers,data=data).text
		soup = BeautifulSoup(html,'lxml')
		results = soup.find_all('pre',id="formResponse")
		result = results[0].text
	except Exception as e:
		result = ''
	info['subdomains'] = result

def saveSubDomains(domain):
	subdomains = getSubFromhackertarget(domain)
	filename = '{}_subdomians.txt'.format(domain)
	with open(filename,'w') as f:
		f.write(subdomains)

def isValidDomain(domain):
	regex = re.compile(r'^[0-9a-zA-Z\-_\.]{1,100}\.\w+$')
	if re.match(regex,domain):
		return True
	else:
		return False

def getExten(filename):
	extension = filename.split('.')[-1]
	return extension

def saveToTxt(filename):
	c_name = u'公司名:{}'.format(info['company_name'])
	c_website = u'官网:{}'.format(info['website'])
	c_cnname = ''
	c_enname = ''
	c_email = ''
	c_subdomain = ''
	for name in info['cnnames']:
		print name
		c_cnname = c_cnname + name + '\n'
	c_cnname = u'员工:\n{}'.format(c_cnname)
	for name in info['ennames']:
		c_enname = c_enname + name + '\n'
	c_enname = u'员工拼音:\n{}'.format(c_enname)
	for email in info['emails']:
		c_email = c_email + email + '\n'
	c_email = u'邮箱:\n{}'.format(c_email)
	c_subdomain = u'子域名:\n{}'.format(info['subdomains'])
	text = '{}\n{}\n{}\n{}\n{}\n{}'.format(c_name,c_website,c_cnname,c_email,c_subdomain,c_enname)
	with open(filename,'w') as f:
		f.write(text)

def getProxy():
	regex = re.compile(r'([0-9\.:]{9,21})')
	try:
		html = getContent('http://www.89ip.cn/tqdl.html?api=1&num=10&port=&address=&isp=')
		#html = getContent('xxx')
		results = re.findall(regex,html)
		result = results[0]
	except Exception as e:
		html = getContent('http://www.66ip.cn/mo.php?sxb=%D6%D0%B9%FA&tqsl=2&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1')
		results = re.findall(regex,html)
		result = results[0]
	return result

def checkProxy(proxy):
	try:
		html  =getContent('https://www.qichacha.com/firm_90c374c997ecb752ce9938db11c4a192.html')
	except Exception as e:
		raise e

def main():
	'''
		1.通过域名搜集邮箱
		2.通过公司名获取公司相关人员姓名，并转换成拼音字典
		3.通过api获取子域名
	'''
	parser = argparse.ArgumentParser()
	parser.add_argument("keyword", help=u"需要搜索的公司名或域名(必填参数)")
	parser.add_argument("-m", "--module", help=u"待定，默认为搜集信息",default=0)
	parser.add_argument("-p", "--page", help=u"需要搜索的页数",default=10)
	parser.add_argument("-P", "--proxy", help=u"使用代理,格式为ip:port")
	parser.add_argument("-o", "--output", help=u"保存的文件名")
	args = parser.parse_args()
	keyword = args.keyword
	pages = int(args.page)
	print u'[-]程序开始运行，请稍后……'
	if args.output is None:
		filename = '{}.json'.format(keyword)
	else:
		filename = args.output
	if args.proxy is not None:
		if args.proxy == 'auto':
			proxy_one = getProxy()
			print u'自动获取代理{}'.format(proxy_one)
		else:
			proxy_one = args.proxy
		global proxy
		proxy = {
		'http':'http://{}'.format(proxy_one),
		'https':'https://{}'.format(proxy_one)
		}
	if args.module == 1:
		pass
	elif args.module == 2:
		pass
	else:
		keywords = urllib.quote(keyword.decode('gbk').encode("UTF-8"))
		url = getTarget(keywords)
		if url == '':
			if isValidDomain(keyword):
				maindomain = keyword
			else:
				print u'[*]未找到有效的信息'
				exit()
		else:
			getPerson(url)
			getFullPin()
			getShortPin()
			if isValidDomain(keyword):
				maindomain = keyword
			else:
				maindomain = domainHandle(info['website'])
		getFromBaidu(maindomain,pages)
		getFromBing(maindomain,pages)
		getFrom360(maindomain,pages)
		getFromSoGou(maindomain,pages)			
		getSubFromhackertarget(maindomain)
	info['emails'] = list(emails)
	if getExten(filename) == 'json':
		with open(filename,'w') as f:
			json_data = json.dumps(info, indent=2)
			f.write(json_data)
	else:
		saveToTxt(filename)
	print u'[*]资料采集完成，请查看文件{}'.format(filename.decode('gbk').encode('utf-8'))



if __name__ == '__main__':
	main()