# Informe de desarrollo del diseño físico

**Proyecto:** Cableado estructurado — QuetzalDev S.A.  
**Autor:** Josue Daniel Herrera Cottom  
**Carné:** 202300689  
**Curso:** Redes de Computadoras 1 — FIUSAC — Segundo semestre 2026  
**Documento complementario:** [Manual_Tecnico.md](Manual_Tecnico.md) · [diagrama_diseno_fisico.png](diagrama_diseno_fisico.png)

---

## 1. Propósito de este informe

El manual técnico registra *qué* se va a instalar y *por qué* cada componente cumple TIA/EIA. Este informe registra *cómo* se llegó a esas decisiones: lectura del plano, restricciones del enunciado, tensiones entre centralidad geométrica y centralidad técnica, y la recomendación comercial de comprar materiales por cuenta propia o contratar a un integrador.

El trabajo se limitó a **Capa 1**. No se configuró un switch, no se dibujó un direccionamiento y no se usó Packet Tracer como evidencia de esta práctica (sí como cultura de laboratorio del curso). El artefacto visual es un diagrama de topología **física** superpuesto al plano asignado a los carnets 8 y 9.

---

## 2. Proceso de diseño

El proceso se ejecutó en seis pasos, de lo inmueble a lo presupuestario.

### Paso 1 — Lectura del plano

Se identificaron nueve recintos con función de red (siete oficinas + vestíbulo + Data Center) y dos que no reciben datos de usuario (baño 2 × 2 m y, en esta versión, el vestíbulo). El Hall Central de 26 × 2 m se interpretó de inmediato como **ruta primaria de canalización**, no como zona de racks. El corredor secundario de 1.5 m es el único acceso técnico al Data Center: eso condicionó que el troncal “suba” por ahí y no atraviese Legal en diagonal.

Dimensiones usadas como escala real (no en píxeles):

- Bloque principal: 26 m (X) × 16 m (Y).
- Franja norte: 6 m (Dirección, Recepción, Legal).
- Franja sur: 8 m (RRHH, Capacitación, vestíbulo, Diseño, Backend).
- Hall: 2 m.
- Data Center: 6 × 4 m.

Con esa malla se midieron recorridos **por pasillo**, que es como se tiende una escalerilla, no en línea recta euclidiana.

### Paso 2 — Inventario de hosts y mezcla propia

El enunciado fija cuántos “computadoras” hay por depto. y deja libre la partición entre 30 PC y 12 laptops. La terminación de carné **9** se usó para sesgar la mezcla hacia movilidad en RRHH (3 laptops) y Diseño (3 laptops), y hacia puestos fijos en Capacitación (8 PC) y Backend (5 PC). Eso impide que el diagrama sea un calco del de otro estudiante y cambia el mapa de tomas (triples en mostrador de Recepción, dobles en filas del aula).

Los 6 servidores se respetaron al pie de la letra: 1 en Recepción, 1 en Diseño, 1 en Backend y 3 en el Data Center.

### Paso 3 — MDF y jerarquía

Se compararon tres sitios:

| Candidato | Ventaja | Desventaja | Resultado |
|-----------|---------|------------|-----------|
| Centro del Hall / vestíbulo | Distancia media mínima | Público, sin HVAC, bloquea evacuación | Descartado |
| Cuarto improvisado en Recepción (12 × 6 m) | Espacio amplio | Ruido, visitas, sin control de acceso de nivel DC | Descartado |
| Data Center 6 × 4 m | Único local técnico, servidores nucleares, puerta de servicio | Excentricidad al este (~30–38 m al ala oeste) | **Elegido** |

La excentricidad es aceptable porque 38 m ≪ 90 m. La jerarquía quedó: **1 core + 8 accesos**. Un diseño “todo home-run al MDF” (48 cobres al Data Center) saturaría la escalerilla de 1.5 m del corredor secundario y anularía los switches de departamento que el enunciado exige.

### Paso 4 — Topologías locales

