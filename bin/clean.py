#!/bin/python

import data
import libvirt as lbv

def clean_server():
	try:
		print "Cleaning all virtual machines"
		for vmid in data.pm:
			v_name = data.pm[vmid][0]
			machine_id = data.pm[vmid][2]
	
			remote_machine = data.pm[machine_id]
			remote_machine_add = remote_machine[0]+'@'+remote_machine[1]
			path = 'remote+ssh://'+remote_machine_add+'/system'
			print "Remote ssh to virtual machine location",path
			conn = lbv.open(path)
			try:
				r = conn.lookupByName(v_name)
			except:
				print "The ",v_name,"virtual machine does not exist on any physical machine."
			if r.isActive():
				r.destroy()
			r.undefine()
#		del fileHandling.machine_v_details[vmid]
		print "Virtual machines deleted and domain undefined."

	except Exception,e:
		print str(e)


