#!/bin/python

import create
import data
import libvirt 

def destroy(server,attributes):
	data.server_header(server,attributes)
	try:
		vmid = int(attributes[0])
		print "Trying to delete virtual machine with id",vmid
		v_name = data.vmdetails[vmid][0]
		machine_id = data.vmdetails[vmid][2]
		vmtype=data.vmdetails[vmid][3]

		remote_machine = data.pm[machine_id]
		remote_machine_add = remote_machine[0]
		path = 'remote+ssh://'+remote_machine_add+'/system'
		print "Remote ssh to virtual machine location",path
		conn = libvirt.open(path)
		try:
			r = conn.lookupByName(v_name)
		except:
			print "The said virtual machine does not exist on any physical machine."
		if r.isActive():
			r.destroy()
		r.undefine()
		print "vm_type",vmtype
		print "heyaa",data.final_types[vmtype-1]
		#data.final_types[vmtype-1][2]=data.final_types[vmtype-1][2]*1024/100000;
		print "byee",data.final_types[vmtype-1]
		req=data.final_types[vmtype-1]
		print data.pm[machine_id]
		print "req",req
		data.pm[machine_id][1]+=req[1]
		data.pm[machine_id][2]+=req[2]
		data.pm[machine_id][3]+=req[3]
		print data.pm[machine_id]
		del data.vmdetails[vmid]
		print "Virtual machine deleted and domain undefined."

		server.wfile.write(create.json_out({"status":1}))
	except:
		server.wfile.write(create.json_out({"status":0}))
