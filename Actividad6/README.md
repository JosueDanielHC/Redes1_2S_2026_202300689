# Actividad práctica 6 — HSRP

Universidad de San Carlos de Guatemala  
Facultad de Ingeniería  
Escuela de Ingeniería en Ciencias y Sistemas  
Redes de Computadoras 1 — Segundo semestre 2026

| Dato | Valor |
|------|--------|
| Estudiante | Josue Daniel Herrera Cottom |
| Carné | 202300689 |
| Fecha | 11 de octubre de 2026 |
| Simulación | [202300689_JosueDanielHerreraCottom_HSRP.pkt](202300689_JosueDanielHerreraCottom_HSRP.pkt) |
| Informe | [202300689_JosueDanielHerreraCottom_HSRP.pdf](202300689_JosueDanielHerreraCottom_HSRP.pdf) |

La entrega de esta actividad es el par de archivos con el nombre `Carnet_Nombre_HSRP`. La PC inferior usa como gateway la IP virtual `192.168.10.1`. `R1` inicia activo y `R2` en espera. Al apagar la LAN de `R1`, `R2` toma el rol activo y el ping hacia la PC superior se recupera.

El archivo `.pkt` quedó guardado con `Gi0/0` de `R1` en shutdown, que es el estado posterior a la prueba de falla.
