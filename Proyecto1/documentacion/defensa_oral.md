# Defensa oral — respuestas cortas

Carné **202300689** impar → **PAgP** y **Rapid-PVST**. VLAN nativa **99**. Dominio **Smart_8**.

**¿Qué es VTP?** Protocolo que propaga el catálogo de VLAN desde un Server a los Client del mismo dominio.

**¿Por qué este switch es Server?** `SW-CORE` es el centro; un solo punto crea las VLAN 19–59 y 99.

**¿Qué significa Client?** Recibe VLAN; no las crea ni las borra.

**¿Cómo sabes que se propagó?** `show vtp status`: mismo dominio, revision > 0, y `show vlan brief` muestra 19, 29, 39, 49, 59, 99.

**¿Qué es un trunk?** Enlace que transporta varias VLAN con etiquetas 802.1q.

**¿Access vs Trunk?** Access = una VLAN (PC). Trunk = varias (switch–switch).

**¿Qué es STP?** Evita bucles L2 bloqueando enlaces redundantes.

**¿Quién es Root?** `SW-CORE`, prioridad 4096. Ahí converge todo el campus.

**¿Qué hace EtherChannel?** Agrupa 2 enlaces en uno lógico. Si cae un miembro, el otro sigue.

**¿Por qué PAgP?** Carné impar. Modo `desirable` en ambos lados.

**¿Si falla un enlace de I+D?** El triángulo reencamina por ACC1–ACC2. Lo comprobamos con `shutdown` del uplink.

**¿Dominio de broadcast?** Una VLAN. Broadcast de Gerencia no llega a I+D.

**¿Dominio de colisión?** En un switch, un puerto = un dominio. En el **Hub**, todos los puertos son el mismo dominio.

**¿Por qué el Hub?** El PDF pide Legacy. CSMA/CD compartido entre PC-IND-1, PC-IND-2 y el puerto del switch.

**¿Por qué nativa 99?** El PDF prohíbe dejar VLAN 1 como nativa. 9X con X=9 → 99.

**¿Qué es la revisión VTP?** Contador. El Client solo acepta anuncios con revisión **mayor**.

**¿Por qué VISIT es Transparent?** Para que visitantes no dependan del catálogo corporativo; VLAN 59 se crea local.

**¿Por qué el ping Gerencia → I+D falla?** Distinta VLAN y no hay router. Eso es el aislamiento pedido.
