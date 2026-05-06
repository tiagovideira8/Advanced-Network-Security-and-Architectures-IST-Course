# Advanced-Network-Security-and-Architectures-IST-Course

Repository containing all laboratory assignments and individual projects developed for the SAAR course at Instituto Superior Técnico (IST).

# Lab 1 - Network Attacks and Countermeasures

This laboratory assignment explores common network attacks and the mechanisms used to prevent them in modern networks.

## Topics Covered

* MAC Table Overflow
* DHCP Spoofing
* ARP Poisoning (Man-in-the-Middle)
* DNS Spoofing
* RIP Poisoning

## Objectives

* Understand how each attack works
* Analyze packet behavior using Wireshark
* Configure network security mechanisms
* Evaluate the effectiveness and feasibility of each attack

## Tools Used

* GNS3
* Wireshark
* Cisco IOSvL2
* Cisco c3725
* VPCS
* saar-tools container

## Notes for the report

### RIP Poisoning

#### How RIP normally works

Routers periodically send RIP Response messages (every ~30s)

These messages contain:
- Destination networks
- Metric (hop count)
- Routers pick routes based on:
- Lowest metric (shortest path)
- Longest prefix match (more specific route wins)

#### What the attacker does

The attacker sends fake RIP responses claiming:

“Hey, I have a better route to the Web Server!”

Two main tricks:

1. Lower metric attack
- Advertise same network with smaller hop count
- Router prefers attacker

2. Longest prefix match (more powerful)
- Advertise more specific subnet
- Legit: 10.0.0.0/24
- Attacker: 10.0.0.0/25
- Router prefers attacker even if metric is worse

#### What to capture (important for report)

Use:
- Wireshark
- Cisco CLI
- Browser screenshots

Show:
- Normal RIP updates
- Fake RIP packets
- Routing table BEFORE / AFTER
- Browser redirection

#### AI prediction (for your report)

AI predicts that:
-Longer prefix → preferred route
-Auto-summary reduces attack effectiveness

👉 Then compare with your results.

#### Final insight (for your discussion)

This attack works because:
- RIP has no integrity by default
- Trusts any received update
- No validation of source

#### Feasibility (your opinion section)

Real-world:
- ❌ Rare today (RIP mostly obsolete)
- ✅ Still relevant conceptually:

Similar attacks exist in:
- BGP hijacking
- OSPF attacks

### What to write on the auto summary ON/OFF section

What SHOULD happen (in theory)

If auto-summary interferes, you might see:  
| Scenario               | Expected Effect                |
| ---------------------- | ------------------------------ |
| Attacker sends `/25`   | Gets summarized → becomes `/8` |
| Router compares routes | Loses specificity advantage    |
| Result                 | Attack may fail                |

What YOU are seeing

    “Nothing changed, attack worked the same”

That means:
- Your /25 route is NOT being summarized
- Routers are still receiving and using it as /25

**Why auto-summary has no effect here**

This is the key insight for your report.

Auto-summary only matters when:

    Routes cross major network boundaries

In your lab:
- All relevant networks are already cleanly separated:
- 10.0.0.0/24
- 172.16.0.0/24
- 192.168.x.x

👉 There’s no ambiguous classful boundary being crossed

**What you should conclude (VERY IMPORTANT for report)**

Instead of forcing a difference, explain this:

    “In our topology, enabling auto-summary did not affect the attack because the injected route did not cross a classful boundary where summarization would apply.”

### Commands used and results for second firewall exercise

**interface configuration**

conf t

interface f0/0
 ip address 10.1.1.254 255.255.255.0
 no shut

interface f1/0
 ip address 10.2.2.254 255.255.255.0
 no shut

interface f2/0
 ip address 172.16.0.254 255.255.255.0
 no shut

interface f3/0
 ip address 200.0.0.254 255.255.255.0
 no shut

end

**define inside/outside**

conf t

interface f0/0
 ip nat inside

interface f1/0
 ip nat inside

interface f3/0
 ip nat outside

**ACL and NAT overload**

ip access-list standard NAT_INSIDE
 permit 10.0.0.0 0.255.255.255

exit

ip nat inside source list NAT_INSIDE interface f3/0 overload

**Sanity check**

From PR1:

ping 200.0.0.10

Then on firewall:

show ip nat translations

✔ You MUST see translation like:

10.1.1.10 → 200.0.0.254

**Define zones**

conf t

zone security PR1
zone security PR2
zone security DMZ
zone security OUT

**assign interfaces**

interface f0/0
 zone-member security PR1

interface f1/0
 zone-member security PR2

interface f2/0
 zone-member security DMZ

interface f3/0
 zone-member security OUT

end

**PR->OUT Policy**

**ACL**

conf t

ip access-list extended PR_TO_OUT
 permit tcp any any eq 80
 permit tcp any any eq 443
 permit udp any any eq 53
 permit icmp any any

**Class map**

class-map type inspect match-any PR_OUT_CLASS
 match access-group name PR_TO_OUT

**Policy**

policy-map type inspect PR_OUT_POLICY
 class type inspect PR_OUT_CLASS
  inspect
 class class-default
  drop

**Apply**

