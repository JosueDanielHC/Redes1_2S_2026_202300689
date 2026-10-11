# Actividad práctica 6 — HSRP

Universidad de San Carlos de Guatemala  
Facultad de Ingeniería  
Escuela de Ingeniería en Ciencias y Sistemas  
Redes de Computadoras 1 — Segundo semestre 2026

**Estudiante:** Josue Daniel Herrera Cottom  
**Carné:** 202300689  
**Fecha:** 11 de octubre de 2026  
**Archivo:** `202300689_JosueDanielHerreraCottom_HSRP.pkt`

## 1. Qué se configuró

La red inferior tiene dos routers, `R1` y `R2`, unidos por un switch `SW1` a `PC-INF`. Arriba, `R-SUP` conecta con los dos routers y con `PC-SUP`. Todos los cables son Copper Straight-Through.

`PC-INF` no usa la IP de un router como puerta de enlace. Usa la IP virtual de HSRP, `192.168.10.1`. `R1` arranca como activo, con prioridad 110. `R2` arranca en espera, con prioridad 100. Los dos tienen `preempt`. El enrutamiento entre la red de abajo (`192.168.10.0/24`) y la de arriba (`192.168.20.0/24`) es OSPF.

| Equipo | Dirección | Rol |
|--------|-----------|-----|
| PC-INF | 192.168.10.10/24, gateway 192.168.10.1 | Host inferior |
| R1 Gi0/0 | 192.168.10.2/24 | Activo, prioridad 110 |
| R2 Gi0/0 | 192.168.10.3/24 | Standby, prioridad 100 |
| Virtual | 192.168.10.1 | Gateway de PC-INF |
| R-SUP Gi0/0 | 192.168.20.1/24 | Gateway de PC-SUP |
| PC-SUP | 192.168.20.10/24, gateway 192.168.20.1 | Host superior |

## 2. Antes de la falla

`show standby brief` en `R1` muestra estado Active, prioridad 110, preempt y la virtual `192.168.10.1`. El standby es `192.168.10.3`, o sea `R2`.

En `R2` el mismo comando muestra estado Standby, prioridad 100 y al activo `192.168.10.2`.

Desde `PC-INF`, `ping -t 192.168.20.10` llega a la PC superior. En la primera prueba se enviaron 23 paquetes y se recibieron 21. Los dos perdidos corresponden al arranque.

## 3. Durante la falla

Con el ping continuo en marcha se apagó `GigabitEthernet0/0` de `R1`, la interfaz de la LAN inferior. HSRP en `R1` pasó de Active a Init. En `R2` el aviso fue `Standby -> Active`.

El ping se interrumpió dos paquetes (`Request timed out`) y luego volvió a responder. `PC-INF` no cambió su gateway: siguió usando `192.168.10.1`, ahora respondida por `R2`.

El `show standby brief` posterior en `R2` queda así: estado Active, columna Active en local, Standby unknown (porque `R1` ya no participa) y la misma IP virtual.

## 4. Para qué sirve preempt

`preempt` permite que el router de mayor prioridad recupere el rol activo cuando su interfaz vuelve. Sin ese comando, `R2` se quedaría activo aunque `R1` regresara. Con el comando configurado, un `no shutdown` en `Gi0/0` de `R1` le devuelve el papel de activo por su prioridad 110.

Al momento de guardar la simulación, `Gi0/0` de `R1` sigue en shutdown. Ese es el estado de después de la prueba. La conectividad hacia `PC-SUP` se mantiene por `R2`.
