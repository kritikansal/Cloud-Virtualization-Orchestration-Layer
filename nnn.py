from xml.etree import ElementTree as ET import libvirt,os DISK_TEMPLATE= \ '''<disk type='network' device='disk'> <source protocol='rbd' name='rbd/chakka'> <host name='meenal-pc' port='6789'/> </source> <target dev='hdb' bus='virtio'/> </disk> ''' def attach_disk(domain, path, dev): conn = libvirt.open('remote+ssh://girish@10.1.97.7/') # os.system("scp ./try1.xml girish@10.1.97.7:/home/girish/abc.xml") # os.system("ssh girish@10.1.97.7 sudo virsh attach-device somia /home/girish/abc.xml") dom = conn.lookupByName(domain) template = DISK_TEMPLATE.format(path=path, dev=dev) dom.attachDevice(template) attach_disk('somia', '/mnt/check-disk', 'hdb')