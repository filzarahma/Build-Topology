#!/usr/bin/python
'''
 Source code tugas besar jaringan komputer dibuat oleh:
 Nama : Filza Rahma Muflihah
 NIM  : 1301201261
 Kelas: IF-44-03
'''

#import library
from mininet.log import setLogLevel, info
from mininet.node import UserSwitch, OVSKernelSwitch
from mininet.cli import CLI
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink, Link, Intf
from mininet.node import CPULimitedHost
from mininet.util import pmonitor
from signal import SIGINT
from time import time
import os
from subprocess import *
 
def topology():
    #konfigurasi mininet
    Link = TCLink
    host = CPULimitedHost
    net = Mininet(link=Link, host=host)
   
    #menambah host
    h1 = net.addHost('h1')
    h2 = net.addHost('h2')
   
    #menambah router
    r1 = net.addHost('r1')
    r2 = net.addHost('r2')
    r3 = net.addHost('r3')
    r4 = net.addHost('r4')
   
    #setting bandwidth
    bw1 = {'bw':1} #bandwidth 1 mbps
    bw2 = {'bw' :0.5} #bandwidth 500 kbps
   
    #hubungkan host dengan router sesuai topologi
    net.addLink(h1,r1, IntfName1 = 'h1-eth0', IntfName2 = 'r1-eth0', cls = TCLink, **bw1)
    net.addLink(h1,r2, IntfName1 = 'h1-eth1', IntfName2 = 'r2-eth0', cls = TCLink, **bw1)
    net.addLink(h2,r3, IntfName1 = 'h2-eth0', IntfName2 = 'r3-eth0', cls = TCLink, **bw1)
    net.addLink(h2,r4, IntfName1 = 'h2-eth1', IntfName2 = 'r4-eth0', cls = TCLink, **bw1)
    net.addLink(r1,r3, IntfName1 = 'r1-eth1', IntfName2 = 'r3-eth1', cls = TCLink, **bw2)
    net.addLink(r2,r4, IntfName1 = 'r2-eth1', IntfName2 = 'r4-eth1', cls = TCLink, **bw2)
    net.addLink(r1,r4, IntfName1 = 'r1-eth2', IntfName2 = 'r4-eth2', cls = TCLink, **bw1)
    net.addLink(r2,r3, IntfName1 = 'r2-eth2', IntfName2 = 'r3-eth2', cls = TCLink, **bw1)

    '''
    #add link + modifikasi buffer size 100
    net.addLink(h1,r1, max_queue_size = 100, IntfName1 = 'h1-eth0', IntfName2 = 'r1-eth0', cls = TCLink, **bw1)
    net.addLink(h1,r2, max_queue_size = 100, IntfName1 = 'h1-eth1', IntfName2 = 'r2-eth0', cls = TCLink, **bw1)
    net.addLink(h2,r3, max_queue_size = 100, IntfName1 = 'h2-eth0', IntfName2 = 'r3-eth0', cls = TCLink, **bw1)
    net.addLink(h2,r4, max_queue_size = 100, IntfName1 = 'h2-eth1', IntfName2 = 'r4-eth0', cls = TCLink, **bw1)
    net.addLink(r1,r3, max_queue_size = 100, IntfName1 = 'r1-eth1', IntfName2 = 'r3-eth1', cls = TCLink, **bw2)
    net.addLink(r2,r4, max_queue_size = 100, IntfName1 = 'r2-eth1', IntfName2 = 'r4-eth1', cls = TCLink, **bw2)
    net.addLink(r1,r4, max_queue_size = 100, IntfName1 = 'r1-eth2', IntfName2 = 'r4-eth2', cls = TCLink, **bw1)
    net.addLink(r2,r3, max_queue_size = 100, IntfName1 = 'r2-eth2', IntfName2 = 'r3-eth3', cls = TCLink, **bw1)
    '''  
   
    #build topologi
    net.build()
 
    #konfigurasi router dan host
    h1.cmd('ifconfig h1-eth0 0')
    h1.cmd('ifconfig h1-eth1 0')
 
    h2.cmd('ifconfig h2-eth0 0')
    h2.cmd('ifconfig h2-eth1 0')
 
    r1.cmd('ifconfig r1-eth0 0')
    r1.cmd('ifconfig r1-eth1 0')
    r1.cmd('ifconfig r1-eth2 0')
 
    r2.cmd('ifconfig r2-eth0 0')
    r2.cmd('ifconfig r2-eth1 0')
    r2.cmd('ifconfig r2-eth2 0')
 
    r3.cmd('ifconfig r3-eth0 0')
    r3.cmd('ifconfig r3-eth1 0')
    r3.cmd('ifconfig r3-eth2 0')
 
    r4.cmd('ifconfig r4-eth0 0')
    r4.cmd('ifconfig r4-eth1 0')
    r4.cmd('ifconfig r4-eth2 0')
 
    #subnetting
    h1.cmd('ifconfig h1-eth0 195.30.0.1 netmask 255.255.255.0') #h1-r1
    h1.cmd('ifconfig h1-eth1 195.30.5.2 netmask 255.255.255.0') #h1-r2
   
    r1.cmd('ifconfig r1-eth0 195.30.0.2 netmask 255.255.255.0') #r1-h1
    r1.cmd('ifconfig r1-eth1 195.30.1.1 netmask 255.255.255.0') #r1-r3
    r1.cmd('ifconfig r1-eth2 195.30.6.1 netmask 255.255.255.0') #r1-r4
   
    r2.cmd('ifconfig r2-eth0 195.30.5.1 netmask 255.255.255.0') #r2-h1
    r2.cmd('ifconfig r2-eth1 195.30.4.2 netmask 255.255.255.0') #r2-r4
    r2.cmd('ifconfig r2-eth2 195.30.7.1 netmask 255.255.255.0') #r2-r3
   
    h2.cmd('ifconfig h2-eth0 195.30.2.2 netmask 255.255.255.0') #h2-r3
    h2.cmd('ifconfig h2-eth1 195.30.3.1 netmask 255.255.255.0') #h2-r4
   
    r3.cmd('ifconfig r3-eth0 195.30.2.1 netmask 255.255.255.0') #r3-h2
    r3.cmd('ifconfig r3-eth1 195.30.1.2 netmask 255.255.255.0') #r3-r1
    r3.cmd('ifconfig r3-eth2 195.30.7.2 netmask 255.255.255.0') #r3-r2
   
    r4.cmd('ifconfig r4-eth0 195.30.3.2 netmask 255.255.255.0') #r4-h2
    r4.cmd('ifconfig r4-eth1 195.30.4.1 netmask 255.255.255.0') #r4-r2
    r4.cmd('ifconfig r4-eth2 195.30.6.2 netmask 255.255.255.0') #r4-r1
    
    #forward semua router
    r1.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
    r2.cmd("echo 2 > /proc/sys/net/ipv4/ip_forward")
    r3.cmd("echo 3 > /proc/sys/net/ipv4/ip_forward")
    r4.cmd("echo 4 > /proc/sys/net/ipv4/ip_forward")
   
    #static routing host
    h1.cmd("ip rule add from 195.30.0.1 table 1")
    h1.cmd("ip rule add from 195.30.5.2 table 2")
    h1.cmd("ip route add 195.30.0.0/24 dev h1-eth0 scope link table 1")
    h1.cmd("ip route add default via 195.30.0.2 dev h1-eth0 table 1")
    h1.cmd("ip route add 195.30.5.0/24 dev h1-eth1 scope link table 2")
    h1.cmd("ip route add default via 195.30.5.1 dev h1-eth1 table 2")
    h1.cmd("ip route add default scope global nexthop via 195.30.0.2 dev h1-eth0")
   
    h2.cmd("ip rule add from 195.30.2.2 table 3")
    h2.cmd("ip rule add from 195.30.3.1 table 4")
    h2.cmd("ip route add 195.30.2.0/24 dev h2-eth0 scope link table 3")
    h2.cmd("ip route add default via 195.30.2.1 dev h2-eth0 table 3")
    h2.cmd("ip route add 195.30.3.0/24 dev h2-eth1 scope link table 4")
    h2.cmd("ip route add default via 195.30.3.2 dev h2-eth1 table 4")
    h2.cmd("ip route add default scope global nexthop via 195.30.2.1 dev h2-eth0")
   
    #static routing router
    r1.cmd("route add -net 195.30.2.0/24 gw 195.30.1.2")
    r1.cmd("route add -net 195.30.3.0/24 gw 195.30.6.2")
    r1.cmd("route add -net 195.30.4.0/24 gw 195.30.6.2")
    r1.cmd("route add -net 195.30.5.0/24 gw 195.30.1.2")
    r1.cmd("route add -net 195.30.7.0/24 gw 195.30.1.2")
   
    r2.cmd("route add -net 195.30.0.0/24 gw 195.30.4.1")
    r2.cmd("route add -net 195.30.1.0/24 gw 195.30.7.2")
    r2.cmd("route add -net 195.30.2.0/24 gw 195.30.7.2")
    r2.cmd("route add -net 195.30.3.0/24 gw 195.30.4.1")
    r2.cmd("route add -net 195.30.6.0/24 gw 195.30.4.1") 
    
    r3.cmd("route add -net 195.30.0.0/24 gw 195.30.1.1")
    r3.cmd("route add -net 195.30.3.0/24 gw 195.30.7.1")
    r3.cmd("route add -net 195.30.4.0/24 gw 195.30.1.1")
    r3.cmd("route add -net 195.30.5.0/24 gw 195.30.7.1")
    r3.cmd("route add -net 195.30.6.0/24 gw 195.30.1.1")   
 
    r4.cmd("route add -net 195.30.0.0/24 gw 195.30.6.1")
    r4.cmd("route add -net 195.30.1.0/24 gw 195.30.6.1")
    r4.cmd("route add -net 195.30.2.0/24 gw 195.30.4.2")
    r4.cmd("route add -net 195.30.5.0/24 gw 195.30.4.2")
    r4.cmd("route add -net 195.30.7.0/24 gw 195.30.4.2")

    '''
    #menjalankan background traffic menggunakan iperf
    h2.cmd('iperf -s &')
    h1.cmd('iperf -t 60 -c 195.30.2.2')
    '''

    #menampilkan informasi ping
    info('\n',net.ping(),'\n')
    
    #menghentikan topologi
    CLI(net)
    net.stop()
    
#main program
if __name__ == '__main__':
    os.system('mn -c')
    os.system('clear')
    setLogLevel('info')
    topology()