Se evitó poner “estrella” en las ocho áreas con la misma frase. Dirección, Recepción y Backend son estrellas simples (pocos hosts). Legal y RRHH son estrellas **extendidas** vía tomas dobles (el faceplate es el segundo nivel). Capacitación se canalizó como **árbol por filas** (una derivación por pupitre doble + rama del instructor). El Data Center se documentó como **malla parcial** (dos NIC por servidor hacia SW-DC). El edificio entero es el árbol que amarra esas hojas.

### Paso 5 — Medios

Horizontal: Cat 6A (10G a 100 m, alien crosstalk controlado, vida útil alineada a 2026–2031).  
Troncal: OM4 10GBASE-SR en un cable de 12 hilos, más un crossover de cobre a Legal como evidencia de ponchado y como contingencia.  
La justificación detallada está en el manual; aquí basta decir que el criterio no fue “la distancia obliga a fibra” (no obliga), sino **aislamiento, densidad de bandeja y uplink de 10 Gb/s sin comerse 8 puertos 10GBASE-T del core**.

### Paso 6 — Dibujo, etiquetado, presupuesto

Sobre el plano se pintaron MDF, switches, iconos PC/laptop/servidor, rombos de toma, troncal rojo, horizontal por color, escalerilla ámbar y las etiquetas `Depto-PR##` / `MDF-Depto`. El script `generar_diagrama.py` reproduce ese PNG. El presupuesto cerró en **Q 148 940** de materiales, cifra que alimenta la sección comercial de este informe.

---

## 3. Criterios para topologías, medios y equipo activo

Tres variables se pesaron en cada depto.: **número de hosts**, **criticidad** y **costo / escalabilidad / tolerancia a fallos**.

- Un aula de 10 puestos (Capacitación) no puede depender de un bus: un conector flojo partiría la clase. El árbol por filas localiza la falla a una toma doble.
- Los servidores de DC justifican dual-homing; el servidor de Recepción (turnos) no: si cae, el negocio sigue en papel un día; si caen los tres del DC, no hay repositorio ni CI.
- El Catalyst 9200-48P parece “grande” para ocho uplinks de fibra. Se eligió así **a propósito**: la rúbrica pide paridad con un patch panel de 48 puertos, y el 48P deja cobre para firewall, out-of-band y el crossover a Legal. Un CBS350-8SFP como core habría incumplido esa paridad y habría dejado a QuetzalDev sin puertos el día del primer AP o de la primera cámara.
- Los CBS350 de acceso (y no otro Catalyst 9200 por depto.) recortan el presupuesto en decenas de miles de quetzales con SFP suficientes para OM4.

---

## 4. Retos de planificación física al interpretar el plano

1. **El Data Center no es central.** El enunciado pide minimizar distancia *y* usar el plano tal cual. Resolverlo exigió argumentar *centralidad técnica* y demostrar con números que el ala oeste sigue dentro de Cat 6A / OM4.

2. **Muebles vs. tomas.** RRHH es casi solo una mesa de juntas en 5 × 8 m; Capacitación ya trae ocho pupitres y un baño que “come” esquina. No se colocaron tomas en el baño ni se atravesó esa esquina con bandeja. En Diseño, la mesa de ocho sillas sugiere ocho personas, pero el enunciado solo da **siete computadoras + un servidor**: el octavo asiento quedó sin permanente (crecimiento documentado).

3. **Backend muestra más estaciones que hosts asignados.** El plano sugiere bancadas largas; el enunciado da 6 computadoras + 1 servidor. Se cablearon 7 puertos y se dejó holgura en el CBS350-16T (8 puertos libres) para no recablear cuando Backend crezca.

4. **Corredor de 1.5 m.** Es estrecho para un rack, no para una escalerilla. Eso reforzó la decisión de **no** poner el MDF en el corredor y sí de usarlo solo como pathway.

5. **Vestíbulo con ingreso.** Tentador para un rack “de bienvenida”. Se rechazó: es el punto más inseguro y más sucio (puerta al exterior).

