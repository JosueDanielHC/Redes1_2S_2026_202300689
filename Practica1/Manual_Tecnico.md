# Manual técnico de cableado estructurado

**Proyecto:** Red LAN de un nivel — QuetzalDev S.A.  
**Elaborado por:** Josue Daniel Herrera Cottom — Carné 202300689  
**Rol:** Ingeniero consultor en telecomunicaciones (diseño de Capa 1)  
**Universidad:** USAC / FIUSAC — Redes de Computadoras 1 — 2S 2026  
**Plano base:** carnets con terminación 8 y 9 (26 m × 16 m + Data Center 6 m × 4 m)

---

## Índice

1. [Alcance y supuestos](#1-alcance-y-supuestos)
2. [Inventario de equipos](#2-inventario-de-equipos)
3. [Ubicación del MDF](#3-ubicación-del-mdf)
4. [Topologías físicas por departamento](#4-topologías-físicas-por-departamento)
5. [Puntos de red y tipo de toma](#5-puntos-de-red-y-tipo-de-toma)
6. [Cableado horizontal](#6-cableado-horizontal)
7. [Cableado troncal](#7-cableado-troncal)
8. [Dimensionamiento de patch panel y switch del edificio](#8-dimensionamiento-de-patch-panel-y-switch-del-edificio)
9. [Justificación del equipo activo](#9-justificación-del-equipo-activo)
10. [Canalización](#10-canalización)
11. [Rack / gabinete del MDF](#11-rack--gabinete-del-mdf)
12. [Consumo eléctrico y UPS](#12-consumo-eléctrico-y-ups)
13. [Normas de ponchado T568A / T568B](#13-normas-de-ponchado-t568a--t568b)
14. [Etiquetado de cables y comparación TIA/EIA-606](#14-etiquetado-de-cables-y-comparación-tiaeia-606)
15. [Flujo de conexión end-to-end](#15-flujo-de-conexión-end-to-end)
16. [Presupuesto estimado](#16-presupuesto-estimado)
17. [Referencias](#17-referencias)

---

## 1. Alcance y supuestos

Este manual documenta **únicamente la Capa 1 (física)** del modelo OSI: medios, conectores, canalizaciones, racks, tomas, etiquetado y equipo activo de acceso. No se asignan VLAN, direcciones IP ni se simula el reenvío de tramas.

**Inventario de hosts del cliente (enunciado):** 30 PC de escritorio, 12 laptops y 6 servidores, en un solo nivel, con un switch de departamento por área y **un único switch principal** en el MDF que alimenta a esos switches.

**Mezcla PC / laptop (discreción del estudiante, carné …689):**

| Departamento | PC | Laptop | Servidor | Total hosts | Switch |
|--------------|----|--------|----------|-------------|--------|
| Dirección General | 3 | 1 | 0 | 4 | SW-DIR |
| Recepción | 2 | 1 | 1 | 4 | SW-REC |
| Legal | 3 | 1 | 0 | 4 | SW-LEG |
| Recursos Humanos | 5 | 3 | 0 | 8 | SW-RRHH |
| Sala de Capacitación | 8 | 2 | 0 | 10 | SW-CAP |
| Diseño e Innovación | 4 | 3 | 1 | 8 | SW-DIS |
| Backend | 5 | 1 | 1 | 7 | SW-BCK |
| Data Center | 0 | 0 | 3 | 3 | SW-DC |
| **Total** | **30** | **12** | **6** | **48** | 8 de acceso + 1 core |

La mezcla privilegia laptops en RRHH y Diseño (movilidad de entrevistas y workshops) y PCs fijas en Capacitación y Backend (puestos permanentes). Esa decisión cambia el tipo de toma (doble vs unitaria) respecto a un diseño que pusiera 12 laptops solo en Capacitación.

**Supuestos de ingeniería:**

- Altura de plenum / falso cielo ≈ 0.45 m; las distancias de planta se incrementan **25 %** por verticales, holgura de bandeja y bucles de servicio (TIA-568 recomienda slack en ambos extremos).
- No hay interferencia industrial; sí hay UPS, iluminación y HVAC en el Data Center (EMI moderada → fibra en troncal).
- Cada host requiere **un puerto de red dedicado**. Las laptops se conectan por toma de pared (no se diseña Wi-Fi en esta práctica).
- El baño y el vestíbulo **no** reciben tomas de datos de usuario.

---

## 2. Inventario de equipos

Marcas y modelos reales (Cisco, Panduit, Siemon, APC, Chatsworth), seleccionados por disponibilidad regional (distribuidores tipo ITG, PC Wholesale, Anixter/Wesco Centroamérica).

### 2.1 Equipo activo

| ID | Equipo | Marca / modelo | Cant. | Puertos | Función |
|----|--------|----------------|-------|---------|---------|
| SW-CORE | Switch principal del edificio | Cisco Catalyst C9200-48P-E | 1 | 48×1G PoE+ + 4×SFP/SFP+ (módulo C9200-NM-4X) | Agregación de troncales y borde WAN futuro |
| SW-DIR | Switch Dirección | Cisco CBS350-8T-E-2G | 1 | 8×1G + 2 SFP | Acceso Dirección |
| SW-REC | Switch Recepción | Cisco CBS350-8T-E-2G | 1 | 8×1G + 2 SFP | Acceso Recepción + servidor local |
| SW-LEG | Switch Legal | Cisco CBS350-8T-E-2G | 1 | 8×1G + 2 SFP | Acceso Legal |
| SW-DC | Switch Data Center | Cisco CBS350-8T-E-2G | 1 | 8×1G + 2 SFP | Acceso 3 servidores principales |
| SW-RRHH | Switch RRHH | Cisco CBS350-16T-E-2G | 1 | 16×1G + 2 SFP | Acceso RRHH |
| SW-CAP | Switch Capacitación | Cisco CBS350-16T-E-2G | 1 | 16×1G + 2 SFP | Acceso Capacitación |
| SW-DIS | Switch Diseño | Cisco CBS350-16T-E-2G | 1 | 16×1G + 2 SFP | Acceso Diseño + servidor QA |
| SW-BCK | Switch Backend | Cisco CBS350-16T-E-2G | 1 | 16×1G + 2 SFP | Acceso Backend + servidor depto. |

Los CBS350 incluyen SFP para el uplink de fibra. El core 48P cumple la regla de la práctica: **puertos del switch del edificio ≥ puertos del patch panel del edificio (48)**.

### 2.2 Pasivo de cobre y fibra

| Ítem | Marca / modelo | Cant. | Observación |
|------|----------------|-------|-------------|
| Patch panel 24 puertos Cat 6A | Panduit CP24BLY (Mini-Com) | 2 en MDF + 8 en IDF de depto. = 10 | MDF: 48 puertos; cada depto. un panel de 24 (holgura) |
| Jacks RJ45 Cat 6A | Panduit CJ6X88TGBU (Mini-Com) | 48 | Azul = datos (código de color TIA-606) |
| Faceplates | Panduit CFP2IW / CFP4IW / CFP1IW | 27 | 1, 2 o 4 posiciones según toma |
| Cordones de parcheo Cat 6A 1 m | Panduit UTP6A1M | 48 | Switch ↔ patch panel (IDF) |
| Cordones de estación Cat 6A 3 m | Panduit UTP6A3M | 48 | Toma ↔ host |
| Cable horizontal UTP Cat 6A | Siemon 9A6L4-A5 (CMP/CMR) bobina 305 m | 3 bobinas | Canal clase EA, 500 MHz, 10GBASE-T |
| Cable troncal fibra 12 hilos OM4 | Siemon 9FF8P012G-TBO (indoor) | 60 m | Un backbone compartido; 2 fibras por depto. + 4 de reserva |
| ODF / bandeja FO 12 puertos LC | Siemon RIC3-24-01 + adaptadores LC dúplex | 1 | Terminación en MDF |
| Pigtails / cassette LC OM4 | Siemon LightVerse LC | 8 dúplex | Un cassette por troncal |
| Transceptores SFP+ 10G SR | Cisco SFP-10G-SR | 16 | 8 en core + 8 en acceso |
| Patch cords FO LC-LC OM4 2 m | Panduit FZ2ERQ1Q1SNM002 | 16 | ODF ↔ SFP |
| Cable Cat 6A troncal de respaldo | Siemon Cat 6A (del mismo lote) | 20 m | Solo MDF–Legal (cobre) |

### 2.3 Canalización, rack y energía

| Ítem | Marca / modelo | Cant. |
|------|----------------|-------|
| Escalerilla metálica cerrada 300 × 100 mm | Chatsworth / Panduit Wyr-Grid equivalente, tapa | 32 m |
| Bajantes EMT ¾" + curvas | Steel Electric | 16 tramos |
| Rack de piso 42U × 800 × 1070 mm | Chatsworth F-Series TeraFrame o equivalente 42U | 1 |
| PDU metered 16A | APC AP8853 | 2 |
| Organizadores 1U y 2U | Panduit NCMH2 / WMPFSE | 6 |
| UPS | APC Smart-UPS SMT1500C | 1 |
| Gabinete mural 12U (IDF depto.) | Panduit PZWMC12W | 8 |
| Etiquetas P-touch TIA-606 | Brother TZe / Panduit LS8EQ | 1 kit |

### 2.4 Resumen de tomas

| Tipo de toma | Cantidad de faceplates | Puertos RJ45 |
|--------------|------------------------|--------------|
| Unitaria (U) | 8 | 8 |
| Doble (D) | 18 | 36 |
| Triple (T) | 1 | 3 |
| **Total** | **27** | **48** |

---

## 3. Ubicación del MDF

### 3.1 Decisión

El **Main Distribution Frame (MDF)** se instala **dentro del Data Center (6 m × 4 m)**, en el extremo superior derecho del plano, junto a los tres servidores principales. No se crea un cuarto de telecomunicaciones nuevo en el vestíbulo ni en el Hall Central.

### 3.2 Por qué no el “centro geométrico”

El centro geométrico del rectángulo 26 × 16 m cae cerca del Hall Central / vestíbulo. Esa posición **minimizaría metros de cobre**, pero violaría buenas prácticas TIA-569 / TIA-942:

1. El vestíbulo es zona pública (ingreso). Un MDF allí no tiene control de acceso, HVAC ni extinción.
2. El Hall Central es ruta de evacuación: no debe alojar racks.
3. El Data Center **ya es el único espacio técnico** del plano: 24 m², puerta restringida y corredor secundario de 1.5 m (separación de circulación general).
4. Los tres servidores nucleares **deben** quedar a pocos metros del core y de la UPS; mover el MDF al centro obligaría a un segundo hop o a alargar power/datos de servidores críticos.
5. La distancia permanente más larga (MDF → Dirección / RRHH, recorriendo Hall Central) es del orden de **32–38 m**, muy por debajo del límite de **90 m** de TIA-568.2-D. La penalización de no estar en el centro geométrico **no compromete la categoría del canal**.

### 3.3 Centralidad técnica (no solo geométrica)

Se entiende *centralidad* como el punto que **minimiza el riesgo y el costo total de propiedad**, no solo la media aritmética de distancias:

- Un solo cuarto de equipos (MDF + servidores + UPS + ODF).
- Troncal de fibra recorre **una sola** escalerilla (Hall Central + corredor secundario).
- Cada departamento queda a un drop vertical de 2–4 m desde esa bandeja.

**Coordenada de referencia (origen en la esquina inferior izquierda del bloque 26 × 16):** MDF ≈ (29 m, 14 m) dentro del anexo Data Center.

---

## 4. Topologías físicas por departamento

La topología **del edificio** es un **árbol (estrella jerárquica)**: un core en el MDF y un switch de acceso por área. Eso equilibra costo (un solo core), escalabilidad (se agrega un IDF sin recablear el edificio) y tolerancia a fallos (la caída de un switch de depto. no apaga los demás).

A nivel de cada área, **no se repite el mismo esquema físico**, porque el enunciado exige justificar por número de hosts, criticidad y costo.

| Área | Topología física | Por qué |
|------|------------------|---------|
| **Edificio** | Árbol / estrella jerárquica | Un core, ocho hojas. Crecimiento por depto. sin malla cara. |
| **Dirección General** | Estrella simple | 4 hosts, criticidad alta de *información* pero baja de *conteo*. Un switch 8P es el mínimo profesional. Malla sería desperdicio. |
| **Recepción** | Estrella simple | 3 puestos + 1 servidor de turnos/visitas. El servidor cuelga del mismo switch local para no atravesar el troncal en cada autenticación de visita. |
| **Legal** | Estrella extendida | 4 hosts en dos núcleos (escritorio y mesa de juntas). Tomas **dobles** en cada núcleo: la estrella se “extiende” al faceplate, no se pone un segundo switch. |
| **RRHH** | Estrella extendida | 8 hosts alrededor de una mesa de 6+ asientos. Cuatro tomas dobles perimetrales evitan un bus sobre la mesa (proscrito en 568) y permiten laptops itinerantes. |
| **Capacitación** | Árbol (por filas) | 10 hosts en filas de pupitres. El switch de depto. es la raíz; cada fila se trata como rama (tomas dobles PR01–PR04) y el podio es una rama aparte (PR05). Físicamente sigue siendo estrella en el switch, **pero la canalización y el etiquetado son arbóreos** (una derivación por fila). Un bus coaxial o daisy-chain de PCs se descartó: un host caído no debe partir el aula. |
| **Diseño e Innovación** | Estrella + enlace dedicado a servidor | 7 puestos creativos en estrella sobre la mesa central; el servidor de QA/repositorios tiene **toma unitaria propia** (PR05) para no compartir faceplate con un laptop. Criticidad media-alta del servidor local. |
| **Backend** | Estrella | 6 desarrolladores en dos bancadas + servidor de depto. Topología más barata y suficiente: el código crítico se replica hacia los 3 servidores del DC, no depende de malla local. |
| **Data Center** | Malla parcial | 3 servidores principales. Cada uno tiene toma unitaria al SW-DC **y** se documenta un segundo puerto NIC hacia el mismo switch (enlace de respaldo en el propio rack). No es malla completa servidor–servidor (caro e innecesario en Capa 1 de un solo switch), sí es **parcial**: dual-homing al switch de DC. Criticidad máxima. |

Ningún departamento usa anillo ni bus como topología principal: ambos penalizan la localización de fallas y no cumplen el espíritu de cableado estructurado (enlaces punto a punto desde un concentrador).

---

## 5. Puntos de red y tipo de toma

Criterio: **una posición RJ45 por host**. Si dos hosts comparten escritorio, faceplate doble; tres en el mismo mostrador, triple; servidores y puestos aislados, unitaria.

| Etiqueta de toma | Depto. | Tipo | Hosts que atiende |
|------------------|--------|------|-------------------|
| Direccion-PR01 | Dirección | Doble | DIR-PC01, DIR-PC02 |
| Direccion-PR02 | Dirección | Doble | DIR-PC03, DIR-LT01 |
| Recepcion-PR01 | Recepción | Triple | REC-PC01, REC-PC02, REC-LT01 |
| Recepcion-PR02 | Recepción | Unitaria | REC-SRV01 |
| Legal-PR01 | Legal | Doble | LEG-PC01, LEG-PC02 |
| Legal-PR02 | Legal | Doble | LEG-PC03, LEG-LT01 |
| RRHH-PR01 | RRHH | Doble | RRHH-PC01, RRHH-PC02 |
| RRHH-PR02 | RRHH | Doble | RRHH-LT01, RRHH-PC03 |
| RRHH-PR03 | RRHH | Doble | RRHH-PC04, RRHH-LT02 |
| RRHH-PR04 | RRHH | Doble | RRHH-PC05, RRHH-LT03 |
| Capacitacion-PR01 | Capacitación | Doble | CAP-PC01, CAP-PC02 |
| Capacitacion-PR02 | Capacitación | Doble | CAP-PC03, CAP-PC04 |
| Capacitacion-PR03 | Capacitación | Doble | CAP-PC05, CAP-PC06 |
| Capacitacion-PR04 | Capacitación | Doble | CAP-PC07, CAP-PC08 |
| Capacitacion-PR05 | Capacitación | Doble | CAP-LT01, CAP-LT02 |
| Diseno-PR01 | Diseño | Doble | DIS-PC01, DIS-PC02 |
| Diseno-PR02 | Diseño | Doble | DIS-LT01, DIS-PC03 |
| Diseno-PR03 | Diseño | Doble | DIS-PC04, DIS-LT02 |
| Diseno-PR04 | Diseño | Unitaria | DIS-LT03 |
| Diseno-PR05 | Diseño | Unitaria | DIS-SRV01 |
| Backend-PR01 | Backend | Doble | BCK-PC01, BCK-PC02 |
| Backend-PR02 | Backend | Doble | BCK-PC03, BCK-PC04 |
| Backend-PR03 | Backend | Doble | BCK-PC05, BCK-LT01 |
| Backend-PR04 | Backend | Unitaria | BCK-SRV01 |
| DataCenter-PR01 | Data Center | Unitaria | DC-SRV01 |
| DataCenter-PR02 | Data Center | Unitaria | DC-SRV02 |
| DataCenter-PR03 | Data Center | Unitaria | DC-SRV03 |

Las tomas se marcan sobre el plano (rombos U/D/T) en `diagrama_diseno_fisico.png`.

---

## 6. Cableado horizontal

### 6.1 Medio, categoría y ancho de banda

| Segmento | Medio | Categoría / clase | Ancho de banda | Aplicación |
|----------|-------|-------------------|----------------|------------|
| Switch de depto. → toma → host | UTP 4 pares, 100 Ω | **Cat 6A / Clase EA** | 500 MHz | 1000BASE-T hoy; 10GBASE-T hasta 100 m mañana |
| Patch cords IDF y estación | UTP Cat 6A | Cat 6A | 500 MHz | Mismos canales |
| Servidores de DC (opcional DAC futuro) | UTP Cat 6A en esta práctica | Cat 6A | 500 MHz | Homogeneidad del inventario |

**Por qué Cat 6A y no Cat 5e/6:** el edificio es de software (repos, CI, artefactos, mesas de diseño). Cat 5e se queda en 1 Gb/s. Cat 6 alcanza 10 Gb/s solo hasta ~55 m y con alien crosstalk peor. Cat 6A garantiza 10GBASE-T a 100 m y es el mínimo razonable en un diseño 2026 para no recablear en 3–5 años. Todas las distancias reales son << 55 m, pero el costo incremental Cat 6 → 6A es menor que una segunda mano de obra.

**Por qué no fibra al escritorio:** 48 transceptores + ODF por depto. disparan el presupuesto y no hay distancias ni EMI que lo justifiquen.

Ponchado: **T568B en ambos extremos** (jack de la toma y jack del patch panel del IDF). Ver sección 13.

### 6.2 Distancias estimadas (planta + 25 % de holgura)

Escala del plano: 26 m de frente, 16 m de fondo, Hall Central de 2 m a la cota y = 8–10 m, Data Center 6 × 4 m al noreste. Las rutas **siguen la escalerilla** (no diagonal a través de muros).

Distancia de **enlace permanente horizontal** = switch de departamento → bandeja del depto. → faceplate. El troncal se cuenta aparte (sección 7).

Valores medios por departamento (un drop por puerto):

| Depto. | Puertos | Dist. media (m) | Dist. máx. (m) | Metros brutos | +25 % slack | Subtotal (m) |
|--------|---------|-----------------|----------------|---------------|-------------|--------------|
| Dirección | 4 | 7.5 | 9.0 | 30.0 | 7.5 | 37.5 |
| Recepción | 4 | 8.0 | 11.0 | 32.0 | 8.0 | 40.0 |
| Legal | 4 | 6.0 | 8.0 | 24.0 | 6.0 | 30.0 |
| RRHH | 8 | 8.5 | 11.0 | 68.0 | 17.0 | 85.0 |
| Capacitación | 10 | 7.0 | 10.0 | 70.0 | 17.5 | 87.5 |
| Diseño | 8 | 7.5 | 10.0 | 60.0 | 15.0 | 75.0 |
| Backend | 7 | 6.5 | 9.0 | 45.5 | 11.4 | 56.9 |
| Data Center | 3 | 3.0 | 4.0 | 9.0 | 2.3 | 11.3 |
| **Total permanente** | **48** | | **11.0 < 90** | 338.5 | | **423.2** |

Ningún permanente supera 90 m. El canal completo (permanente + cordón de 3 m + cordón de 1 m) permanece < 100 m.

### 6.3 Cordones y desperdicio de corte

| Concepto | Metros |
|----------|--------|
| Enlaces permanentes (con slack) | 423.2 |
| Desperdicio de corte / fallos de certificación (~12 %) | 50.8 |
| Reserva de mantenimiento (cambios de layout 1 año) | 40.0 |
| **Total UTP Cat 6A a comprar** | **≈ 514 m** |

### 6.4 Bobinas de 305 m

\[
\lceil 514 / 305 \rceil = 2 \text{ bobinas}
\]

Se compran **3 bobinas de 305 m (915 m)** y no 2, por tres razones:

1. Una bobina se dedica a **Dirección + RRHH + Capacitación** (oeste, ~210 m).
2. La segunda a **Recepción + Legal + Diseño + Backend + DC** (~230 m).
3. La tercera cubre **certificación repetida, el troncal de cobre de respaldo (20 m), errores de tiro y crecimiento de 8–10 puestos**. Dejar el proyecto en el límite de 2 × 305 m obliga a un pedido de emergencia a mitad de obra.

**Conclusión de materiales de cobre:** 3 × 305 m Cat 6A.

---

## 7. Cableado troncal

### 7.1 Función

El troncal une el **SW-CORE (MDF)** con cada **switch de departamento**. En el diagrama es la línea **roja gruesa**, etiquetada `MDF-[Área]`.

### 7.2 Medio seleccionado

| Enlace | Medio | Velocidad | Motivo |
|--------|-------|-----------|--------|
| MDF → Dirección, Recepción, Legal, RRHH, Capacitación, Diseño, Backend, Data Center | **Fibra multimodo OM4**, 2 hilos (dúplex LC), indoor | 10GBASE-SR (850 nm) | Uplink de 10 Gb/s independiente del cobre horizontal; inmunidad EMI de UPS/HVAC; escalable a 40G-SR4 reutilizando OM4 |
| MDF → Legal (respaldo) | UTP Cat 6A | 1/10GBASE-T | Depto. más cercano (~11 m). Solo contingencia si falla el par de fibra Legal |

**Por qué no UTP Cat 6A en todos los uplinks como diseño principal:** aunque las distancias (11–38 m) caben en 10GBASE-T, ocho uplinks de cobre ocuparían 8 puertos del core que la práctica pide reservar alineados al patch panel de 48, mezclarían haces de 10G cobre (disipación, alien crosstalk en la misma bandeja que el horizontal) y no aislarían galvánicamente el MDF de los IDF. La fibra, con un solo cable de 12 hilos, transporta los 8 dúplex + 4 fibras de reserva en **un** tiro de bandeja.

**Por qué OM4 y no OS2 (monomodo):** tramos < 40 m. OS2 encarece transceptores (LR) sin beneficio. OM4 SR es el estándar de backbone de campus corto y de data center.

**Por qué no OM3:** el diferencial de precio es mínimo; OM4 duplica el alcance SR y deja margen si QuetzalDev abre un segundo nivel encima (bajante vertical futura).

### 7.3 Distancias de troncal (ruta de escalerilla)

Ruta común: MDF → corredor secundario (1.5 m) → extremo este del Hall Central → oeste según el drop.

| Etiqueta | Destino | Dist. planta (m) | +25 % | Fibra a instalar (m) |
|----------|---------|-------------------|-------|----------------------|
| MDF-Direccion | SW-DIR | 30.5 | 38.1 | 38 |
| MDF-Recepcion | SW-REC | 20.5 | 25.6 | 26 |
| MDF-Legal | SW-LEG | 11.0 | 13.8 | 14 |
| MDF-RRHH | SW-RRHH | 32.0 | 40.0 | 40 |
| MDF-Capacitacion | SW-CAP | 26.5 | 33.1 | 33 |
| MDF-Diseno | SW-DIS | 16.5 | 20.6 | 21 |
| MDF-Backend | SW-BCK | 10.8 | 13.5 | 14 |
| MDF-DataCenter | SW-DC | 2.5 | 3.1 | 4 |
| **Cable 12 hilos (un solo tiro al oeste)** | — | 32 m de bandeja | 40 | **60 m comprados** (incluye reservas y terminaciones) |

El cable de 12 hilos se tiende **una vez** a lo largo de la escalerilla; en cada drop de depto. se derivan 2 fibras (fusión o cassette preterminado). Eso es más limpio que ocho dúplex sueltos.

Respaldo cobre `MDF-Legal-COBRE`: 14 m permanentes, cordones straight/crossover según sección 13.

---

## 8. Dimensionamiento de patch panel y switch del edificio

La práctica exige: *si hay N puntos de red, patch panel de N puertos y switch ≥ N*.

| Magnitud | Valor | Equipo |
|----------|-------|--------|
| Puntos de red (puertos RJ45 de usuario + servidores) | **48** | — |
| Patch panel del MDF | **48 puertos** | 2 × Panduit CP24BLY |
| Switch del edificio | **48 puertos de cobre** + 4 SFP+ | Cisco Catalyst 9200-48P-E |

Los 48 puertos de cobre del core **no** terminan los 48 horizontales (esos terminan en los IDF de cada depto.). Terminan:

- 8 uplinks de cobre de respaldo / crecimiento (hoy 1 usado: Legal).
- Puertos de gestión, sonda de monitoreo y WAN/firewall futuro.
- Holgura exigida por el enunciado (paridad patch panel ↔ switch).

Los horizontales de cada depto. terminan en **su** patch panel de 24 puertos (ocupación máxima 10/24 en Capacitación). El ODF de 12 LC atiende las 8 troncales de fibra + 4 oscuras.

Ocupación de puertos de acceso (host + 1 uplink SFP, sin contar PoE AP):

| Switch | Hosts | Uplink | Puertos usados / disponibles | Holgura |
|--------|-------|--------|------------------------------|---------|
| SW-DIR 8P | 4 | 1 | 5 / 8 | 3 |
| SW-REC 8P | 4 | 1 | 5 / 8 | 3 |
| SW-LEG 8P | 4 | 1 | 5 / 8 | 3 |
| SW-DC 8P | 3 (+3 NIC backup) | 1 | 7 / 8 | 1 |
| SW-RRHH 16P | 8 | 1 | 9 / 16 | 7 |
| SW-CAP 16P | 10 | 1 | 11 / 16 | 5 |
| SW-DIS 16P | 8 | 1 | 9 / 16 | 7 |
| SW-BCK 16P | 7 | 1 | 8 / 16 | 8 |
| SW-CORE 48P | 8 SFP+ a depto. | — | 8 / 48+4 | alta |

---

## 9. Justificación del equipo activo

| Elemento | Función en el flujo físico |
|----------|----------------------------|
| **Toma RJ45** | Punto de demarcación usuario. Termina el permanente T568B. |
| **Cable horizontal Cat 6A** | Canal permanente IDF ↔ toma. |
| **Patch panel IDF** | Ordena los permanentes; permite recablear un puesto cambiando un cordón de 1 m, no el muro. |
| **Switch de departamento** | Concentrador de Capa 2 de acceso; reduce el número de fibras al MDF de 48 a 8. |
| **Fibra OM4 + ODF** | Troncal; el ODF es el equivalente óptico del patch panel. |
| **SW-CORE** | Único switch principal: agrega los 8 IDF y será el futuro peer del firewall. |
| **Patch panel MDF 48P** | Cobre de respaldo, out-of-band y crecimiento; cumple dimensionamiento N = 48. |
| **Transceptores SFP-10G-SR** | Convierten el puerto SFP+ en luz 850 nm. |
| **UPS + PDU** | Energía limpia al plano de control de la red. |
| **Rack 42U** | Orden mecánico, tierra, flujo de aire. |

Sin patch panel, cada movimiento de personal implicaría reponchar el permanente (viola el concepto de cableado estructurado). Sin switch de depto., 48 fibras o 48 cobres llegarían al MDF (bandeja saturada y core más caro de 48 SFP).

---

## 10. Canalización

| Tramo | Tipo | Justificación |
|-------|------|----------------|
| Hall Central (26 m) y corredor secundario | **Escalerilla metálica cerrada** 300 × 100 mm con tapa | Troncal de fibra + futuros APs + posibles cámaras. La tapa cumple TIA-569 en zona de circulación (protege de polvo y de “colgar” decoración). Abierta se descartó: el hall es visible al cliente. PVC no ofrece tierra ni resistencia al aplastamiento. |
| Bajantes muro → IDF mural 12U | EMT ¾" rígido | Corto, estético, código eléctrico. |
| Interior de oficina (mesa / sillas) | Canaleta metálica de piso / zócalo Panduit Pan-Way | No se tira UTP suelto bajo sillas (seguridad y radio de curvatura Cat 6A ≥ 4× diámetro). |
| Interior del Data Center | Escalerilla corta + anillos de rack | 4 m; se evita falso piso (el anexo es pequeño y el plano no lo indica). |

Separación de energía: la bandeja de datos corre por el eje del Hall; la acometida eléctrica se supone por el perímetro (práctica 569: distancia a conductores de potencia). El cruce perpendicular, si ocurre, se hace a 90°.

Fill: 12 hilos FO + 48 UTP no coinciden en el mismo metro de bandeja (los UTP entran/salen en cada depto.). El tramo más cargado (este del hall, cerca de Backend/Legal) lleva el backbone 12FO + ~15 UTP de Legal/Backend: fill < 40 % de 300 × 100 mm.

---

## 11. Rack / gabinete del MDF

**Se elige rack de piso 42U × 800 mm de fondo, no gabinete de pared.**

Motivos:

1. El Data Center tiene 6 × 4 m: hay huella para un rack de 60 × 107 cm más pasillo frontal/posterior de 1 m (TIA-942).
2. Equipo a alojar (aprox. 24U usados): UPS 3U, PDU, organizadores 4U, ODF 2U, 2 patch 24P = 2U, SW-CORE 1U, SW-DC 1U, bandeja de servidores 8–10U, holgura 50 % para firewall, NAS y segundo switch.
3. Un gabinete mural 12U **no entra** el UPS 1500 VA + core 48P + ODF + 3 servidores.
4. 800 mm de fondo aceptan switches Cisco y servidores 600–700 mm.
5. Tierra de rack unida a tierra de telecomunicaciones (TGB) del cuarto.

Los 8 departamentos usan **gabinete mural 12U** (IDF): switch 1U + patch 1U + organizador + 8U libres (AP, cámara, mini-UPS). No se pone rack de piso en oficinas de 5–7 m de frente.

---

## 12. Consumo eléctrico y UPS

La práctica pide estimar el **equipo activo de red** (core + switches de departamento). Los servidores se listan como carga recomendada aparte.

### 12.1 Carga de red (diseño)

| Equipo | Consumo típico (W) | Consumo máximo datasheet (W) | Cant. | Típico total (W) |
|--------|-------------------|------------------------------|-------|------------------|
| Catalyst 9200-48P (PoE casi idle; PCs no alimentadas por PoE) | 90 | 1440 (PoE full) | 1 | 90 |
| CBS350-8T | 12 | 18 | 4 | 48 |
| CBS350-16T | 22 | 32 | 4 | 88 |
| 16 × SFP-10G-SR | 1 | 1.5 | 16 | 16 |
| **Subtotal red** | | | | **242 W** |
| Factor de pérdidas PDU/cables 10 % | | | | 24 W |
| **Carga de diseño red** | | | | **≈ 266 W** |

No se activa el presupuesto PoE de 740 W+ del 9200-48P: las estaciones van con fuente propia. El modelo 48P se eligió por **conteo de puertos**, no para alimentar 48 teléfonos hoy. Si en el futuro hay AP Wi-Fi 6, la misma UPS **no** cubre PoE masivo; habría que subir a 3000 VA.

### 12.2 Autonomía objetivo

Objetivo: **30 minutos** de red de datos (apagado ordenado, continuidad de reuniones de dirección y cierre de compilaciones). Energía requerida:

\[
266\,\mathrm{W} \times 0{,}5\,\mathrm{h} = 133\,\mathrm{Wh}
\]

APC Smart-UPS **SMT1500C** (1 440 VA / 1 000 W, batería ~150–180 Wh útiles en el primer tercio de curva) entrega, a 270 W, del orden de **20–35 min** según temperatura. Es el mínimo profesional.

**Propuesta:** 1 × SMT1500C en el MDF, alimentando **solo** SW-CORE, ODF activo (si aplica), SW-DC y, mediante un circuito derivado a IDF, los 7 CBS350 (consumo bajo). Los PCs y laptops **no** van a esta UPS.

### 12.3 Servidores (recomendación, fuera del mínimo de la rúbrica)

6 servidores × 250 W típicos ≈ 1 500 W → UPS 3 kVA (p. ej. APC SRT3000XLT) **aparte**. Mezclar servidores y red en el SMT1500 saturaría el inverter.

---

## 13. Normas de ponchado T568A / T568B

### 13.1 Estándar de planta

Toda la planta horizontal se poncha **T568B en ambos extremos** (toma y patch panel). Es el estándar de facto en Guatemala y en kits Cisco / Panduit de datos. Mezclar A y B en el mismo permanente crea un cable cruzado **accidental**.

### 13.2 Straight-through vs crossover

| Tipo | Terminación | Cuándo se usa en este diseño |
|------|-------------|------------------------------|
| **Straight-through** | Mismo código (B–B o A–A) | Dispositivos de **capas distintas** en el modelo clásico: host (PC, laptop, servidor, impresora) ↔ switch; patch panel es pasivo y no cambia el criterio. **Todos los 48 horizontales y los 48 cordones de estación.** |
| **Crossover** | Un extremo T568B y el otro T568A (equivalente a cruzar pares 2 y 3: pines 1-2 con 3-6) | Dispositivos de **la misma capa** sin Auto-MDIX: switch ↔ switch, PC ↔ PC. En este proyecto: **únicamente el respaldo de cobre MDF–Legal** (`MDF-Legal-COBRE`), por si el SFP falla y se une SW-CORE con SW-LEG por RJ45. |

Los CBS350 y el Catalyst 9200 tienen **Auto-MDIX**: en la práctica un straight-through también funcionaría en el uplink de cobre. Se documenta el crossover **como evidencia de Capa 1** exigida por la rúbrica y como cable etiquetado de contingencia (no depende del Auto-MDIX).

Los uplinks de **fibra** no se “ponchan” en A/B: el cruce TX/RX lo resuelve el cordón LC (posición A-B).

### 13.3 Tabla de uso por tipo de enlace

| Enlace | Extremo 1 | Extremo 2 | Cable |
|--------|-----------|-----------|-------|
| Host ↔ toma (cordón de 3 m) | NIC | Jack | Straight-through T568B |
| Permanente toma ↔ patch IDF | Jack T568B | Jack T568B | Straight-through |
| Patch IDF ↔ switch acceso (1 m) | Panel | SW | Straight-through T568B |
| SW acceso ↔ SW-CORE (fibra) | SFP+ | SFP+ | OM4 LC (no UTP) |
| SW-CORE ↔ SW-LEG (cobre de respaldo) | RJ45 core | RJ45 LEG | **Crossover** (B en core, A en LEG) |
| Servidor DC NIC1 ↔ SW-DC | NIC | SW | Straight-through |
| Servidor DC NIC2 ↔ SW-DC (malla parcial) | NIC | SW | Straight-through |

### 13.4 Disposición de pines

Convención: pin 1 a la izquierda con el clip del RJ45 hacia abajo y los contactos visibles.

#### T568B (straight-through: ambos extremos idénticos)

| Pin | Par | Color T568B | Función 10/100/1000 |
|-----|-----|-------------|---------------------|
| 1 | 2 | Blanco-Naranja | Tx+ / BI_DA+ |
| 2 | 2 | Naranja | Tx− / BI_DA− |
| 3 | 3 | Blanco-Verde | Rx+ / BI_DB+ |
| 4 | 1 | Azul | BI_DC+ |
| 5 | 1 | Blanco-Azul | BI_DC− |
| 6 | 3 | Verde | Rx− / BI_DB− |
| 7 | 4 | Blanco-Marrón | BI_DD+ |
| 8 | 4 | Marrón | BI_DD− |

```text
  Straight-through T568B            Straight-through T568B
  Extremo A                         Extremo B
  Pin 1  Blanco/Naranja  ─────────  Blanco/Naranja  Pin 1
  Pin 2  Naranja         ─────────  Naranja         Pin 2
  Pin 3  Blanco/Verde    ─────────  Blanco/Verde    Pin 3
  Pin 4  Azul            ─────────  Azul            Pin 4
  Pin 5  Blanco/Azul     ─────────  Blanco/Azul     Pin 5
  Pin 6  Verde           ─────────  Verde           Pin 6
  Pin 7  Blanco/Marrón   ─────────  Blanco/Marrón   Pin 7
  Pin 8  Marrón          ─────────  Marrón          Pin 8
```

#### T568A (se usa solo en un extremo del crossover)

| Pin | Par | Color T568A |
|-----|-----|-------------|
| 1 | 3 | Blanco-Verde |
| 2 | 3 | Verde |
| 3 | 2 | Blanco-Naranja |
| 4 | 1 | Azul |
| 5 | 1 | Blanco-Azul |
| 6 | 2 | Naranja |
| 7 | 4 | Blanco-Marrón |
| 8 | 4 | Marrón |

#### Crossover (T568B ↔ T568A) — enlace `MDF-Legal-COBRE`

```text
  Extremo CORE (T568B)              Extremo LEG (T568A)
  Pin 1  Blanco/Naranja  ─────────  Blanco/Verde    Pin 1
  Pin 2  Naranja         ─────────  Verde           Pin 2
  Pin 3  Blanco/Verde    ─────────  Blanco/Naranja  Pin 3
  Pin 4  Azul            ─────────  Azul            Pin 4
  Pin 5  Blanco/Azul     ─────────  Blanco/Azul     Pin 5
  Pin 6  Verde           ─────────  Naranja         Pin 6
  Pin 7  Blanco/Marrón   ─────────  Blanco/Marrón   Pin 7
  Pin 8  Marrón          ─────────  Marrón          Pin 8
```

En 1 Gb/s los cuatro pares son bidireccionales; el cruce 1-2 ↔ 3-6 sigue siendo el crossover “clásico” que Auto-MDIX emula. Un crossover 10G completo cruzaría también el par 1 y 4 (pines 4-5 con 7-8); para el respaldo a 1G del CBS350 basta el cruce de pares 2 y 3.

---

## 14. Etiquetado de cables y comparación TIA/EIA-606

### 14.1 Formato de la práctica

- Horizontal: `[Área/Departamento]-[Número de Punto de Red]`  
  Ejemplos: `Recepcion-PR01`, `Legal-PR03`, `Capacitacion-PR05`.
- Troncal: `MDF-[Área/Departamento]`  
  Ejemplos: `MDF-Recepcion`, `MDF-Backend`, `MDF-DataCenter`.

Cada etiqueta se coloca en **ambos extremos** del permanente (jack y panel) y en la fibra (ODF y SFP del acceso).

### 14.2 Tabla maestra de etiquetas

| Etiqueta | Tipo | Origen | Destino |
|----------|------|--------|---------|
| Direccion-PR01 | Horizontal | SW-DIR / PP-DIR | Toma doble Dirección |
| Direccion-PR02 | Horizontal | SW-DIR / PP-DIR | Toma doble Dirección |
| Recepcion-PR01 | Horizontal | SW-REC | Toma triple mostrador |
| Recepcion-PR02 | Horizontal | SW-REC | Servidor recepción |
| Legal-PR01 | Horizontal | SW-LEG | Toma doble escritorio |
| Legal-PR02 | Horizontal | SW-LEG | Toma doble juntas |
| RRHH-PR01 … PR04 | Horizontal | SW-RRHH | Cuatro tomas dobles |
| Capacitacion-PR01 … PR05 | Horizontal | SW-CAP | Cuatro filas + podio |
| Diseno-PR01 … PR05 | Horizontal | SW-DIS | Mesa + laptop + servidor |
| Backend-PR01 … PR04 | Horizontal | SW-BCK | Bancadas + servidor |
| DataCenter-PR01 … PR03 | Horizontal | SW-DC | Tres servidores |
| MDF-Direccion | Troncal FO | ODF / SW-CORE | SW-DIR |
| MDF-Recepcion | Troncal FO | ODF / SW-CORE | SW-REC |
| MDF-Legal | Troncal FO | ODF / SW-CORE | SW-LEG |
| MDF-RRHH | Troncal FO | ODF / SW-CORE | SW-RRHH |
| MDF-Capacitacion | Troncal FO | ODF / SW-CORE | SW-CAP |
| MDF-Diseno | Troncal FO | ODF / SW-CORE | SW-DIS |
| MDF-Backend | Troncal FO | ODF / SW-CORE | SW-BCK |
| MDF-DataCenter | Troncal FO | ODF / SW-CORE | SW-DC |
| MDF-Legal-COBRE | Troncal UTP crossover | SW-CORE | SW-LEG |

Los cordones de 1 m heredan el ID del puerto de panel (`PP-CAP-07` → `SW-CAP-07`) en un entorno real; en esta práctica el ID visible exigido es el de permanente `Capacitacion-PR##`.

### 14.3 Comparación con TIA/EIA-606-C

TIA-606-C (*Administration Standard for Telecommunications Infrastructure*) define un sistema de identificadores **únicos y jerárquicos** para espacios, racks, paneles, puertos, cables y rutas, más un **registro de administración** (base de datos) que sobrevive al técnico que instaló la red.

| # | El formato de la práctica | Lo que exige TIA-606-C | Diferencia concreta |
|---|---------------------------|------------------------|---------------------|
| 1 | `Recepcion-PR01` identifica el cable por nombre de depto. + entero local | Identificador de cable del tipo `FS001/R1-1A-24` o `1A-B01-01 / 1B-A03-12` (espacio + rack + panel + puerto en **ambos** extremos) | La práctica **no incluye el espacio ni el puerto de panel**. Dos edificios o dos pisos no podrían reutilizar `Recepcion-PR01` sin colisión; 606 exige unicidad global. |
| 2 | Un solo texto plano, sin clase de identificador | Codificación por **clases** (fs, rs, cs, ts: floor space, rack, cable, termination) y **colores de etiqueta** (p. ej. azul = LAN, verde = red, púrpura = común) | Aquí no hay color administrativo ni prefijo de clase: un técnico no distingue a simple vista un horizontal de un troncal salvo por el prefijo `MDF-`. |
| 3 (contexto) | La tabla vive en este Markdown | 606 exige registros de **rutas** (pathway IDs), **espacios** (ER, TR, TE) y work orders de movimiento/altas/bajas | El manual de la práctica es estático; no es un sistema de administración. |

**Por qué en un MDF / data center real se adoptaría 606 completo:** en QuetzalDev, el día que Legal se mude tres metros o se agregue un segundo rack, `Legal-PR01` deja de describir el puerto físico. Un identificador 606 (`DC01-R01-PP02-05` ↔ `LEG-R01-PP01-03`) sigue siendo verdadero, se audita con software (p. ej. iTRACS / planillas 606) y permite que un contratista distinto certifique sin preguntar al estudiante que diseñó la red. El esquema simplificado de la práctica es **pedagógico y suficiente para 48 puntos en un piso**; no escala a auditorías ISO ni a centros de datos con cientos de jumper.

---

## 15. Flujo de conexión end-to-end

Ejemplo: laptop de capacitación `CAP-LT01` consulta un repositorio en `DC-SRV01`.

```text
CAP-LT01 (NIC)
    │  cordón estación Cat 6A 3 m  —  straight-through T568B
    │  etiqueta de estación: Capacitacion-PR05
    ▼
Toma doble Capacitacion-PR05 (jack Mini-Com Cat 6A, T568B)
    │  permanente UTP Cat 6A por zócalo → EMT → IDF mural Capacitación
    ▼
Patch panel PP-CAP puerto 09/10 (T568B)
    │  cordón 1 m Cat 6A  —  straight-through
    ▼
SW-CAP (CBS350-16T) puerto de acceso
    │  SFP-10G-SR + patch LC OM4 2 m
    ▼
Cassette / derivación del backbone 12 hilos
    │  fibra OM4  —  etiqueta MDF-Capacitacion
    │  (escalerilla cerrada por Hall Central + corredor)
    ▼
ODF del MDF (LC)
    │  patch LC 2 m
    ▼
SW-CORE (Catalyst 9200-48P) puerto SFP+
    │  fibra MDF-DataCenter (muy corta, mismo rack)
    ▼
SW-DC (CBS350-8T)
    │  cordón 1 m Cat 6A  —  straight-through
    ▼
Patch panel PP-DC / toma DataCenter-PR01
    │  permanente corto en el rack
    ▼
DC-SRV01 (NIC1)
```

El retorno simétrico usa los mismos permanentes. No hay NAT ni VLAN en este documento: el flujo describe **solo el camino metálico/óptico**.

Diagrama lógico de Capa 1 (no es simulación):

```mermaid
flowchart LR
  LT[CAP-LT01]
  TOMA[Toma Capacitacion-PR05]
  PP[PP-CAP]
  SWA[SW-CAP]
  FO[FO MDF-Capacitacion]
  CORE[SW-CORE]
  FODC[FO MDF-DataCenter]
  SWDC[SW-DC]
  SRV[DC-SRV01]
  LT --> TOMA --> PP --> SWA --> FO --> CORE --> FODC --> SWDC --> SRV
```

---

## 16. Presupuesto estimado

Precios de mercado Guatemala / listados regionales 2025–2026, **sin IVA**, redondeados a quetzales. Tipo de cambio de referencia: Q 7.80 / USD. Son **estimaciones de ingeniería** para decidir compra directa vs integrador (ver Informe de desarrollo), no una cotización firmada.

| Ítem | Cant. | P. unitario (Q) | Subtotal (Q) |
|------|-------|-----------------|--------------|
| Cisco Catalyst C9200-48P-E + red DNA Essential 3 años | 1 | 32 800 | 32 800 |
| Módulo C9200-NM-4X | 1 | 4 200 | 4 200 |
| Cisco CBS350-8T-E-2G | 4 | 1 350 | 5 400 |
| Cisco CBS350-16T-E-2G | 4 | 2 150 | 8 600 |
| Cisco SFP-10G-SR | 16 | 780 | 12 480 |
| Panduit CP24BLY patch panel 24P | 10 | 890 | 8 900 |
| Panduit CJ6X88TGBU jack Cat 6A | 48 | 95 | 4 560 |
| Faceplates Mini-Com 1/2/4 pos. | 27 | 45 | 1 215 |
| Siemon UTP Cat 6A bobina 305 m | 3 | 2 850 | 8 550 |
| Cordón Cat 6A 1 m | 48 | 55 | 2 640 |
| Cordón Cat 6A 3 m | 48 | 75 | 3 600 |
| Cable FO indoor 12 hilos OM4 (60 m) | 1 | 2 400 | 2 400 |
| ODF + cassettes LC OM4 | 1 | 3 100 | 3 100 |
| Patch cord LC-LC OM4 2 m | 16 | 120 | 1 920 |
| Escalerilla cerrada 300×100 + tapa + soportes | 32 m | 285 / m | 9 120 |
| EMT, cajas, canaleta Pan-Way | 1 lote | 3 800 | 3 800 |
| Rack piso 42U 800 mm + kit tierra | 1 | 7 400 | 7 400 |
| Gabinete mural 12U | 8 | 1 150 | 9 200 |
| APC SMT1500C | 1 | 4 350 | 4 350 |
| PDU metered APC | 2 | 1 680 | 3 360 |
| Organizadores / etiquetadoras / bridas | 1 lote | 1 850 | 1 850 |
| Certificación Fluke DSX (alquiler 2 días) o servicio | 1 | 3 200 | 3 200 |
| **Subtotal materiales y equipo** | | | **142 445** |
| Imprevistos 4.5 % | | | 6 495 |
| **Total estimado** | | | **Q 148 940.00** |

Mano de obra de un integrador certificado (tiro, ponchado, fusión, certificación, as-built) se estima en **Q 18 000–25 000** adicionales si no se autogestiona. Esa cifra **no** está en el total de materiales; se discute en el informe de desarrollo.

Costo por puerto de usuario (48): ≈ **Q 3 103** en materiales, coherente con un diseño Cat 6A + FO de oficina pequeña.

---

## 17. Referencias

- Odom, W. (2019). *CCNA 200-301 Official Cert Guide*, Vol. 1. Cisco Press.
- TIA-568.2-D, TIA-568.3-D, TIA-569-E, TIA-606-C, TIA-942-B.
- Cisco. Fichas Catalyst 9200 y CBS350.
- Panduit. *Catálogo infraestructura de redes LATAM* (Mini-Com, Pan-Way).
- Siemon. Catálogo 2022 (cobre 6A y fibra LightVerse / TBO).
- APC by Schneider Electric. Curvas de runtime Smart-UPS SMT1500.
- Enunciado *Redes de Computadoras 1 — Práctica 1, 2S 2026*, FIUSAC.
- Plano arquitectónico asignado a carnets terminación 8 y 9.

---

*Fin del manual técnico — QuetzalDev S.A. / 202300689*
