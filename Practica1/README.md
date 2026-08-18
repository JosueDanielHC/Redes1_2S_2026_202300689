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
| **Práctica** | Práctica 1 — Diseño físico de cableado estructurado (Capa 1 OSI) |
| **Cliente** | QuetzalDev S.A. |
| **Estudiante** | Josue Daniel Herrera Cottom |
| **Carné** | 202300689 |
| **Terminación de carné** | 9 (plano asignado: carnets 8 y 9) |
| **Repositorio** | [Redes1_2S_2026_202300689](https://github.com/) |
| **Semestre** | Segundo semestre 2026 |
| **Ponderación** | 7 pts |
| **Fecha de entrega** | 21 de agosto de 2026 |

---

# Práctica 1 — Infraestructura física de red para QuetzalDev S.A.

## Descripción general

QuetzalDev S.A. inauguró un edificio corporativo de un solo nivel (26 m × 16 m más un Data Center de 6 m × 4 m) y requiere, **antes de comprar e instalar equipo activo**, el diseño de la Capa 1 del modelo OSI: ubicación del cuarto de telecomunicaciones (MDF), topologías físicas por departamento, medios de transmisión, canalización, etiquetado y presupuesto.

Este repositorio contiene el diseño completo de cableado estructurado. **No incluye configuración lógica, direccionamiento IP ni simulación de dispositivos**; el alcance es exclusivamente físico, conforme al enunciado de la práctica.

La distribución de las 30 computadoras de escritorio y las 12 laptops entre departamentos es **propia del carné 202300689** (terminación 9), de modo que las topologías y mezclas de hosts no coinciden con las de otros estudiantes.

---

## Índice navegable

1. [Datos del estudiante y del proyecto](#universidad-de-san-carlos-de-guatemala)
2. [Descripción general](#descripción-general)
3. [Entregables](#entregables)
4. [Cómo leer el diagrama](#cómo-leer-el-diagrama)
5. [Resumen técnico ejecutivo](#resumen-técnico-ejecutivo)
6. [Estructura de la carpeta](#estructura-de-la-carpeta)
7. [Normativa de referencia](#normativa-de-referencia)
8. [Cómo regenerar el diagrama](#cómo-regenerar-el-diagrama)

### Documentos de la práctica

- [Manual técnico](Manual_Tecnico.md) — inventario, justificaciones, distancias, bobinas, T568A/B, TIA/EIA-606, flujo end-to-end y presupuesto.
- [Informe de desarrollo](Informe_Desarrollo.md) — proceso de diseño, retos del plano, compra individual vs proveedor y escalabilidad.
- [Diagrama de diseño físico](diagrama_diseno_fisico.png) — plano arquitectónico con MDF, hosts, tomas, troncal, horizontal, escalerilla y etiquetas.

---

## Entregables

| Archivo | Contenido |
|---------|-----------|
| `diagrama_diseno_fisico.png` | Diseño físico sobre el plano base: MDF, 48 puntos de red, 8 switches de acceso, switch core, tomas U/D/T, troncal (rojo), horizontal (color por depto), escalerilla (ámbar discontinua) y etiquetas `Depto-PR##` / `MDF-Depto`. |
| `Manual_Tecnico.md` | Documentación exhaustiva exigida por la rúbrica. |
| `Informe_Desarrollo.md` | Relato de ingeniería del proceso de diseño. |
| `plano_base.png` | Plano arquitectónico original (terminación 8/9). |
| `generar_diagrama.py` | Script de diagramación que produce el PNG a partir del plano. |

---

## Cómo leer el diagrama

- **Línea roja gruesa:** cableado troncal (fibra multimodo OM4, 10 GbE) entre el MDF y cada switch de departamento. Etiqueta: `MDF-[Área]`.
- **Líneas delgadas de color:** cableado horizontal UTP Cat 6A entre el switch de departamento y los hosts. Etiqueta: `[Área]-PR##`.
- **Línea ámbar discontinua:** escalerilla metálica cerrada en Hall Central y corredor secundario hacia el Data Center.
- **Rectángulo rojo en el Data Center:** MDF (rack de piso 42U: core, ODF, patch panel, UPS).
- **Naranja:** switches de acceso. **Azul:** PC. **Cian:** laptop. **Violeta:** servidor.
- **Rombo verde / naranja / magenta:** toma unitaria / doble / triple.

---

## Resumen técnico ejecutivo

| Elemento | Decisión |
|----------|----------|
| MDF | Data Center (6 × 4 m), único local técnico del edificio |
| Topología del edificio | Árbol (estrella jerárquica): 1 core → 8 switches de acceso → hosts |
| Horizontal | UTP Cat 6A, T568B, straight-through, canal ≤ 90 m |
| Troncal | Fibra OM4 (LC duplex) 10 GbE; cobre Cat 6A de respaldo MDF–Legal (crossover) |
| Puntos de red | 27 tomas / **48 puertos** de patch |
| Patch panel MDF | 2 × 24 puertos Cat 6A (48) |
| Switch del edificio | Cisco Catalyst 9200-48P (48 puertos de cobre + uplinks SFP+) |
| Canalización | Escalerilla metálica cerrada 300 × 100 mm + bajantes EMT |
| Rack | Gabinete de piso 42U × 800 mm (no gabinete de pared) |
| UPS | APC Smart-UPS SMT1500 (1.5 kVA) para equipo activo de red |
| Bobinas Cat 6A | 3 bobinas de 305 m |
| Inversión estimada | Q 148 940.00 (impuestos no incluidos) |

---

## Estructura de la carpeta

```text
Practica1/
├── README.md
├── Manual_Tecnico.md
├── Informe_Desarrollo.md
├── diagrama_diseno_fisico.png
├── plano_base.png
└── generar_diagrama.py
```

---

## Normativa de referencia

- TIA/EIA-568.2-D — cableado de pares trenzados y canales de 90 m + 10 m de cordones.
- TIA-568.3-D — cableado de fibra óptica.
- TIA-569-E — espacios y canalizaciones.
- TIA-606-C — administración e identificadores.
- TIA-942-B — salas de telecomunicaciones y centros de datos.
- ISO/IEC 11801 — clases de canal (clase EA = Cat 6A).

---

## Cómo regenerar el diagrama

Requiere Python 3 y Pillow:

```bash
pip install pillow
python generar_diagrama.py
```

El PNG se escribe en la misma carpeta. El diseño conceptual (cantidades, etiquetas y rutas) está documentado en el [Manual técnico](Manual_Tecnico.md) y no depende del script para ser evaluado.
