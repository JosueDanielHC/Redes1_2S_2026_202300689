# Código fuente — Práctica 2

**Estudiante:** Josue Daniel Herrera Cottom  
**Carné:** 202300689  
**Simulador:** Cisco Packet Tracer  
**Contraseña de consola y VTY:** `cisco`  
**Contraseña de modo privilegiado:** `class`  
**Dominio VTP:** `202300689`  
**Contraseña VTP:** `cisco123`

Los bloques de abajo son la configuración final que quedó operando. En CORE y en Z1-SWP el EtherChannel se aplica con el orden que sí negoció PAgP: primero el grupo, y después la VLAN nativa 99 solo en `Port-channel1`.

---

## CORE (3560-24PS) — VTP transparente, root de las VLAN 1 y 99

```text
enable
configure terminal
hostname CORE
banner motd #Complejo Cayala - Josue Daniel Herrera Cotton - 202300689#
service password-encryption
no ip domain-lookup
enable secret class
line console 0
 password cisco
 login
 logging synchronous
 exit
line vty 0 4
 password cisco
 login
 logging synchronous
 exit
vtp domain 202300689
vtp password cisco123
vtp version 2
vtp mode transparent
vlan 19
 name Paseo_Cayala
vlan 29
 name Distrito_Residencial
vlan 39
 name Parque_Cayala
vlan 49
 name Distrito_Corporativo
vlan 59
 name Administracion_Seguridad
vlan 99
 name Nativa_Administracion
vlan 999
 name Blackhole
exit
spanning-tree mode rapid-pvst
spanning-tree vlan 1 priority 4096
spanning-tree vlan 99 priority 4096
spanning-tree vlan 19,29,39,49,59 priority 8192
interface range FastEthernet0/1-6
 switchport
 switchport trunk encapsulation dot1q
 switchport mode trunk
 switchport trunk native vlan 99
 switchport nonegotiate
 no shutdown
 exit
interface FastEthernet0/1
 switchport trunk allowed vlan 1,29,99
 exit
interface FastEthernet0/2
 switchport trunk allowed vlan 1,39,99
 exit
interface range FastEthernet0/3-4
 switchport trunk allowed vlan 1,59,99
 exit
interface range FastEthernet0/5-6
 switchport trunk allowed vlan 1,49,99
 exit
interface range GigabitEthernet0/1-2
 switchport
 switchport trunk encapsulation dot1q
 switchport mode trunk
 channel-protocol pagp
 channel-group 1 mode desirable
 no shutdown
 exit
interface Port-channel1
 switchport trunk encapsulation dot1q
 switchport mode trunk
 switchport trunk native vlan 99
 switchport trunk allowed vlan 1,19,99
 exit
interface range FastEthernet0/7-24
 switchport
 switchport mode access
 switchport access vlan 999
 switchport nonegotiate
 shutdown
 exit
interface Vlan1
 shutdown
 exit
interface Vlan99
 ip address 192.168.89.1 255.255.255.0
 no shutdown
 exit
ip routing
end
write memory
```

## Z1-SWP (3560-24PS) — servidor VTP, root de la VLAN 19, EtherChannel PAgP

```text
enable
configure terminal
hostname Z1-SWP
banner motd #Paseo Cayala - principal - Josue Daniel Herrera Cotton - 202300689#
service password-encryption
no ip domain-lookup
enable secret class
line console 0
 password cisco
 login
 logging synchronous
 exit
line vty 0 4
 password cisco
 login
 logging synchronous
 exit
vtp domain 202300689
vtp password cisco123
vtp version 2
vtp mode server
vlan 19
 name Paseo_Cayala
vlan 29
 name Distrito_Residencial
vlan 39
 name Parque_Cayala
vlan 49
 name Distrito_Corporativo
vlan 59
 name Administracion_Seguridad
vlan 99
 name Nativa_Administracion
vlan 999
 name Blackhole
exit
spanning-tree mode rapid-pvst
spanning-tree vlan 19 priority 4096
no ip routing
ip default-gateway 192.168.89.1
interface FastEthernet0/1
 switchport
 switchport trunk encapsulation dot1q
 switchport mode trunk
 switchport trunk native vlan 99
 switchport trunk allowed vlan 1,19,99
 switchport nonegotiate
 no shutdown
 exit
interface FastEthernet0/24
 switchport
 switchport trunk encapsulation dot1q
 switchport mode trunk
 switchport trunk native vlan 99
 switchport trunk allowed vlan 1,19,49,99
 switchport nonegotiate
 no shutdown
 exit
interface range GigabitEthernet0/1-2
 switchport
 switchport trunk encapsulation dot1q
 switchport mode trunk
 channel-protocol pagp
 channel-group 1 mode desirable
 no shutdown
 exit
interface Port-channel1
 switchport trunk encapsulation dot1q
 switchport mode trunk
 switchport trunk native vlan 99
 switchport trunk allowed vlan 1,19,99
 exit
interface range FastEthernet0/2-23
 switchport
 switchport mode access
 switchport access vlan 999
 switchport nonegotiate
 shutdown
 exit
interface Vlan1
 shutdown
 exit
interface Vlan99
 ip address 192.168.89.2 255.255.255.0
 no shutdown
 exit
end
write memory
```

