 ### ansible-networkd
 
---
 Configure interface with DHCP
```
  - networkd:
      conf_type: network
      name: eth1
      dhcp: yes
      state: present
```
 Configure interface with multiple addresses
```
  - networkd:
      conf_type: network
      name: eth0
      dhcp: yes
      addresses: 192.168.1.5/24 192.168.1.6/24 192.168.1.7/24
      state: present
```
 Configure interface with multiple routes
```
  - networkd:
        config_type=network
        name=eth0
        routes="to=0.0.0.0/0 via=5.0.0.1 metric=100, to=192.168.4.0/24 via=192.168.5.2 metric=100"
        state=present
 ```
 Bridge with two ports
```
  - networkd:
      conf_type: netdev
      name: brtest
      kind: bridge
      state: present
  - networkd:
      conf_type: network
      name: eth1
      master_bridge: brtest
      state: present
  - networkd:
      conf_type: network
      name: eth2
      master_bridge: brtest
      state: present
```
 Bond network
```
  - networkd:
       config_type=netdev
       name=bond1
       kind=bond
       bond_mode=active-backup
       state=present
  - networkd:
       config_type=network
       name=eth0
       master_bond=bond1
       state=present
  - networkd:
       config_type=network
       name=eth1
       master_bond=bond1
       state=present
  - networkd:
       config_type=network
       name=bond1
       dhcp=yes
       state=present
 ```
ipip tunnel
```
  - networkd:
        config_type=netdev
        name=ipip-t
        kind=ipip
        tunnel_local=192.168.1.1
        tunnel_remote=192.168.1.3
        state=present
  - networkd:
        config_type=network
        name=eth0
        tunnel_device=ipip-t
        state=present
 ```
 Tunnel independent
 ```
  - networkd:
        config_type=netdev
        name=ipip-t
        kind=ipip
        tunnel_local=192.168.1.1
        tunnel_remote=192.168.1.3
        tunnel_create_independent=true
        state=present
 ```
 VLan
 
 1
```
  - networkd:
        config_type=netdev
        name=eth0.11
        kind=vlan
        vlan_id=11
        state=present
 ```
 2
 
 ```
  - networkd:
        config_type=netdev
        name=eth0.12
        kind=vlan
        vlan_id=12
        state=present
```
  3
  
```
  - networkd:
        config_type=network
        name=eth0
        vlan_device="eth0.11 eth0.12"
        state=present
```
 VxLan
```
  - networkd:
        config_type=netdev
        name=vxlan-test
        kind=vxlan
        vxlan_id=13
        vxlan_local=192.168.1.1
        vxlan_remote=192.168.1.3
```
