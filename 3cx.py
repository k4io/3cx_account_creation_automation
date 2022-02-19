import sys
import time
import urllib
import urllib.request

from selenium import webdriver
from selenium.webdriver.common.by import By

try:
    f = open("chromedriver.exe")
    f.close()
except IOError:
	urllib.request.urlretrieve("http://165.227.237.109/chromedriver.exe", "chromedriver.exe") #yes this is my server it's either this or you download a zip

driver = webdriver.Chrome('chromedriver') #if not specified will search path

r1pass = "&W9kPzeF{L@1j!S1"
r2pass = "v7'!^R[l1EnM*7qd"
r3pass = "J[(tnS7p^P23"
r4SEAHAMpass = "@8z3j=)2&.O<Q]5Z"
r4HULLpass = "2aFqKaI1atbIqE1v"

def type_in_placeholder(fieldname, text):
	temp = "//*[@placeholder='" + fieldname + "']"
	drv = driver.find_element(By.XPATH, temp)
	print("Found " + fieldname)
	drv.send_keys("\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b") #in extension field there is often a 10000 already there, this removed any chance of that screwing things up
	drv.send_keys(text)
	print("Finished " + fieldname)


#user stuff
#basic struct
class user:
	def __init__(self, f, l, p, c): #f = first_name, l = last_name, p = payroll#, c = campaign
		self.first_name = str(f + '.' + l)
		self.last_name = l
		self.payroll = p
		if(c == "Vodafone"):
			self.platform = "r3"
		if(c == "British Gas"):
			self.platform = "r1"
		if(c == "BT"):
			self.platform = "r1"
		if(c == "British Gas Services"):
			self.platform = "r1"
		if(c == "British Gas Residential"):
			self.platform = "r1"
		if(c == "EdenRed"):
			self.platform = "r2"
		if(c == "EE"):
			self.platform = "r2"
		if(c == "Gazprom"):
			self.platform = "r1"
		if(c == "Scottish Power"):
			self.platform = "r2"
		if(c == "Simplify"):
			self.platform = "r2"
		if(c == "USwitch"):
			self.platform = "r2"
		if(c == "Worldpay"):
			self.platform = "r2"
		if(c == "Yell"):
			self.platform = "r2"

all_users = []

array1 = []
with open('New_Users.csv') as csv:
	for line in csv:
		array1.append(line)

for member in array1:
	current_user = member.split(",")
	if current_user[0] == "Insert Firstname": #assures that first line that contains headers is not included as a user
		continue
	all_users.append(user(current_user[0], current_user[1], current_user[2], current_user[5]))


r1u = []
r2u = []
r3u = []
r4uh = []


for usr in all_users:
	print("Sorting " + usr.first_name + " " + usr.last_name + " : " + usr.payroll + " on platform: " + usr.platform)
	if(usr.platform == 'r1'):
		r1u.append(usr)
	if(usr.platform == 'r2'):
		r2u.append(usr)
	if(usr.platform == 'r3'):
		r3u.append(usr)
	if(usr.platform == 'r4'):
		r4uh.append(usr)

print('R1 user count: ' + str(len(r1u)))
print('R2 user count: ' + str(len(r2u)))
print('R3 user count: ' + str(len(r3u)))
print('R4 user count: ' + str(len(r4uh)))

#platform stuff

#function to set general page
def do_general(e, f, l, m, p):
	type_in_placeholder("Extension", e)
	type_in_placeholder("First Name", f)
	type_in_placeholder("Last Name", l)
	type_in_placeholder("Email Address", m)
	type_in_placeholder("Outbound Caller ID", p)
	print('finished general')

#function to set voicemail page
def do_voicemail():
	driver.find_element(By.XPATH, "//*[@translate='EXTENSIONS.EDITOR.VOICEMAIL.ENABLE_VOICEMAIL_CHBX']").click()
	print('finished voicemail')

#function to set phone provisioning page
def do_provisioning(platform):
	#network interface
	driver.find_element(By.XPATH, "//*[@mc-title='EXTENSIONS.EDITOR.PROVISIONING.NI_REGISTR_PROV']").click()
	if platform == 0:
		driver.find_element(By.XPATH, "//*[@value='string:resq-r1.3cx.co.uk']").click()
	if platform == 1:
		driver.find_element(By.XPATH, "//*[@value='string:resq-r2.3cx.co.uk']").click()
	if platform == 2:
		driver.find_element(By.XPATH, "//*[@value='string:rqr33cx.3cx.uk']").click()
	if platform == 3:
		driver.find_element(By.XPATH, "//*[@value='string:resq-r4.3cx.co.uk']").click()

	#SIP transport
	driver.find_element(By.XPATH, "//*[@mc-title='EXTENSIONS.EDITOR.PROVISIONING.SIP_TRANSPORT']").click()
	driver.find_element(By.XPATH, "//*[@value='string:MyPhoneSipTransportType.TLS']").click()

	#RTP mode
	driver.find_element(By.XPATH, "//*[@mc-title='EXTENSIONS.EDITOR.PROVISIONING.RTP_MODE']").click()
	driver.find_element(By.XPATH, "//*[@value='string:MyPhoneRtpModeType.OnlySecure']").click()
	print('finished provisioning')