zone-pair security PR1_TO_OUT source PR1 destination OUT
 service-policy type inspect PR_OUT_POLICY

zone-pair security PR2_TO_OUT source PR2 destination OUT
 service-policy type inspect PR_OUT_POLICY

**PR-DMZ**

**ACL**

conf t

ip access-list extended PR_TO_DMZ
 permit icmp any host 172.16.0.10
 permit icmp any host 172.16.0.20
 permit icmp any host 172.16.0.30

 permit tcp any host 172.16.0.10 eq 80
 permit tcp any host 172.16.0.10 eq 443

 permit tcp any host 172.16.0.20 eq 25
 permit tcp any host 172.16.0.20 eq 110
 permit tcp any host 172.16.0.20 eq 143

 permit udp any host 172.16.0.30 eq 53
 permit tcp any host 172.16.0.30 eq 53

**Class-map**

class-map type inspect match-any PR_DMZ_CLASS
 match access-group name PR_TO_DMZ

**Policy**

policy-map type inspect PR_DMZ_POLICY
 class type inspect PR_DMZ_CLASS
  inspect
 class class-default
  drop

**Apply**

zone-pair security PR1_TO_DMZ source PR1 destination DMZ
 service-policy type inspect PR_DMZ_POLICY

zone-pair security PR2_TO_DMZ source PR2 destination DMZ
 service-policy type inspect PR_DMZ_POLICY

### Test results (second exercise of the firewalls lab)

PR1->OUT and then PR1->DMZ:

root@PR1:/# nmap 200.0.0.10
Starting Nmap 7.80 ( https://nmap.org ) at 2026-05-06 11:19 UTC
mass_dns: warning: Unable to determine any DNS servers. Reverse DNS is disabled. Try using --system-dns or specify valid servers with --dns-servers
Nmap scan report for 200.0.0.10
Host is up (0.020s latency).
Not shown: 998 filtered ports
PORT    STATE  SERVICE
80/tcp  closed http
443/tcp closed https

Nmap done: 1 IP address (1 host up) scanned in 4.58 seconds
root@PR1:/# nmap 172.16.0.10
Starting Nmap 7.80 ( https://nmap.org ) at 2026-05-06 11:19 UTC
mass_dns: warning: Unable to determine any DNS servers. Reverse DNS is disabled. Try using --system-dns or specify valid servers with --dns-servers
Nmap scan report for 172.16.0.10
Host is up (0.016s latency).
Not shown: 998 filtered ports
PORT    STATE SERVICE
80/tcp  open  http
443/tcp open  https

Nmap done: 1 IP address (1 host up) scanned in 4.57 seconds

wireshark capture screenshot:

../Images/nmap_PR_to_DMZ(working proof).png

PR->PR

root@PR1:/# nmap 10.2.2.10
Starting Nmap 7.80 ( https://nmap.org ) at 2026-05-06 11:21 UTC
mass_dns: warning: Unable to determine any DNS servers. Reverse DNS is disabled. Try using --system-dns or specify valid servers with --dns-servers
Note: Host seems down. If it is really up, but blocking our ping probes, try -Pn
Nmap done: 1 IP address (0 hosts up) scanned in 3.10 seconds
root@PR1:/# nmap -Pn 10.2.2.10
Starting Nmap 7.80 ( https://nmap.org ) at 2026-05-06 11:21 UTC
mass_dns: warning: Unable to determine any DNS servers. Reverse DNS is disabled. Try using --system-dns or specify valid servers with --dns-servers

root@PR1:/# 

Wireshark capute screenshot:

../Images/Nmap_PR_to_PR(no replies).png

PR → OUT (NAT proof)

root@PR1:/# nmap -Pn 200.0.0.10
Starting Nmap 7.80 ( https://nmap.org ) at 2026-05-06 11:26 UTC
mass_dns: warning: Unable to determine any DNS servers. Reverse DNS is disabled. Try using --system-dns or specify valid servers with --dns-servers
Nmap scan report for 200.0.0.10
Host is up (0.015s latency).
Not shown: 998 filtered ports
PORT    STATE  SERVICE
80/tcp  closed http
443/tcp closed https

Nmap done: 1 IP address (1 host up) scanned in 6.43 seconds

Wireshark capute screenshot:

../Images/Nmap_PR_to_OUT(NAT proof).png

Configuration ssh on firewall:

line vty 0 4
 transport input ssh
 login local

username admin secret cisco
ip domain-name lab.local
crypto key generate rsa



Access to firewall via ssh on PR1:

root@PR1:/# ssh -o KexAlgorithms=+diffie-hellman-group14-sha1 \
>     -o HostKeyAlgorithms=+ssh-rsa \
>     -o Ciphers=+aes128-cbc \
>     admin@10.1.1.254
The authenticity of host '10.1.1.254 (10.1.1.254)' can't be established.
RSA key fingerprint is SHA256:6d604yy3K7nXktvI7R3hnSa7Sbk6n0O3hWh9gPm1ky8.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.1.1.254' (RSA) to the list of known hosts.
Password: 

Firewall>
Firewall>exit
Connection to 10.1.1.254 closed by remote host.
Connection to 10.1.1.254 closed.