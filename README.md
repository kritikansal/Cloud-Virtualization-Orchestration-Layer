A Virtualization Orchestration Layer to provision virtual machines using LIBVIRT API and attaching object storage to them using CEPH API. This fabric can coordinate the provisioning of compute resources by negotiating with a set of Hypervisors running across physical servers in the datacenter.

BRIEF BACKGROUND: In today’s world, Hypervisor is the new OS and Virtual Machines are the new processes. Many system programmers are familiar with the low level APIs that are exposed by the operating systems like Linux and Microsoft Windows. These APIs can be used to take
control of the OS programmatically and help in developing management tools. Similar to the
OS, Hypervisors expose APIs that can be invoked to manage the virtualized environments. Typical APIs include provisioning, de-provisioning, changing the state of VMs, configuring the running VMs and so on. While it may be easy to deal with one Hypervisor running on a physical server, it is complex to concurrently deal with a set of Hypervisors running across the datacenter. In a dynamic environment, this is a critical requirement to manage the resources
and optimize the infrastructure. This is the problem that we try to solve in this project.

MODULES OF DESIGN OF SYSTEM:

1. Resource Discovery:
Recourse Discovery refers to the component which search/discovers the available hardware recourses in the given setup. A static file gives location of the hosts in the setup in the form of list of IP addresses.
Using this information, determined the available resources (CPU, RAM, HDD) on the hosts. This information will be used in the next step.

2. Resource Allocation:
Resource Allocation refers to the component, which decides what resources to allocate to fulfill the given request. Resource allocation is done only when
the request for creating a new Virtual Machine (VM) is received. Round Robin decides VM should be created on which Physical Machine (PM).

3. A REST API Server:
A server which provides the services for management and monitoring the virtual and physical infrastructure. The Representational State Transfer (REST) is a style of distributed architecture. 

Syntax for bash script to run the code:
./script pm_file image_file
pm_file : Contains a list of IP addresses separated by new-line. These addresses the Physical
machines to be used for hosting VMs. A unique ID is to be assigned by you.
image_file : Contains a list of Images(full path) to be used for spawning VMs. The name of the
image is to be extracted from the path itself. A unique ID is to be assigned by you.

After running the script, the rest server should be up and running.

1. LIBVIRT api used for hypervisor controller functionality.

2. CEPH api used for attaching object storage to the virtual machines created.

3. Round Robin algorithm used to coordinate the provisioning spanning multiple resources

4. Clients built that demonstrate the end-to-end use cases.

References:
1. EC2 APIs
2. OpenStack APIs and Architecture.
3. http://www.json.org/
4. http://libvirt.org/
5. Similar Open Source Project: http://archipelproject.org/
6. Android Client example: VM Manager
7. Json Validation: http://jsonlint.com/
8. You can use curl to see your server’s request-response during testing phase.
