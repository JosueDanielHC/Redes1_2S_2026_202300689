# -*- coding: utf-8 -*-
import os
from xhtml2pdf import pisa

BASE = os.path.dirname(os.path.abspath(__file__))
EV = os.path.join(BASE, "evidencias").replace("\\", "/")
OUT = os.path.join(BASE, "AP6_InterVLAN_202300689.pdf")
FONT = ""

def img(name):
    return EV + "/" + name

html = f"""
<html><head><meta charset="utf-8"/>
<style>
@page {{ size: letter; margin: 1.8cm 1.7cm; }}
body {{ font-family: Helvetica, sans-serif; font-size: 11px; color: #1a1a1a; line-height: 1.45; }}
h1 {{ font-size: 16px; color: #0b3d91; text-align: center; margin: 2px 0; }}
h2 {{ font-size: 13px; color: #0b3d91; border-bottom: 1px solid #cccccc; margin-top: 16px; }}
h3 {{ font-size: 12px; color: #222; margin-top: 12px; }}
.center {{ text-align: center; }}
.cover {{ text-align: center; margin-top: 70px; }}
.uni {{ font-size: 15px; font-weight: bold; color: #0b3d91; }}
.title {{ font-size: 18px; font-weight: bold; color: #0b3d91; margin-top: 70px; }}
.meta {{ margin-top: 70px; line-height: 1.8; font-size: 12px; }}
p {{ text-align: justify; }}
table {{ border-collapse: collapse; width: 100%; margin: 8px 0 10px 0; font-size: 10px; }}
th, td {{ border: 1px solid #bbbbbb; padding: 4px 6px; text-align: left; vertical-align: top; }}
th {{ background-color: #0b3d91; color: white; }}
pre {{ font-family: Courier, monospace; font-size: 9px; background: #f4f6fb; border: 1px solid #ddd; padding: 6px; }}
.cap {{ text-align: center; margin: 8px 0 12px 0; }}
.cap img {{ width: 15.5cm; }}
.capnum {{ font-size: 9px; color: #555; font-style: italic; }}
</style></head><body>

<div class="cover">
  <div class="uni">Universidad de San Carlos de Guatemala</div>
  <div>Facultad de Ingeniería</div>
  <div>Escuela de Ingeniería en Ciencias y Sistemas</div>
  <div class="title">Actividad práctica 6<br/>Enrutamiento Inter-VLAN</div>
  <div>Router-on-a-Stick y switch de capa 3</div>
  <div class="meta">
    <b>Curso:</b> Redes de Computadoras 1<br/>
    <b>Estudiante:</b> Josue Daniel Herrera Cottom<br/>
    <b>Carné:</b> 202300689<br/>
    <b>Fecha:</b> 11 de octubre de 2026<br/>
    <b>Archivo:</b> AP6_InterVLAN_202300689.pkt
  </div>
</div>
<div style="page-break-after: always;"></div>

<h2>1. Introducción</h2>
<p>La actividad pide comunicar dos departamentos que están en VLANs distintas y comparar dos maneras de hacerlo. Marketing queda en la VLAN 10 y Engineering en la VLAN 20. Un switch de capa 2 separa esas redes, así que hace falta un equipo de capa 3 para pasar de una a la otra.</p>
<p>Se armaron dos escenarios independientes en el mismo archivo de Packet Tracer. El primero usa Router-on-a-Stick: un router 2911 con subinterfaces 802.1Q y un switch 2960. El segundo usa un switch multicapa 3650, con una interfaz virtual por VLAN y el comando ip routing. Los dos lados no están cableados entre sí, por eso pueden repetir las mismas direcciones sin conflicto.</p>

<h2>2. Objetivos</h2>
<p>El objetivo es implementar enrutamiento Inter-VLAN con Router-on-a-Stick y con un switch de capa 3, de modo que una PC de Marketing alcance a una PC de Engineering.</p>
<table>
<tr><th>Dimensión</th><th>Aplicación en esta práctica</th></tr>
<tr><td>Específico</td><td>Configurar 2 VLANs, subinterfaces en el router y SVI en el switch de capa 3.</td></tr>
<tr><td>Medible</td><td>Ping con 0 % de pérdida y tracert que muestre la puerta de enlace.</td></tr>
<tr><td>Alcanzable</td><td>Solo con Cisco Packet Tracer y comandos de subinterfaces y SVI.</td></tr>
<tr><td>Realista</td><td>Ver qué método conviene cuando el tráfico entre departamentos crece.</td></tr>
<tr><td>A tiempo</td><td>Evidencia entregada con el archivo .pkt y este informe.</td></tr>
</table>

<h2>3. Direccionamiento</h2>
<p>La guía no fija las direcciones. Se usó una red por VLAN y la puerta de enlace .1 en el equipo de capa 3. En el escenario 1 esa puerta vive en las subinterfaces de R1. En el escenario 2 vive en Vlan10 y Vlan20 de SW-L3. La máscara de todos los hosts es 255.255.255.0.</p>
<table>
<tr><th>VLAN</th><th>Nombre</th><th>Red</th><th>Puerta de enlace</th><th>PC</th></tr>
<tr><td>10</td><td>Marketing</td><td>192.168.10.0/24</td><td>192.168.10.1</td><td>192.168.10.10</td></tr>
<tr><td>20</td><td>Engineering</td><td>192.168.20.0/24</td><td>192.168.20.1</td><td>192.168.20.10</td></tr>
</table>

<h2>4. Escenario 1: Router-on-a-Stick</h2>
<p>R1 es un router 2911. SW-ROAS es un 2960-24TT. PC-MKT está en la VLAN 10 y PC-ENG en la VLAN 20. Fa0/1 y Fa0/2 son puertos de acceso. Gi0/1 del switch va en modo trunk hacia Gi0/0 del router, con cable directo.</p>
<p>El router no lleva dirección en la interfaz física. Cada subinterfaz etiqueta su VLAN y recibe la puerta de enlace de ese departamento:</p>
<pre>interface GigabitEthernet0/0
 no ip address
 no shutdown
interface GigabitEthernet0/0.10
 encapsulation dot1Q 10
 ip address 192.168.10.1 255.255.255.0
interface GigabitEthernet0/0.20
 encapsulation dot1Q 20
 ip address 192.168.20.1 255.255.255.0</pre>
<p>show ip route en R1 muestra 192.168.10.0/24 conectada por GigabitEthernet0/0.10 y 192.168.20.0/24 conectada por GigabitEthernet0/0.20.</p>
<div class="cap"><img src="{img('02_sw_roas_vlans.png')}"/><div class="capnum">Figura 1. VLAN 10 y VLAN 20 en SW-ROAS, con Fa0/1 y Fa0/2 en acceso.</div></div>
<div class="cap"><img src="{img('03_r1_subinterfaces_y_ruta.png')}"/><div class="capnum">Figura 2. Subinterfaces dot1Q y tabla de rutas de R1.</div></div>
<p>Desde PC-MKT, el segundo ping a 192.168.20.10 terminó en 4 recibidos y 0 % de pérdida. El primer intento perdió un paquete mientras se armaba la tabla ARP. El tracert pasa por 192.168.10.1, que es la subinterfaz de la VLAN 10, y llega a PC-ENG. La trama sale sin etiqueta en el puerto de acceso, el switch la etiqueta en el troncal y el router cambia de red en las subinterfaces.</p>
<div class="cap"><img src="{img('04_ping_tracert_roas.png')}"/><div class="capnum">Figura 3. Ping y tracert de Marketing hacia Engineering por el router.</div></div>

<h2>5. Escenario 2: switch de capa 3</h2>
<p>SW-L3 es un 3650-24PS. PC-MKT2 entra por GigabitEthernet1/0/1 en la VLAN 10 y PC-ENG2 por GigabitEthernet1/0/2 en la VLAN 20. En este modelo los puertos nacen como interfaces de capa 3, así que cada uno lleva primero el comando switchport y después switchport mode access.</p>
<pre>ip routing
interface Vlan10
 ip address 192.168.10.1 255.255.255.0
interface Vlan20
 ip address 192.168.20.1 255.255.255.0</pre>
<p>ip routing es lo que permite reenviar entre esas interfaces virtuales. show ip route muestra las dos redes conectadas por Vlan10 y Vlan20.</p>
<div class="cap"><img src="{img('05_sw_l3_svi_routing_ruta.png')}"/><div class="capnum">Figura 4. Comando ip routing, interfaces Vlan10 y Vlan20, y tabla de rutas de SW-L3.</div></div>
<p>En la primera prueba, PC-MKT2 tenía la puerta de enlace escrita en el campo DNS y el gateway en 0.0.0.0. El ping se perdía por completo. Al colocar 192.168.10.1 en Default Gateway, el segundo ping quedó en 0 % de pérdida. El tracert ya no pasa por el 2911: el primer salto es 192.168.10.1 en SW-L3 y el segundo es PC-ENG2.</p>
<div class="cap"><img src="{img('06_ping_tracert_svi.png')}"/><div class="capnum">Figura 5. Ping y tracert entre VLANs a través del switch de capa 3.</div></div>

<h2>6. Topología completa</h2>
<p>Los dos escenarios están en el mismo lienzo y no comparten cables. Las luces verdes indican que los enlaces de acceso y el troncal del router están arriba.</p>
<div class="cap"><img src="{img('01_topologia.png')}"/><div class="capnum">Figura 6. Topología completa: Router-on-a-Stick a la izquierda y switch de capa 3 a la derecha.</div></div>

<h2>7. Análisis técnico</h2>
<p>Para una red empresarial con mucho tráfico entre departamentos, el método más eficiente es el switch de capa 3.</p>
<p>En Router-on-a-Stick cada paquete que cambia de VLAN sube por el único troncal, lo procesa el CPU del router y regresa por el mismo cable. Ese enlace se vuelve el cuello de botella: el ancho de banda de todas las VLANs compite por un solo puerto, y la latencia crece cuando el router está ocupado. Sirve para una oficina pequeña, con pocas VLANs y poco tráfico entre ellas, porque aprovecha un router que ya existe y un switch de capa 2.</p>
<p>En el 3650 la decisión de capa 3 ocurre dentro del mismo equipo, en hardware. No hay un cable externo que concentre el tráfico entre Marketing y Engineering, y las SVI permiten agregar VLANs sin crear una subinterfaz y un salto extra hacia un router. Para alto tráfico, menor latencia y más departamentos, el switch multicapa escala mejor. El router sigue teniendo sentido como salida a otras redes o a Internet, no como único camino entre VLANs del mismo edificio.</p>

<h2>8. Conclusiones</h2>
<p>1. Las dos VLANs quedan aisladas en capa 2 y se comunican solo cuando existe una puerta de enlace de capa 3.</p>
<p>2. Router-on-a-Stick cumple con un troncal 802.1Q y una subinterfaz por VLAN. El tracert pasa por 192.168.10.1 en R1.</p>
<p>3. El switch de capa 3 cumple lo mismo con SVI e ip routing. El tracert pasa por 192.168.10.1 en SW-L3, sin usar el router.</p>
<p>4. Cuando el tráfico entre VLANs es alto, el switch multicapa evita el cuello de botella del enlace único hacia el router.</p>

<h2>9. Referencias</h2>
<p>1. Guía de la actividad práctica de Inter-VLAN, Redes de Computadoras 1, Escuela de Ingeniería en Ciencias y Sistemas, USAC, segundo semestre 2026.</p>
<p>2. Cisco Networking Academy. CCNA v7, Switching, Routing, and Wireless Essentials. Módulo 4: Inter-VLAN Routing.</p>
<p>3. Cisco IOS. Comandos usados: encapsulation dot1Q, interface vlan, ip routing, show ip route y show vlan brief.</p>

</body></html>
"""

for a, b in {
    "á": "&aacute;", "é": "&eacute;", "í": "&iacute;", "ó": "&oacute;", "ú": "&uacute;",
    "Á": "&Aacute;", "É": "&Eacute;", "Í": "&Iacute;", "Ó": "&Oacute;", "Ú": "&Uacute;",
    "ñ": "&ntilde;", "Ñ": "&Ntilde;", "ü": "&uuml;",
}.items():
    html = html.replace(a, b)

with open(OUT, "wb") as f:
    status = pisa.CreatePDF(html, dest=f, encoding="utf-8")
print("ERROR" if status.err else "OK " + OUT)
