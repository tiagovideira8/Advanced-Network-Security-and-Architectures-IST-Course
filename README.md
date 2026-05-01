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