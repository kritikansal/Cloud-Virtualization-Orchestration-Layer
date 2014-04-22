#!/bin/python

"""
Creates a Virtual Machine according to the specifications
"""
import libvirt as lbv
import json
import data
import subprocess
import os

test_number = 100000


def create_xml(vm_name,type_p,add,vmlocate,hyper_type,vmid,arch):
	xml = "<domain type="+str(arch[1])+  		\
			"><name>" + vm_name + "</name>				\
			<memory >"+str(type_p[2])+"</memory>					\
			<vcpu>"+str(type_p[1])+"</vcpu>						\
			<os>							\
			<type arch='"+arch[2]+"' machine='pc'>hvm</type>		\
			<boot dev='hd'/>					\
			</os>							\
			<features>						\
			<acpi/>							\
			<apic/>							\
			<pae/>							\
			</features>						\
			<on_poweroff>destroy</on_poweroff>			\
			<on_reboot>restart</on_reboot>				\
			<on_crash>restart</on_crash>				\
			<devices>							\
			<emulator>"+str(arch[0])+"</emulator>	\
			<disk type='file' device='disk'>			\
			<driver name="+str(arch[1])+" type='raw'/>			\
			<source file='"+str(vmlocate)+"'/>		\
			<target dev='hda' bus='ide'/>				\
			<address type='drive' controller='0' bus='0' unit='0'/>	\
			</disk>							\
			</devices>						\
			</domain>"
	return xml	

def json_out(out): 
        return json.dumps(out,indent=4) 


def create(server,arguments):
	data.server_header(server,arguments)
	if(1):
		vm_name = str(arguments[0])		# The name of VM
		vm_type = int(arguments[1])		# The Type(tid) of VM
		image_type = int(arguments[2])	# The ID of VM
		type_properties=[]
		type_properties = data.final_types[vm_type-1]  ## from types file, requirements of Virtual Machine
		print "dfg" ,type_properties
		m,useid = get_machine(type_properties)		# Get the physical machine to host the VM

		if useid == 0:
			print "NO MACHINES AVAILABLE FOR THE TASK"
			return
		print "Machine id",useid,"selected"
		machine_addr = m[0]
		
		images_list = data.im[image_type]  #dictionary
		location_user = images_list[0]
		filename = images_list[1]
		location_image = images_list[2]			#Find the location of image
				
		print "HRRAY!!anfdjnfv",m[0]," ",m[0].split('@')[0] 
		if not os.path.isfile('./'+filename): 
			subprocess.call(["scp",':'.join([location_user,location_image]),"."]) 
		try: 
			subprocess.call(["scp","./"+filename,':'.join([machine_addr,"/home/"+m[0].split('@')[0]+'/Desktop'])]) 
		except: 
			print "cannot copy"
		path = 'remote+ssh://'+m[0]+'/system'
		print "Remote ssh to machine location ---- ",path
		try:
			conn = lbv.open(path)
		except:
			print "Could Not Open Connection\n"
			return

		system_info = conn.getCapabilities()	#get PM capabilities
		node_info = conn.getInfo()
		print "HERE I AM",node_info[1],node_info[2]
		emulator_path = system_info.split("emulator>")
		
		emulator_path = emulator_path[1].split("<")[0]	#location of xen/qemu
		
		emulator1 = system_info.split("<domain type=")
	
		emulator1 = emulator1[1].split(">")[0]		#emulator present xen/qemu
		
		arch_type = system_info.split("<arch>")
		arch_type = arch_type[1].split("<")[0]

		data.type_p[useid] = [emulator_path ,emulator1, arch_type] #machine id as key--- stores physical machine arch details
#		print emulator_path ,emulator1, arch_type
		arch = data.type_p[useid]

		hyper_type = conn.getType().lower()
		print "Type of Connection --- ",hyper_type
		## check whether Xen or Qemu
		print "again",type_properties	
		print "final once",data.final_types
		type_properties[2] = (type_properties[2]*test_number)/1024
		print "last again",type_properties	
		print "final again",data.final_types
		'''if not os.path.isfile('~/'+images_list[1]):
#                       p = subprocess.Popen(["ssh",location_user])
                        print machine_addr,location_image
                        #subprocess.call(["scp",':'.join([location_user,location_image]),'/var/lib/libvirt/images/'])
                        subprocess.call(["scp",images_list[0]+':'+images_list[2],''])
                        #print "scp",':'.join([location_user,location_image]),':'.join([machine_addr,'/var/lib/libvirt/images/'+images_list[1][0]])
#                       p.kill()
		'''
		#xml = create_xml(vm_name, type_properties,images_list[0],'/var/lib/libvirt/images/',hyper_type,image_type,arch)  ## type_properties has tid,cpu,ram,disk
		xml = create_xml(vm_name, type_properties,images_list[0],"/home/"+m[0].split('@')[0]+'/Desktop/'+filename,hyper_type,image_type,arch)  ## type_properties has tid,cpu,ram,disk

#		print xml
	
		connect_xml = conn.defineXML(xml)
		try:
			connect_xml.create()
			print "Task Done!" 
			vmachine_id = data.getvmid(useid)	#Get Virtual Machine unique ID -- useid is machineid!
			data.vmdetails[vmachine_id] = [vm_name, type_properties, useid,vm_type]			#store VM vs Phy machine details..
			print "vm ne kya liya",data.vmdetails[vmachine_id]
#			print "Here are details",fileHandling.machine_v_details,vmachine_id
			server.wfile.write(json_out({"vmid":vmachine_id}))
		except Exception,e:
			print str(e)
			server.wfile.write(json_out({"vmid":0}))

	else:
		server.wfile.write(json_out({"vmid":0}))

iterate=1
def get_machine(vmtype):
	global iterate
	r_cpu = vmtype[1]	
	r_ram = vmtype[2]	
	r_disk = vmtype[3]
	print r_cpu, data.pm[1][1]
	l=len(data.pm)
	print "l is ",l
	x=iterate
	while iterate<=l:
		if data.pm[iterate][1] >= r_cpu and data.pm[iterate][2] >= r_ram and data.pm[iterate][3] >= r_disk:
			data.pm[iterate][1] -= r_cpu
			data.pm[iterate][2] -= r_ram
			data.pm[iterate][3] -= r_disk
			print "get out", data.pm[iterate],iterate
			return data.pm[iterate],iterate
		iterate=iterate+1
		print "x is!!",x,"hey",iterate
		if iterate==x:
			print "ho"
			return 0,0
		if iterate>l:
			iterate=1 
	return 0,0
#	id_to_be_used = idused()
#	return fileHandling.machine_with_id[id_to_be_used],id_to_be_used

def idused():
	return 100
