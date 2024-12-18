#!/usr/bin/env python

from mininet.net import Mininet
from mininet.node import Node
from mininet.link import TCLink
from mininet.log import setLogLevel, info
from mininet.cli import CLI
import time

class LinuxRouter(Node):
    """Create a router node with IP forwarding enabled."""
    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        self.cmd('sysctl net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()

def run():
    net = Mininet(topo=None, build=False, link=TCLink)

    # Add routers
    r1 = net.addHost('r1', cls=LinuxRouter, ip='192.168.1.1/24', mac='00:00:00:00:01:01')
    r2 = net.addHost('r2', cls=LinuxRouter, ip='192.168.2.2/24', mac='00:00:00:00:02:02')
    r3 = net.addHost('r3', cls=LinuxRouter, ip='192.168.3.2/24', mac='00:00:00:00:03:03')
    r4 = net.addHost('r4', cls=LinuxRouter, ip='192.168.4.2/24', mac='00:00:00:00:04:04')

    # Add hosts
    h1 = net.addHost('h1', ip='192.168.1.2/24', mac='00:00:00:00:01:02')
    h2 = net.addHost('h2', ip='192.168.5.2/24', mac='00:00:00:00:05:02')

    # Add links with specified bandwidth
    # Link with 1 Mbps bandwidth
    net.addLink(h1, r1, cls=TCLink, bw=1,
                intfName1='h1-eth0', intfName2='r1-eth0',
                params1={'ip': '192.168.1.2/24'}, params2={'ip': '192.168.1.1/24'})
    
    net.addLink(r1, r2, cls=TCLink, bw=1,
                intfName1='r1-eth1', intfName2='r2-eth0',
                params1={'ip': '192.168.2.1/24'}, params2={'ip': '192.168.2.2/24'})
    
    # Link with 0.5 Mbps bandwidth
    net.addLink(r2, r3, cls=TCLink, bw=0.5,
                intfName1='r2-eth1', intfName2='r3-eth0',
                params1={'ip': '192.168.3.1/24'}, params2={'ip': '192.168.3.2/24'})
    
    net.addLink(r3, r4, cls=TCLink, bw=0.5,
                intfName1='r3-eth1', intfName2='r4-eth0',
                params1={'ip': '192.168.4.1/24'}, params2={'ip': '192.168.4.2/24'})
    
    net.addLink(r4, h2, cls=TCLink, bw=1,
                intfName1='r4-eth1', intfName2='h2-eth0',
                params1={'ip': '192.168.5.1/24'}, params2={'ip': '192.168.5.2/24'})

    # Add additional links for mesh topology
    net.addLink(r1, r3, cls=TCLink, bw=1,
                intfName1='r1-eth2', intfName2='r3-eth2',
                params1={'ip': '192.168.6.1/24'}, params2={'ip': '192.168.6.2/24'})
    
    net.addLink(r2, r4, cls=TCLink, bw=1,
                intfName1='r2-eth2', intfName2='r4-eth2',
                params1={'ip': '192.168.7.1/24'}, params2={'ip': '192.168.7.2/24'})

    net.start()

    # Configure routing for routers
    r1.cmd('ip route add 192.168.3.0/24 via 192.168.2.2')
    r1.cmd('ip route add 192.168.4.0/24 via 192.168.2.2')
    r1.cmd('ip route add 192.168.5.0/24 via 192.168.2.2')
    r1.cmd('ip route add 192.168.6.0/24 via 192.168.6.2')
    r1.cmd('ip route add 192.168.7.0/24 via 192.168.2.2')

    r2.cmd('ip route add 192.168.1.0/24 via 192.168.2.1')
    r2.cmd('ip route add 192.168.4.0/24 via 192.168.3.2')
    r2.cmd('ip route add 192.168.5.0/24 via 192.168.3.2')
    r2.cmd('ip route add 192.168.6.0/24 via 192.168.3.2')
    r2.cmd('ip route add 192.168.7.0/24 via 192.168.7.2')

    r3.cmd('ip route add 192.168.1.0/24 via 192.168.3.1')
    r3.cmd('ip route add 192.168.2.0/24 via 192.168.3.1')
    r3.cmd('ip route add 192.168.5.0/24 via 192.168.4.2')
    r3.cmd('ip route add 192.168.6.0/24 via 192.168.6.1')
    r3.cmd('ip route add 192.168.7.0/24 via 192.168.4.2')

    r4.cmd('ip route add 192.168.1.0/24 via 192.168.4.1')
    r4.cmd('ip route add 192.168.2.0/24 via 192.168.4.1')
    r4.cmd('ip route add 192.168.3.0/24 via 192.168.4.1')
    r4.cmd('ip route add 192.168.6.0/24 via 192.168.3.2')
    r4.cmd('ip route add 192.168.7.0/24 via 192.168.7.1')

    # Add routes for the 192.168.6.0/24 network
    r2.cmd('ip route add 192.168.6.0/24 via 192.168.7.2')
    r4.cmd('ip route add 192.168.6.0/24 via 192.168.7.1')

    # Configure default gateway for hosts
    h1.cmd('ip route add default via 192.168.1.1')
    h2.cmd('ip route add default via 192.168.5.1')

    # Implement policy-based routing for hosts
    h1.cmd('ip rule add from 192.168.1.2 table 1')
    h1.cmd('ip route add 192.168.1.0/24 dev h1-eth0 scope link table 1')
    h1.cmd('ip route add default via 192.168.1.1 table 1')

    h2.cmd('ip rule add from 192.168.5.2 table 2')
    h2.cmd('ip route add 192.168.5.0/24 dev h2-eth0 scope link table 2')
    h2.cmd('ip route add default via 192.168.5.1 table 2')

    # Function to test connectivity
    def test_connectivity():
        info('*** Testing connectivity:\n')
        hosts = [h1, h2]
        routers = [r1, r2, r3, r4]
        
        info(f'\n')
        net.pingAll()
        info(f'\n')

        # Test connectivity from hosts to routers
        for host in hosts:
            for router in routers:
                for intf in router.intfs.values():
                    if intf.IP():
                        result = host.cmd(f'ping -c 1 -W 1 {intf.IP()}')
                        if '1 received' in result:
                            info(f'{host.name} -> {router.name} ({intf.IP()}): OK\n')
                        else:
                            info(f'{host.name} -> {router.name} ({intf.IP()}): FAILED\n')
                info(f'\n')

        # Test connectivity from routers to hosts
        for router in routers:
            for host in hosts:
                for intf in host.intfs.values():
                    if intf.IP():
                        result = router.cmd(f'ping -c 1 -W 1 {intf.IP()}')
                        if '1 received' in result:
                            info(f'{router.name} -> {host.name} ({intf.IP()}): OK\n')
                        else:
                            info(f'{router.name} -> {host.name} ({intf.IP()}): FAILED\n')
            info(f'\n')
        
    def test_traffic():
        info('*** Testing bandwidth between hosts:\n')
        # Start iperf server on h2
        h2.cmd('iperf -s &')
        # Wait for server to start
        time.sleep(1)
        # Run iperf client on h1
        result = h1.cmd('iperf -c ' + h2.IP() + ' -t 10')
        info(result)
        # Kill iperf server
        h2.cmd('killall -9 iperf')

    # Run connectivity tests
    info('*** Running connectivity test\n')
    time.sleep(2)  # Wait for routing tables to update
    test_connectivity()
    
    info('*** Running traffic simulation\n')
    test_traffic()

    info('*** Running CLI\n')
    CLI(net)
    
    info('*** Stopping network\n')
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()