## Z4-SWP (3560-24PS) — servidor VTP, root de la VLAN 49

```text
enable
configure terminal
hostname Z4-SWP
banner motd #Distrito Corporativo - principal - Josue Daniel Herrera Cotton - 202300689#
service password-encryption
no ip domain-lookup
enable secret class
line console 0
 password cisco
 login
 logging synchronous
 exit
line vty 0 4
 password cisco
 login
 logging synchronous
 exit
vtp domain 202300689
vtp password cisco123
vtp version 2
vtp mode server
vlan 19
 name Paseo_Cayala
vlan 29
 name Distrito_Residencial
vlan 39
 name Parque_Cayala
vlan 49
 name Distrito_Corporativo
vlan 59
 name Administracion_Seguridad
vlan 99
 name Nativa_Administracion
vlan 999
 name Blackhole
exit
spanning-tree mode rapid-pvst
spanning-tree vlan 49 priority 4096
no ip routing
ip default-gateway 192.168.89.1
interface FastEthernet0/1
 switchport
 switchport trunk encapsulation dot1q
 switchport mode trunk
 switchport trunk native vlan 99
 switchport trunk allowed vlan 1,49,99
 switchport nonegotiate
 no shutdown
 exit
interface FastEthernet0/22
 switchport
 switchport trunk encapsulation dot1q
 switchport mode trunk
 switchport trunk native vlan 99
 switchport trunk allowed vlan 1,19,49,99
 switchport nonegotiate
 no shutdown
 exit
interface range FastEthernet0/23-24
 switchport
 switchport trunk encapsulation dot1q
 switchport mode trunk
 switchport trunk native vlan 99
 switchport trunk allowed vlan 1,49,99
 switchport nonegotiate
 no shutdown
 exit
interface range FastEthernet0/2-21
 switchport
 switchport mode access
 switchport access vlan 999
 switchport nonegotiate
 shutdown
 exit
interface range GigabitEthernet0/1-2
 switchport
 switchport mode access
 switchport access vlan 999
 switchport nonegotiate
 shutdown
 exit
interface Vlan1
 shutdown
 exit
interface Vlan99
 ip address 192.168.89.5 255.255.255.0
 no shutdown
 exit
end
write memory
```

## Z2-SWP (2960-24TT) — servidor VTP, root de la VLAN 29

```text
enable
configure terminal
hostname Z2-SWP
banner motd #Distrito Residencial - principal - Josue Daniel Herrera Cotton - 202300689#
service password-encryption
no ip domain-lookup
enable secret class
line console 0
 password cisco
 login
 logging synchronous
 exit
line vty 0 4
 password cisco
 login
 logging synchronous
 exit
vtp domain 202300689
vtp password cisco123
vtp version 2
vtp mode server
vlan 19
 name Paseo_Cayala
vlan 29
 name Distrito_Residencial
vlan 39
 name Parque_Cayala
vlan 49
 name Distrito_Corporativo
vlan 59
 name Administracion_Seguridad
vlan 99
 name Nativa_Administracion
vlan 999
 name Blackhole
exit
spanning-tree mode rapid-pvst
spanning-tree vlan 29 priority 4096
ip default-gateway 192.168.89.1
interface FastEthernet0/1
 switchport mode trunk
 switchport trunk native vlan 99
 switchport trunk allowed vlan 1,29,99
 switchport nonegotiate
 no shutdown
 exit
interface FastEthernet0/24
 switchport mode trunk
 switchport trunk native vlan 99
 switchport trunk allowed vlan 1,29,99
 switchport nonegotiate
 no shutdown
 exit
interface range FastEthernet0/2-23
 switchport mode access
 switchport access vlan 999
 switchport nonegotiate
 shutdown
 exit
interface range GigabitEthernet0/1-2
 switchport mode access
 switchport access vlan 999
 switchport nonegotiate
 shutdown
 exit
interface Vlan1
 shutdown
 exit
interface Vlan99
 ip address 192.168.89.3 255.255.255.0
 no shutdown
 exit
end
write memory
```

## Z3-SWP (2960-24TT) — servidor VTP, root de la VLAN 39