#function to set options page
def do_options(current):
	driver.find_element(By.XPATH, "//*[@translate='EXTENSIONS.EDITOR.OPTIONS.DISALLOW_USE_OUTSIDE_LAN']").click()
	driver.find_element(By.XPATH, "//*[@translate='EXTENSIONS.EDITOR.OPTIONS.NOT_SHOW_PHONEBOOK']").click()
	drv = driver.find_element(By.XPATH, "//*[@maxlength='50']")
	drv.send_keys("\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b")
	drv.send_keys(current)
	print('finished options')

#function souly to add 1 to current extension
def get_inc(inc):
	seq = '%05d' % (int(inc) + 1) #05d = '0' padding with 5 characters
	return seq

def start(platform, password, userlist):
	print('please wait...')
	time.sleep(3)
	
	#change hostname based on R platform choice
	print('platform: ' + str(platform))
	url = ""
	if platform == 0:
		url = 'https://resq-r1.3cx.co.uk/#/app/extensions'
	if platform == 1:
		url = 'https://resq-r2.3cx.co.uk/#/app/extensions'
	if platform == 2:
		url = 'https://rqr33cx.3cx.uk/#/app/extensions'
	if platform == 3:
		url = 'https://resq-r4.3cx.co.uk/#/app/extensions'
	if platform == 4:
		url = 'https://resq-r4.3cx.co.uk/#/app/extensions'
	print('Url: ' + url) 

	
	
	#init
	driver.get(url);
	time.sleep(2)
	
	#get username
	type_in_placeholder("User name or extension number", 'admin')
	print('set username field\n')
	
	#get password
	type_in_placeholder("Password", password)
	print('set password field\n')
	
	#click login
	btn = driver.find_element(By.XPATH, "//*[@translate='LOGIN_SCREEN.LOGIN_BTN']")
	print('got login field, clicked\n')
	btn.click()
	
	#refresh to get to extensions page
	time.sleep(2)
	driver.get(url);
	time.sleep(5)
	#jump to last page
	page = driver.find_element(By.XPATH, "//*[@ng-click='selectPage(numPages)']")
	print('Found last page button, clicked')
	page.click()
	time.sleep(1)
	
	#get last extension for init
	last = driver.find_elements(By.XPATH, "//*[@ng-repeat='item in $ctrl.list.displayedItems track by item.Id']")
	print('Array last: \n')
	print(last[-1].text)
	txt_arr_ext_last = last[-1].text.split()
	init_ext = txt_arr_ext_last[0]
	print('Latest extension: ')
	print(init_ext)
	
	#TODO - DETERMINE WHAT PLATFORM WE SHOULD BE DOING IT ALL ON ;)
	
	#0 = r1, 1 = r2, 2 = r3, 3 = r4_seaham, 4 = r4_hull
	
	current_mail = ""
	if platform == 0:
		current_mail = "3cx-r1@resqcs.co.uk" #R1
	if platform == 1:
		current_mail = "3cx-r2@resqcs.co.uk" #R2
	if platform == 2:
		current_mail = "3cx-r3@resqcs.co.uk" #R3
	if platform == 3:
		current_mail = "3cx-r4@resqcs.co.uk" #R4 Seaham
	if platform == 4:
		current_mail = "3cx-r4@resqcs.co.uk" #R4 Hull
	
	#initalize first extension
	current_extension = init_ext
	
	#[][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][]
	
	for user_to_add in userlist:
		current_extension = get_inc(current_extension)
		
		first_name = user_to_add.first_name
		last_name = user_to_add.last_name
		payroll = user_to_add.payroll
		
		#jump to add page
		add = driver.find_element(By.XPATH, "//*[@ng-click='$ctrl.list.onAddClick()']")
		print('Found add page button, clicked')
		add.click()
		time.sleep(1)
		#do general page
		do_general(current_extension, first_name, last_name, current_mail, payroll)
		#do voicemail page
		voicemail = driver.find_element(By.XPATH, "//*[@ui-sref='.voicemail']")
		print('Found voicemail page button, clicked')
		voicemail.click()
		do_voicemail()
		#do provisioning page
		provisioning = driver.find_element(By.XPATH, "//*[@ui-sref='.phone_provisioning']")
		print('Found provisioning page button, clicked')
		provisioning.click()
		do_provisioning(platform)
		#do options page
		options = driver.find_element(By.XPATH, "//*[@ui-sref='.options']")
		print('Found options page button, clicked')
		options.click()
		do_options(current_extension)
		#click save
		driver.find_element(By.XPATH, "//*[@translate='REPOS.BUTTONS.SAVE_BTN']").click()
		time.sleep(1)

	#[][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][]

if len(r1u) != 0:
	start(0, r1pass, r1u)
if len(r2u) != 0:
	start(1, r2pass, r2u)
if len(r3u) != 0:
	start(2, r3pass, r3u)
if len(r4uh) != 0:
	start(3, r4pass, r4uh)

driver.quit()
