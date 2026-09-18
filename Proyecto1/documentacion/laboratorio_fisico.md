# Laboratorio físico — dos switches (pareja)

**Switch 1 (Josue, 202300689):** VTP Server / Core  
**Switch 2 (Oscar, 202308486):** VTP Client / distribución-acceso

VLAN del carné de Josue (quien simuló): 19, 29, 39, 49, 59, nativa 99. Dominio `Smart_8`. Password `proyecto12S2026`.

Si el auxiliar pide el carné de Oscar, recalcular X y # de **202308486** (par → LACP y PVST). En la defensa de la simulación se usa **202300689**.

## 1. Cableado

1. Cable **straight-through** o crossover (si no hay auto-MDIX): Switch1 **Fa0/24** (o Gi0/1) ↔ Switch2 **Fa0/24**.
2. PC1 → Switch1 Fa0/1. PC2 → Switch2 Fa0/1.
3. Consola USB/DB9 a cada switch. PuTTY 9600 8N1.

## 2. Switch 1 (Server)

```text
enable
configure terminal
hostname SW1-CORE
banner motd #Acceso Restringido - TechPark_202300689#
vtp mode server
vtp domain Smart_8
vtp password proyecto12S2026
vlan 19
 name GERENCIA
vlan 29
 name INVESTIGACION
vlan 39
 name PRODUCCION
vlan 49
 name SERVIDORES
vlan 59
 name VISITANTES
vlan 99
 name NATIVA
interface FastEthernet0/24
 switchport mode trunk
 switchport trunk native vlan 99
interface FastEthernet0/1
 switchport mode access
 switchport access vlan 19
 spanning-tree portfast
end
write memory
show vtp status
show vlan brief
show interfaces trunk
```

## 3. Switch 2 (Client)

```text
enable
configure terminal
hostname SW2-DIST
vtp domain Smart_8
vtp password proyecto12S2026
vtp mode client
interface FastEthernet0/24
 switchport mode trunk
 switchport trunk native vlan 99
interface FastEthernet0/1
 switchport mode access
 switchport access vlan 19
 spanning-tree portfast
end
write memory
show vtp status
show vlan brief
```

## 4. Verificar

- Switch2: Operating Mode **Client**, mismas VLAN 19/29/39/49/59/99, revision > 0.
- Trunk: native **99**, status trunking.
- IPs: PC1 `192.168.19.11`, PC2 `192.168.19.12`, máscara `255.255.255.0`.
- Ping PC1 → PC2 debe responder.

## 5. Fotos

1. Los dos switches y el cable trunk.  
2. `show vtp status` en Server y Client.  
3. `show vlan brief` en el Client (propagación).  
4. `show interfaces trunk`.  
5. Ping exitoso.

## Si VTP no propaga

1. Mismo dominio y password.  
2. Ambos extremos en trunk.  
3. Native 99 en los dos.  
4. El Client no debe estar en Transparent.  
5. Revision del Server **mayor** que la del Client (si el Client tiene revision más alta, no acepta). En laboratorio nuevo: `vtp mode off` / borrar vlan.dat solo si el auxiliar lo autoriza.