```text
enable
configure terminal
hostname Z3-SWP
banner motd #Parque Cayala - principal - Josue Daniel Herrera Cotton - 202300689#
service password-encryption
no ip domain-lookup
enable secret class
line console 0
 password cisco
 login
 logging synchronous
 exit
line vty 0 4
 password cisco
 login
 logging synchronous
 exit
vtp domain 202300689
vtp password cisco123
vtp version 2
vtp mode server
vlan 19
 name Paseo_Cayala
vlan 29
 name Distrito_Residencial
vlan 39
 name Parque_Cayala
vlan 49
 name Distrito_Corporativo
vlan 59
 name Administracion_Seguridad
vlan 99
 name Nativa_Administracion
vlan 999
 name Blackhole
exit
spanning-tree mode rapid-pvst
spanning-tree vlan 39 priority 4096
ip default-gateway 192.168.89.1
interface FastEthernet0/1
 switchport mode trunk
 switchport trunk native vlan 99
 switchport trunk allowed vlan 1,39,99
 switchport nonegotiate
 no shutdown
 exit
interface FastEthernet0/24
 switchport mode trunk
 switchport trunk native vlan 99
 switchport trunk allowed vlan 1,39,99
 switchport nonegotiate
 no shutdown
 exit
interface range FastEthernet0/2-23
 switchport mode access
 switchport access vlan 999
 switchport nonegotiate
 shutdown
 exit
interface range GigabitEthernet0/1-2
 switchport mode access
 switchport access vlan 999
 switchport nonegotiate
 shutdown
 exit
interface Vlan1
 shutdown
 exit
interface Vlan99
 ip address 192.168.89.4 255.255.255.0
 no shutdown
 exit
end
write memory
```

## Z5-SWP (2960-24TT) — servidor VTP, root de la VLAN 59

```text
enable
configure terminal
hostname Z5-SWP
banner motd #Administracion y Seguridad - principal - Josue Daniel Herrera Cotton - 202300689#
service password-encryption
no ip domain-lookup
enable secret class
line console 0
 password cisco
 login
 logging synchronous
 exit
line vty 0 4
 password cisco
 login
 logging synchronous
 exit
vtp domain 202300689
vtp password cisco123
vtp version 2
vtp mode server
vlan 19
 name Paseo_Cayala
vlan 29
 name Distrito_Residencial
vlan 39
 name Parque_Cayala
vlan 49
 name Distrito_Corporativo
vlan 59
 name Administracion_Seguridad
vlan 99
 name Nativa_Administracion
vlan 999
 name Blackhole
exit
spanning-tree mode rapid-pvst
spanning-tree vlan 59 priority 4096
ip default-gateway 192.168.89.1
interface FastEthernet0/1
 switchport mode trunk
 switchport trunk native vlan 99
 switchport trunk allowed vlan 1,59,99
 switchport nonegotiate
 no shutdown
 exit
interface range FastEthernet0/23-24
 switchport mode trunk
 switchport trunk native vlan 99
 switchport trunk allowed vlan 1,59,99
 switchport nonegotiate
 no shutdown
 exit
interface range FastEthernet0/2-22
 switchport mode access
 switchport access vlan 999
 switchport nonegotiate
 shutdown
 exit
interface range GigabitEthernet0/1-2
 switchport mode access
 switchport access vlan 999
 switchport nonegotiate
 shutdown
 exit
interface Vlan1
 shutdown
 exit
interface Vlan99
 ip address 192.168.89.6 255.255.255.0
 no shutdown
 exit
end
write memory
```

## Z1-SWA (2960-24TT) — cliente VTP, VLAN 19

```text
enable
configure terminal
hostname Z1-SWA
banner motd #Paseo Cayala - acceso - Josue Daniel Herrera Cotton - 202300689#
service password-encryption
no ip domain-lookup
enable secret class
line console 0
 password cisco
 login
 logging synchronous
 exit
line vty 0 4
 password cisco
 login
 logging synchronous
 exit
vtp domain 202300689
vtp password cisco123
vtp version 2
vtp mode client
spanning-tree mode rapid-pvst
interface FastEthernet0/24
 switchport mode trunk
 switchport trunk native vlan 99
 switchport trunk allowed vlan 1,19,99
 switchport nonegotiate
 no shutdown
 exit
interface range FastEthernet0/1-3
 switchport mode access
 switchport access vlan 19
 switchport nonegotiate
 spanning-tree portfast
 spanning-tree bpduguard enable
 no shutdown
 exit
interface range FastEthernet0/4-23
 switchport mode access
 switchport access vlan 999
 switchport nonegotiate
 shutdown
 exit
interface range GigabitEthernet0/1-2
 switchport mode access
 switchport access vlan 999
 switchport nonegotiate
 shutdown
 exit
end
write memory
```

## Z2-SWA (2960-24TT) — cliente VTP, VLAN 29