6. **Un solo nivel, un solo MDF.** No hay IDF de piso intermedio. Toda la jerarquía es “edificio = un TR”. Eso simplifica 606, pero obliga a que la bandeja del hall sea el *backbone pathway* único: un corte de bandeja en el este aislaría el oeste. Por eso la tapa metálica y el cable FO de 12 hilos con 4 fibras oscuras.

7. **Etiquetado pedagógico vs. 606.** El formato `Recepcion-PR01` no cabe en un identificador 606-C de puerto. Se cumplió el enunciado y se documentaron **dos diferencias concretas** (unicidad espacial y clases/colores de identificador) para no fingir que el esquema de clase es un sistema de administración real.

8. **Crossover en un mundo Auto-MDIX.** Los switches elegidos negocian MDI/MDIX. Inventar un crossover “porque el libro lo pide” en un horizontal host–switch habría sido un error técnico. Se acotó al **único** enlace cobre switch–switch (respaldo Legal) y se dibujaron pines B↔A.

---

## 5. Justificación del medio en el cableado troncal

El troncal **no** se resolvió con UTP Cat 6A como diseño principal, pese a que ningún uplink supera 40 m.

Razones, en orden de peso:

1. **Ancho de banda agregado.** Ocho departamentos compartiendo un core a 1 Gb/s de uplink saturarían Capacitación + Backend + Diseño en una demo o un clone masivo de repos. 10GBASE-SR sobre OM4 da un orden de magnitud de holgura.
2. **Un solo cable en bandeja.** Doce hilos OM4 equivalen a ocho dúplex + reserva. Ocho Cat 6A 10G en la misma escalerilla que el horizontal aumentan diámetro, peso y alien crosstalk.
3. **EMI.** El MDF comparte cuarto con UPS y, en operación, con fuentes de servidores. La fibra no cierra mallas de tierra entre IDF y ER.
4. **Costo a cinco años.** El metro de OM4 indoor es más caro que el de Cat 6A, pero 16 SFP-10G-SR (Q 12 480) evitan recablear el hall cuando el primer NAS pida 10G. Recablear el hall después de cielo falso y pintura cuesta más que esos transceptores.
5. **El cobre no se elimina:** el permanente `MDF-Legal-COBRE` cubre la contingencia y la rúbrica de crossover.

OS2 se descartó por distancia y por precio de óptica LR. OM3 se descartó por el marginal a OM4.

---

## 6. Compra individual de materiales vs. proveedor / integrador

Con **Q 148 940** en materiales y ~514 m de Cat 6A + fusión de 12 fibras, la pregunta no es retórica.

### 6.1 Escenario A — Compra individual (QuetzalDev o el estudiante-instalador)

**A favor**

- Se ahorra el margen del integrador (estimado Q 18 000–25 000 de mano de obra + 10–15 % de suministro).
- Control fino de marcas (Panduit + Siemon + Cisco) sin “equivalentes” no solicitados.
- Útil si ya existe un electricista interno que solo necesita supervisión de ponchado.

**En contra**

- Certificar 48 permanentes Cat 6A exige un **Fluke DSX** (alquiler Q 3 200 en el presupuesto; en plaza a veces no hay equipo la semana de la obra).
- La fusión o cassette preterminado OM4 mal hecha deja el troncal inútil: no hay “tester de casa” que sustituya un OTDR / certificador de fibra.
- Garantía de canal de 20–25 años de Siemon/Panduit **se pierde** si no instala un partner certificado.
- Un error de fill en la escalerilla o de radio de curvatura Cat 6A (4× Ø) no se ve hasta que 10GBASE-T no enlaza.

### 6.2 Escenario B — Integrador externo

**A favor**

- Un solo responsable de as-built, etiquetado 606, certificación y garantía de canal.
- Seguros de obra y cumplimiento de TIA-569 en bandeja.
- Entrega alineada al 21/08/2026 sin improvisar fusiones.

**En contra**

- Mayor desembolso.
- Riesgo de que sustituyan CBS350 por una marca blanca si el contrato no fija SKU.

