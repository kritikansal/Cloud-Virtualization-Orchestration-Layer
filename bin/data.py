#!/bin/python
import os
import libvirt
import BaseHTTPServer
import sys
import json
from SocketServer import ThreadingMixIn
type_p={}
pm={}
pmid=1
im={}
imid=100
#global pm{}
def server_header(server,url):
	server.send_response(200)
	server.send_header("content-type","application/json")
	server.end_headers()
	pass

def phy_machine(machines_file):
	global pm
	global pmid
	f=open(machines_file,'r')
	for l in f.readlines():
		l=l.rstrip('\n')
		d=l.split('@')
		#con=libvirt.open("remote+ssh://root@localhost/system")
		#address="qemu:///system"
		address="remote+ssh://"+l+"/system"
		try:
	        	con = libvirt.open(address)
	       	except:
	               	print "Connection not opened"
	        try:
			print l
	                os.system("ssh "+l+" -C 'df -h --total | grep total' > disk")
			os.system("ssh "+l+ " -C ' free -m | head -n2 | tail -n1 ' > sp1") 
			os.system("ssh "+l+ " -C ' nproc ' > cpu1") 
			os.system("ssh "+l+ " -C ' cat /proc/cpuinfo | grep \"lm \"' > arc") 
		
		except Exception,e:
		        print str(e)

		#con=libvirt.open("remote+ssh://root@192.168.1.2/system")
	
		s=open("disk")
		size=s.read()
		size=size.split()
		freeharddisk=int(size[3][:-1])	#harddiskspace
		s.close() 
		
		de=open("sp1") 
		fram=de.read() 
		ram=int(fram.split()[3])    #free ram
		de.close() 
       			
		de=open("cpu1") 
		cpu=int(de.read())    #free cpu's
		de.close() 

		de=open("arc") 
		hard=de.read()    #hardware
		if hard=='':
			hard=32
		else:
			hard=64
		de.close() 


		'''phy_info = con.getInfo()
	        ram = phy_info[1]            #capacity of ram
		cpu = phy_info[7]            #number of cpu's
		size=open('disk','r')
		size=size.read()
		size=size.split()
		freeharddisk=int(size[3][:-1])'''
		#print freeharddisk
		pm[pmid]=[l,cpu,ram,freeharddisk,hard]	#physical machine's address,cpu,ram,harddisk free
		#print pm	
		pmid=pmid+1
		#con.close()
		con.close()
def images(image_file):
	global imid
	global im
	f=open(image_file,'r')
	for l in f.readlines():
		l=l.rstrip('\n')
		l=l.split(':')
		print l
		address=l[0]
		filename=l[1].split('/')[-1]
		pathfile=l[1]
		im[imid]=[address,filename,pathfile]
		imid=imid+1

final_types = []
file_type = ''
def types(instance_type):
	global final_types
	global file_type
	#file_type = instance_type
	f = open(instance_type)
	Typefile = json.load(f)
	print Typefile
	Typefile = Typefile['types']
	print "new",Typefile
	for x in Typefile:
		onetype_list = []
		for y in x:
			onetype_list.append(x[y])
		final_types.append(onetype_list)
	print final_types	

v=1
vminpm={}
vmdetails={}
def getvmid(pmid):
	global v
	print "here"
	v = v + 1
	if pmid not in vminpm:
		vminpm[pmid] = []
	  	vminpm[pmid].append(v)
	else:
		vminpm[pmid].append(v)
	return v