```text
enable
configure terminal
hostname Z2-SWA
banner motd #Distrito Residencial - acceso - Josue Daniel Herrera Cotton - 202300689#
service password-encryption
no ip domain-lookup
enable secret class
line console 0
 password cisco
 login
 logging synchronous
 exit
line vty 0 4
 password cisco
 login
 logging synchronous
 exit
vtp domain 202300689
vtp password cisco123
vtp version 2
vtp mode client
spanning-tree mode rapid-pvst
interface FastEthernet0/24
 switchport mode trunk
 switchport trunk native vlan 99
 switchport trunk allowed vlan 1,29,99
 switchport nonegotiate
 no shutdown
 exit
interface range FastEthernet0/1-2
 switchport mode access
 switchport access vlan 29
 switchport nonegotiate
 spanning-tree portfast
 spanning-tree bpduguard enable
 no shutdown
 exit
interface range FastEthernet0/3-23
 switchport mode access
 switchport access vlan 999
 switchport nonegotiate
 shutdown
 exit
interface range GigabitEthernet0/1-2
 switchport mode access
 switchport access vlan 999
 switchport nonegotiate
 shutdown
 exit
end
write memory
```

## Z3-SWA (2960-24TT) — cliente VTP, VLAN 39

```text
enable
configure terminal
hostname Z3-SWA
banner motd #Parque Cayala - acceso - Josue Daniel Herrera Cotton - 202300689#
service password-encryption
no ip domain-lookup
enable secret class
line console 0
 password cisco
 login
 logging synchronous
 exit
line vty 0 4
 password cisco
 login
 logging synchronous
 exit
vtp domain 202300689
vtp password cisco123
vtp version 2
vtp mode client
spanning-tree mode rapid-pvst
interface FastEthernet0/24
 switchport mode trunk
 switchport trunk native vlan 99
 switchport trunk allowed vlan 1,39,99
 switchport nonegotiate
 no shutdown
 exit
interface range FastEthernet0/1-2
 switchport mode access
 switchport access vlan 39
 switchport nonegotiate
 spanning-tree portfast
 spanning-tree bpduguard enable
 no shutdown
 exit
interface range FastEthernet0/3-23
 switchport mode access
 switchport access vlan 999
 switchport nonegotiate
 shutdown
 exit
interface range GigabitEthernet0/1-2
 switchport mode access
 switchport access vlan 999
 switchport nonegotiate
 shutdown
 exit
end
write memory
```

## Z4-SWA (2960-24TT) — cliente VTP, VLAN 49

```text
enable
configure terminal
hostname Z4-SWA
banner motd #Distrito Corporativo - acceso - Josue Daniel Herrera Cotton - 202300689#
service password-encryption
no ip domain-lookup
enable secret class
line console 0
 password cisco
 login
 logging synchronous
 exit
line vty 0 4
 password cisco
 login
 logging synchronous
 exit
vtp domain 202300689
vtp password cisco123
vtp version 2
vtp mode client
spanning-tree mode rapid-pvst
interface FastEthernet0/24
 switchport mode trunk
 switchport trunk native vlan 99
 switchport trunk allowed vlan 1,49,99
 switchport nonegotiate
 no shutdown
 exit
interface range FastEthernet0/1-3
 switchport mode access
 switchport access vlan 49
 switchport nonegotiate
 spanning-tree portfast
 spanning-tree bpduguard enable
 no shutdown
 exit
interface range FastEthernet0/4-23
 switchport mode access
 switchport access vlan 999
 switchport nonegotiate
 shutdown
 exit
interface range GigabitEthernet0/1-2
 switchport mode access
 switchport access vlan 999
 switchport nonegotiate
 shutdown
 exit
end
write memory
```

## Z5-SWA (2960-24TT) — cliente VTP, VLAN 59

```text
enable
configure terminal
hostname Z5-SWA
banner motd #Administracion y Seguridad - acceso - Josue Daniel Herrera Cotton - 202300689#
service password-encryption
no ip domain-lookup
enable secret class
line console 0
 password cisco
 login
 logging synchronous
 exit
line vty 0 4
 password cisco
 login
 logging synchronous
 exit
vtp domain 202300689
vtp password cisco123
vtp version 2
vtp mode client
spanning-tree mode rapid-pvst
interface FastEthernet0/24
 switchport mode trunk
 switchport trunk native vlan 99
 switchport trunk allowed vlan 1,59,99
 switchport nonegotiate
 no shutdown
 exit
interface range FastEthernet0/1-2
 switchport mode access
 switchport access vlan 59
 switchport nonegotiate
 spanning-tree portfast
 spanning-tree bpduguard enable
 no shutdown
 exit
interface range FastEthernet0/3-23
 switchport mode access
 switchport access vlan 999
 switchport nonegotiate
 shutdown
 exit
interface range GigabitEthernet0/1-2
 switchport mode access
 switchport access vlan 999
 switchport nonegotiate
 shutdown
 exit
end
write memory
```