### 6.3 Recomendación

**Modelo híbrido, con sesgo a integrador en lo óptico:**

- QuetzalDev (o compras internas) **adquiere** el activo Cisco y la UPS (mejor precio académico / mayorista, y queda en inventario de TI).
- Un **partner certificado Panduit o Siemon** tiende bandeja, cobre, fibra, poncha T568B, certifica y entrega reportes PDF por puerto.
- El crossover `MDF-Legal-COBRE` y los cordones los puede armar TI, porque no forman parte del canal permanente certificado.

Para un edificio de 48 puntos, el ahorro de “hacerlo todo uno mismo” es pequeño frente al costo de rehacer el hall. La compra 100 % individual solo se justificaría si el laboratorio de la universidad prestara certificador y un docente supervisara la fusión, lo cual **no** es el caso de QuetzalDev como cliente real.

---

## 7. Consideraciones de escalabilidad futura

1. **Puertos.** Capacitación usa 11/16, Backend 8/16, Dirección 5/8. Hay holgura para ~20 hosts más sin cambiar switches. El core 48P y el panel 48P absorben un segundo piso de cobre de respaldo o un firewall + dos AP controladores.
2. **Tomas.** El asiento extra de Diseño y las bancadas largas de Backend ya tienen ruta de zócalo: agregar un jack Mini-Com no implica picar losa.
3. **Fibra oscura.** 4 de 12 hilos quedan sin terminar. Un noveno IDF (bodega, cafetería, segundo acceso) se deriva sin tender otro backbone.
4. **PoE.** El 9200-48P tiene presupuesto PoE+ dormido. Un par de AP Wi-Fi 6 en Hall y Capacitación se alimentan desde IDF si se cambia el CBS350 por un modelo PoE, o desde el core con un home-run corto. La UPS SMT1500 **debería entonces reemplazarse** por 3 kVA.
5. **Servidores.** El rack 42U deja ~18U libres. Un segundo switch ToR o un UPS SRT3000 entra sin mudar el MDF.
6. **10G al escritorio.** Cat 6A ya es el medio de 10GBASE-T. No hay que abrir muros; solo cambiar NIC y, si se desea, el CBS350 por un acceso Multigig.
7. **TIA-606.** Si la empresa crece a otro nivel, el esquema `Depto-PR##` se sustituye por identificadores de espacio/rack/puerto **sin recablear**, solo reetiquetando y cargando la base de administración.

---

## 8. Limitaciones honestas del diseño

- El PNG es una **proyección didáctica** sobre un plano 1024×768: las cotas en metros del manual priman sobre el píxel.
- No se levantó un estudio de carga de losa ni de HVAC del Data Center de 24 m²; se asume que el local técnico del arquitecto ya contempla disipación de un rack.
- Los precios son de mercado general, no cotizaciones con NIT de QuetzalDev.
- No se diseñó CCTV, control de acceso ni Wi-Fi: el enunciado no los pide. Las reservas de bandeja y de PoE existen para no cerrar esas puertas.

---

## 9. Conclusión

El edificio de QuetzalDev S.A. admite un cableado estructurado de un solo MDF en el Data Center, estrella jerárquica, horizontal Cat 6A y troncal OM4, con 48 puntos certificados dentro de los 90 m de TIA-568. Los retos del plano (Data Center excéntrico, corredor de 1.5 m, muebles que no coinciden con el recuento de hosts) se resolvieron con rutas de Hall Central, tomas U/D/T y holgura de puertos, no con topologías de bus ni con un rack en el vestíbulo.

La mezcla PC/laptop del carné 202300689, el árbol por filas del aula, la malla parcial del DC y el crossover de respaldo a Legal son decisiones **propias** de este diseño. El siguiente paso de ingeniería, fuera de esta práctica, sería la configuración de VLANs y el direccionamiento; la Capa 1 ya no debería reabrirse si se respeta este as-built.

---

*Josue Daniel Herrera Cottom — 202300689 — FIUSAC*
