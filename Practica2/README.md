# Universidad de San Carlos de Guatemala

## Facultad de Ingeniería

### Escuela de Ingeniería en Ciencias y Sistemas

---

| Dato | Valor |
|------|--------|
| **Universidad** | Universidad de San Carlos de Guatemala (USAC) |
| **Facultad** | Facultad de Ingeniería (FIUSAC) |
| **Escuela** | Ingeniería en Ciencias y Sistemas |
| **Curso** | Redes de Computadoras 1 |
| **Práctica** | Práctica 2 — Red de la Ciudad Comercial Cayalá |
| **Estudiante** | Josue Daniel Herrera Cottom |
| **Carné** | 202300689 |
| **Terminación de carné** | 9 (VLANs 19, 29, 39, 49 y 59; EtherChannel con PAgP) |
| **Repositorio** | [Redes1_2S_2026_202300689](https://github.com/JosueDanielHC/Redes1_2S_2026_202300689) |
| **Semestre** | Segundo semestre 2026 |
| **Ponderación** | 7 pts |

---

# Práctica 2 — Red de capa 2 del complejo Cayalá

Cinco zonas reales del complejo se interconectan con switches Cisco 2960 y 3560. Cada zona tiene su VLAN. El direccionamiento de los hosts representativos está en la red **192.168.89.0/24**. La simulación está hecha en Cisco Packet Tracer y configurada solo por CLI.

## Documentos

- [Manual técnico](Manual_Tecnico.md) — zonas, topología híbrida, VLANs, VTP, Rapid PVST+, EtherChannel PAgP, dominios de colisión y pruebas.
- [Informe de desarrollo](Informe_Desarrollo.md) — problemas encontrados (sobre todo el EtherChannel) y cómo se resolvieron.
- [Código fuente](codigo_fuente.md) — comandos CLI finales de los 11 switches.
- `Practica2_202300689.pkt` — archivo de Packet Tracer. Se guarda desde el simulador con **File → Save As** dentro de esta carpeta.
- [capturas](capturas) — evidencia de topología, EtherChannel, STP, VLANs, pings y `show ip route`.

## Qué debe ocurrir en la simulación

- Un ping entre PCs de la **misma zona** responde.
- Un ping entre PCs de **zonas distintas** termina en `Request timed out`.
- `show ip route` en CORE muestra `192.168.89.0/24` conectada por la VLAN 99.
