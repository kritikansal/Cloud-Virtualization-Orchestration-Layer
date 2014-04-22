#!/bin/python

import os
import BaseHTTPServer
import sys 
from SocketServer import ThreadingMixIn
import data
import create
import delete
import json
import libvirt
typefile=''
import rados, rbd

def json_out(out):
	        return json.dumps(out,indent=4)

def query(server,attributes):
        data.server_header(server,attributes)
        try:
                vmid = int(attributes)
                #print "Details of virtual machine with id",vmid
                v_name = data.vmdetails[vmid][0]
                machine_id = data.vmdetails[vmid][2]
                mtype = data.vmdetails[vmid][3]
                #print "{vmid:",vmid,", name: ",v_name,"instance_type: ",machine_id,"pmid: ",mtype
		'''server.wfile.write('{ \n' ) 
		server.wfile.write(' vmid : %d\n ' % int(vmid)) 
		server.wfile.write(' name :%s \n' % str(v_name)) 
		server.wfile.write(' instance_type: %d \n' % int(mtype)) 
		server.wfile.write(' pmid:%d \n }' % int(machine_id))
                '''
		server.wfile.write(create.json_out({"vmid":vmid, "name":v_name, "instance_type": mtype, "pmid": machine_id}))
        except Exception,e:
                print str(e)
                server.wfile.write(create.json_out({"status":0}))
def listimage(server):              #images list
        data.server_header(server,200)
	temp = []
	print "!!!!!!!!!",data.im
	
        for keys in data.im:
		d={}
		d["id"]=keys
		d["name"]=data.im[keys][1]
		temp.append(d)
	m={}
	m["images"]=temp
        server.wfile.write(create.json_out(m))
        pass
POOL_NAME='rbd'
VOLUME_LIST={}
def checkurl(server,url,typefile):
	host_name = url
	if '?' in url:
		host_name, arguments = url.split('?')
	components = host_name.split('/')
	if 'attach' in components:
			
		
	#if 'detach' in components:
		
		
	if 'create' in components:
		final_argument_list = []
		arg_split = arguments.split('&')
		if 'volume' in components:
			for i in xrange(0,2):
				final_argument_list.append((arg_split[i].split('='))[1])
			print final_argument_list
			data.server_header(server,final_argument_list)
			global VOLUME_LIST
                	args=final_argument_list
                	volume_name = str(args[0])
              		volume_size = args[1]
              		actual_size = str(int(float(volume_size)*(1024**3)))
			#os.system('sudo rbd create %s --size %s'%(str(volume_name),str(actual_size)))
			try:
				os.system('sudo rbd create ' + volume_name + ' --size ' + volume_size +' -k /etc/ceph/ceph.client.admin.keyring')
				#rbdInstance.create(ioctx,str(volume_name),actual_size)
				os.system('sudo modprobe rbd')
				os.system('sudo rbd map ' + volume_name + ' --pool rbd --name client.admin -k /etc/ceph/ceph.client.admin.keyring')
				#os.system('sudo mkfs.ext4 -m0 /dev/rbd/rbd/' + volume_name)
			
				#os.system('sudo rbd map %s --pool %s --name client.admin'%(str(volume_name),str(POOL_NAME)));
				global VOLUME_LIST
				volume_id=len(VOLUME_LIST)
				VOLUME_LIST[int(volume_id)]=volume_name
				print VOLUME_LIST
				server.wfile.write(json_out({"volumeid":volume_id+1}))
			except:
				server.wfile.write(json_out({"volumeid":'0'}))
		else:
			for i in xrange(0,3):
				final_argument_list.append((arg_split[i].split('='))[1])
			print final_argument_list
			create.create(server,final_argument_list)
			#return jsonify(volumeid=volume_id)
		#else:
		#	create.create(server,final_argument_list)
	if 'destroy' in components:
	  	final_argument_list = []
		arg_split = arguments.split('=')
		if 'volume' in components:
			final_argument_list.append(arg_split[1])
			global VOLUME_LIST
			args=final_argument_list
			volume_id = int(args[0])-1
			if volume_id in VOLUME_LIST:
				volume_name=str(VOLUME_LIST[int(volume_id)])
			else:
				print "here\n"
			try:
				os.system('sudo rbd unmap /dev/rbd/%s/%s'%(POOL_NAME,volume_name))
				os.system("sudo rbd rm %s"%(volume_name))
				server.wfile.write(json_out({"status":'1'}))
			except:
				server.wfile.write(json_out({"status":'0'}))
			#rbdInstance.remove(ioctx,volume_name)
		else:
		        final_argument_list.append(arg_split[1])
		        delete.destroy(server,final_argument_list)
		        pass
	if 'types' in components:
		data.server_header(server,200)
	  	try:
			f = typefile
			fopen = open(f)
			server.wfile.write(create.json_out(json.load(fopen)))
		except Exception,e:
			print str(e)
			server.wfile.write(create.json_out({"status":0}))
	if 'query' in components:
		if 'volume' in components:
			print 'volume'
		else:
			print "entered!!"
			final_argument_list = int(arguments.split('=')[1])
			query(server,final_argument_list)
	if 'list' in components:
		listimage(server)

class Handler_class(BaseHTTPServer.BaseHTTPRequestHandler):
	def do_GET(self):
		#self.wfile.write("hi hello")
		checkurl(self,self.path,typefile)
		#if (self.path[:4] not in ["/vm/","/pm/","/volume/"]) and (self.path[:7] != "/image/"):
		#	print "NOT valid URL"
		#	return
		#	self.send_error(404,"File Not Found")	
		#else:
		#	print "valid URL"
		#	checkurl(self,self.path,typefile)
def main():
	machines=sys.argv[1]
	images=sys.argv[2]
	vm=sys.argv[3]
	
	global typefile
	typefile=vm
		
	data.phy_machine(machines)	
	data.images(images)
	data.types(vm)	
	address = ('', 80)
	httpd = BaseHTTPServer.HTTPServer(address, Handler_class)
	print "Server Started at port", 80
#       httpd.serve_forever()
	try:
	        httpd.serve_forever()
	except KeyboardInterrupt:
		#clean.clean_server()
	        pass
	httpd.server_close()
if __name__ == "__main__":
	main()

