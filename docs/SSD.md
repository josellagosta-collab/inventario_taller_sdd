# SDD - Software Design Document

# Parte 1 - Arquitectura General y Estructura del Sistema

---

# 1. Información del documento

## Proyecto

Inventario Taller SDD

## Versión

1.0

## Estado

En desarrollo

## Metodología

Specification Driven Development (SDD)

## Tecnologías principales

- Python 3.x
- Django 5.x
- PostgreSQL
- Bootstrap 5
- HTML5
- CSS3
- JavaScript
- Git
- GitHub
- Jira

---

# 2. Objetivo técnico del sistema

El objetivo es desarrollar una aplicación web escalable y modular para gestionar el inventario completo de un taller de hardware e informática.

La aplicación deberá permitir:

- Registrar material.
- Gestionar ubicaciones.
- Gestionar préstamos.
- Gestionar incidencias.
- Gestionar mantenimientos.
- Gestionar usuarios.
- Gestionar auditoría.
- Generar informes.

La solución deberá estar preparada para futuras integraciones con tecnologías IoT e Industria 4.0.

---

# 3. Arquitectura general

La aplicación seguirá una arquitectura basada en el patrón MVT (Model View Template) de Django.

```text
+-----------------------+
|     Navegador Web     |
+-----------+-----------+
            |
            v
+-----------------------+
|       Django URLS     |
+-----------+-----------+
            |
            v
+-----------------------+
|     Django Views      |
+-----------+-----------+
            |
            v
+-----------------------+
|     Django Models     |
+-----------+-----------+
            |
            v
+-----------------------+
|      PostgreSQL       |
+-----------------------+
```

---

# 4. Arquitectura lógica

La aplicación se dividirá en módulos independientes.

```text
Inventario Taller SDD
│
├── Usuarios
├── Inventario
├── Ubicaciones
├── Préstamos
├── Incidencias
├── Mantenimiento
├── Auditoría
└── Informes
```

Cada módulo se implementará mediante una aplicación Django independiente.

---

# 5. Estructura física del proyecto

```text
inventario_taller_sdd/
│
├── docs/
│   ├── PRD.md
│   ├── SDD.md
│   ├── BACKLOG.md
│   └── MODELO_DATOS.md
│
├── inventario_taller/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   ├── wsgi.py
│   └── __init__.py
│
├── apps/
│   ├── usuarios/
│   ├── inventario/
│   ├── ubicaciones/
│   ├── prestamos/
│   ├── incidencias/
│   ├── mantenimiento/
│   ├── auditoria/
│   └── informes/
│
├── templates/
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── media/
│   ├── fotos_material/
│   ├── documentos/
│   └── informes/
│
├── tests/
│
├── requirements.txt
│
├── manage.py
│
└── README.md
```

---

# 6. Aplicaciones Django

## 6.1 App Usuarios

### Objetivo

Gestionar la autenticación y autorización del sistema.

### Responsabilidades

- Login.
- Logout.
- Gestión de usuarios.
- Gestión de grupos.
- Gestión de permisos.
- Recuperación de contraseña.

### Modelos previstos

```text
Rol
PerfilUsuario
```

### Casos de uso asociados

```text
CU001 Iniciar sesión
CU002 Cerrar sesión
CU003 Crear usuario
CU004 Modificar usuario
CU005 Desactivar usuario
```

---

## 6.2 App Inventario

### Objetivo

Gestionar todos los elementos inventariados.

### Responsabilidades

- Alta de material.
- Modificación de material.
- Baja de material.
- Consulta de material.
- Búsqueda de material.
- Gestión documental.

### Modelos previstos

```text
Categoria
Subcategoria
Material
Fotografia
Documento
Proveedor
```

### Casos de uso asociados

```text
CU100 Crear material
CU101 Modificar material
CU102 Eliminar material
CU103 Consultar material
CU104 Buscar material
```

---

## 6.3 App Ubicaciones

### Objetivo

Gestionar la ubicación física de cada elemento.

### Responsabilidades

- Gestión de edificios.
- Gestión de aulas.
- Gestión de armarios.
- Gestión de estanterías.
- Gestión de cajas.

### Modelos previstos

```text
Edificio
Aula
Armario
Estanteria
Caja
Ubicacion
```

### Casos de uso asociados

```text
CU200 Crear ubicación
CU201 Modificar ubicación
CU202 Consultar ubicación
```

---

## 6.4 App Préstamos

### Objetivo

Controlar el préstamo de material.

### Responsabilidades

- Registrar préstamo.
- Registrar devolución.
- Registrar renovación.
- Consultar histórico.

### Modelos previstos

```text
Prestamo
LineaPrestamo
```

### Casos de uso asociados

```text
CU300 Registrar préstamo
CU301 Registrar devolución
CU302 Renovar préstamo
CU303 Consultar histórico
```

---

## 6.5 App Incidencias

### Objetivo

Gestionar averías y problemas detectados.

### Responsabilidades

- Crear incidencias.
- Asignar incidencias.
- Resolver incidencias.
- Consultar histórico.

### Modelos previstos

```text
Incidencia
ComentarioIncidencia
```

### Casos de uso asociados

```text
CU400 Crear incidencia
CU401 Asignar incidencia
CU402 Resolver incidencia
```

---

## 6.6 App Mantenimiento

### Objetivo

Gestionar mantenimientos preventivos y correctivos.

### Responsabilidades

- Registrar mantenimiento.
- Consultar histórico.
- Programar revisiones.

### Modelos previstos

```text
Mantenimiento
PlanMantenimiento
```

### Casos de uso asociados

```text
CU500 Registrar mantenimiento
CU501 Programar revisión
CU502 Consultar histórico
```

---

## 6.7 App Auditoría

### Objetivo

Registrar todas las acciones críticas del sistema.

### Responsabilidades

- Registrar acciones.
- Consultar histórico.
- Trazabilidad.

### Modelos previstos

```text
RegistroAuditoria
```

### Casos de uso asociados

```text
CU600 Consultar auditoría
```

---

## 6.8 App Informes

### Objetivo

Generar documentación y estadísticas.

### Responsabilidades

- Informes PDF.
- Exportación Excel.
- Exportación CSV.
- Estadísticas.

### Modelos previstos

No requiere modelos propios inicialmente.

### Casos de uso asociados

```text
CU700 Exportar CSV
CU701 Exportar Excel
CU702 Generar PDF
CU703 Consultar estadísticas
```

---

# 7. Flujo principal del sistema

## Escenario típico

```text
Administrador inicia sesión
            │
            ▼
Consulta inventario
            │
            ▼
Alta de material
            │
            ▼
Asignación de ubicación
            │
            ▼
Material disponible
            │
            ▼
Préstamo
            │
            ▼
Devolución
            │
            ▼
Auditoría automática
```

---

# 8. Navegación principal

```text
Inicio
│
├── Dashboard
│
├── Inventario
│   ├── Listado
│   ├── Alta
│   ├── Búsqueda
│   └── Detalle
│
├── Ubicaciones
│
├── Préstamos
│
├── Incidencias
│
├── Mantenimiento
│
├── Informes
│
└── Administración
```

---

# 9. Principios de diseño

El sistema deberá cumplir:

## Modularidad

Cada funcionalidad deberá estar aislada en una aplicación Django.

## Escalabilidad

Se deberán poder añadir nuevos módulos sin modificar los existentes.

## Reutilización

Las funcionalidades comunes deberán implementarse una única vez.

## Seguridad

Todas las operaciones deberán estar protegidas por autenticación y permisos.

## Mantenibilidad

El código deberá seguir las buenas prácticas recomendadas por Django.

---

# 10. Preparación para futuras integraciones

La arquitectura deberá permitir incorporar posteriormente:

- Códigos QR.
- RFID.
- MQTT.
- ESP32.
- Raspberry Pi.
- PLC Omron NX102.
- Robot UR3.
- Sistemas OPC UA.
- Inteligencia Artificial.
- Aplicación móvil.

---

# Fin de la Parte 1
# Parte 2 - Modelo de Datos PostgreSQL

---

# 11. Diseño de la Base de Datos

## Objetivos del modelo de datos

La base de datos deberá:

- Almacenar toda la información del inventario.
- Mantener la integridad referencial.
- Permitir búsquedas rápidas.
- Permitir auditoría completa.
- Facilitar futuras ampliaciones.
- Mantener la trazabilidad histórica.

La base de datos utilizada será PostgreSQL.

---

# 12. Diagrama conceptual

```text
Usuario
│
├── Prestamo
│       │
│       └── Material
│
├── Incidencia
│       │
│       └── Material
│
└── RegistroAuditoria

Material
│
├── Categoria
├── Subcategoria
├── Ubicacion
├── Fotografia
├── Documento
├── Incidencia
├── Prestamo
└── Mantenimiento

Ubicacion
│
├── Edificio
├── Aula
├── Armario
├── Estanteria
└── Caja
```

---

# 13. Modelo de Usuarios

## Tabla Rol

### Descripción

Define los tipos de usuario del sistema.

### Campos

| Campo | Tipo | Restricciones |
|---------|---------|---------|
| id | BIGINT | PK |
| nombre | VARCHAR(50) | UNIQUE |
| descripcion | TEXT | NULL |

---

## Tabla PerfilUsuario

### Descripción

Extiende el modelo User de Django.

### Campos

| Campo | Tipo | Restricciones |
|---------|---------|---------|
| id | BIGINT | PK |
| user_id | FK | UNIQUE |
| rol_id | FK | NOT NULL |
| telefono | VARCHAR(20) | NULL |
| observaciones | TEXT | NULL |
| fecha_creacion | TIMESTAMP | NOT NULL |

---

# 14. Modelo de Inventario

## Tabla Categoria

### Campos

| Campo | Tipo |
|---------|---------|
| id | BIGINT |
| nombre | VARCHAR(100) |
| descripcion | TEXT |

### Ejemplos

- Redes
- Hardware
- IoT
- Robótica
- Electrónica

---

## Tabla Subcategoria

### Campos

| Campo | Tipo |
|---------|---------|
| id | BIGINT |
| categoria_id | FK |
| nombre | VARCHAR(100) |
| descripcion | TEXT |

### Ejemplos

- Router
- Switch
- PLC
- ESP32
- Raspberry Pi

---

## Tabla Proveedor

### Campos

| Campo | Tipo |
|---------|---------|
| id | BIGINT |
| nombre | VARCHAR(150) |
| telefono | VARCHAR(50) |
| email | VARCHAR(150) |
| web | VARCHAR(200) |
| observaciones | TEXT |

---

## Tabla Material

### Descripción

Tabla principal del sistema.

### Campos

| Campo | Tipo |
|---------|---------|
| id | BIGINT |
| codigo_inventario | VARCHAR(50) |
| nombre | VARCHAR(200) |
| descripcion | TEXT |
| categoria_id | FK |
| subcategoria_id | FK |
| proveedor_id | FK |
| marca | VARCHAR(100) |
| modelo | VARCHAR(100) |
| numero_serie | VARCHAR(200) |
| codigo_qr | VARCHAR(200) |
| cantidad | INTEGER |
| stock_minimo | INTEGER |
| precio_compra | DECIMAL(10,2) |
| fecha_compra | DATE |
| garantia_hasta | DATE |
| estado | VARCHAR(50) |
| ubicacion_id | FK |
| observaciones | TEXT |
| fecha_creacion | TIMESTAMP |
| fecha_actualizacion | TIMESTAMP |

---

## Estados permitidos

```text
Disponible
Prestado
Reservado
Averiado
En reparación
Fuera de servicio
Retirado
Perdido
```

---

# 15. Modelo de Ubicaciones

## Tabla Edificio

### Campos

| Campo | Tipo |
|---------|---------|
| id | BIGINT |
| nombre | VARCHAR(100) |
| descripcion | TEXT |

---

## Tabla Aula

### Campos

| Campo | Tipo |
|---------|---------|
| id | BIGINT |
| edificio_id | FK |
| nombre | VARCHAR(100) |
| descripcion | TEXT |

---

## Tabla Armario

### Campos

| Campo | Tipo |
|---------|---------|
| id | BIGINT |
| aula_id | FK |
| nombre | VARCHAR(100) |
| descripcion | TEXT |

---

## Tabla Estanteria

### Campos

| Campo | Tipo |
|---------|---------|
| id | BIGINT |
| armario_id | FK |
| nombre | VARCHAR(100) |
| descripcion | TEXT |

---

## Tabla Caja

### Campos

| Campo | Tipo |
|---------|---------|
| id | BIGINT |
| estanteria_id | FK |
| nombre | VARCHAR(100) |
| descripcion | TEXT |

---

## Tabla Ubicacion

### Campos

| Campo | Tipo |
|---------|---------|
| id | BIGINT |
| edificio_id | FK |
| aula_id | FK |
| armario_id | FK |
| estanteria_id | FK |
| caja_id | FK |
| posicion | VARCHAR(100) |

---

# 16. Gestión Documental

## Tabla Fotografia

### Campos

| Campo | Tipo |
|---------|---------|
| id | BIGINT |
| material_id | FK |
| fichero | VARCHAR(255) |
| descripcion | TEXT |
| fecha_subida | TIMESTAMP |

---

## Tabla Documento

### Campos

| Campo | Tipo |
|---------|---------|
| id | BIGINT |
| material_id | FK |
| nombre | VARCHAR(200) |
| fichero | VARCHAR(255) |
| tipo_documento | VARCHAR(100) |
| fecha_subida | TIMESTAMP |

---

## Tipos de documento

```text
Manual
Factura
Ficha Técnica
Certificado
Garantía
Otro
```

---

# 17. Modelo de Préstamos

## Tabla Prestamo

### Campos

| Campo | Tipo |
|---------|---------|
| id | BIGINT |
| usuario_id | FK |
| profesor_id | FK |
| fecha_prestamo | DATE |
| fecha_prevista_devolucion | DATE |
| fecha_devolucion_real | DATE |
| estado | VARCHAR(50) |
| observaciones | TEXT |

---

## Estados de préstamo

```text
Activo
Devuelto
Retrasado
Perdido
```

---

## Tabla LineaPrestamo

### Campos

| Campo | Tipo |
|---------|---------|
| id | BIGINT |
| prestamo_id | FK |
| material_id | FK |
| cantidad | INTEGER |

---

# 18. Modelo de Incidencias

## Tabla Incidencia

### Campos

| Campo | Tipo |
|---------|---------|
| id | BIGINT |
| material_id | FK |
| usuario_id | FK |
| fecha_creacion | TIMESTAMP |
| prioridad | VARCHAR(50) |
| estado | VARCHAR(50) |
| descripcion | TEXT |
| solucion | TEXT |
| fecha_cierre | TIMESTAMP |

---

## Prioridades

```text
Baja
Media
Alta
Crítica
```

---

## Estados

```text
Abierta
Asignada
En Proceso
Resuelta
Cerrada
```

---

## Tabla ComentarioIncidencia

### Campos

| Campo | Tipo |
|---------|---------|
| id | BIGINT |
| incidencia_id | FK |
| usuario_id | FK |
| comentario | TEXT |
| fecha | TIMESTAMP |

---

# 19. Modelo de Mantenimiento

## Tabla Mantenimiento

### Campos

| Campo | Tipo |
|---------|---------|
| id | BIGINT |
| material_id | FK |
| tecnico_id | FK |
| fecha | DATE |
| tipo | VARCHAR(50) |
| descripcion | TEXT |
| resultado | TEXT |
| coste | DECIMAL(10,2) |

---

## Tipos de mantenimiento

```text
Preventivo
Correctivo
Predictivo
```

---

# 20. Modelo de Auditoría

## Tabla RegistroAuditoria

### Campos

| Campo | Tipo |
|---------|---------|
| id | BIGINT |
| usuario_id | FK |
| accion | VARCHAR(100) |
| entidad | VARCHAR(100) |
| entidad_id | BIGINT |
| descripcion | TEXT |
| fecha | TIMESTAMP |

---

# 21. Índices recomendados

## Material

Crear índices sobre:

```sql
codigo_inventario
nombre
numero_serie
estado
```

---

## Prestamo

Crear índices sobre:

```sql
usuario_id
estado
fecha_prestamo
```

---

## Incidencia

Crear índices sobre:

```sql
estado
prioridad
fecha_creacion
```

---

# 22. Restricciones de integridad

## Material

- codigo_inventario debe ser único.
- numero_serie podrá ser único cuando exista.

## Categoria

- nombre único.

## Subcategoria

- combinación categoria + nombre única.

## Prestamo

- no se podrá prestar material averiado.
- no se podrá prestar material retirado.

## Incidencia

- no podrá cerrarse sin solución registrada.

---

# 23. Preparación para futuras ampliaciones

El modelo deberá permitir incorporar:

- Lectores QR.
- RFID.
- NFC.
- MQTT.
- ESP32.
- PLC Omron.
- Robots UR.
- Integración con IA.
- Aplicación móvil.

---

# Fin de la Parte 2
# Parte 3 - Casos de Uso y Reglas de Negocio

---

# 24. Reglas generales de negocio

## RN001 - Identificación única

Todo material inventariable deberá poseer un identificador único.

Campos válidos:

- Código de inventario.
- Número de serie.
- Código QR.

---

## RN002 - Integridad del inventario

No podrá existir material sin categoría asignada.

---

## RN003 - Ubicación obligatoria

Todo material deberá tener una ubicación asignada.

Excepciones:

- Material retirado.
- Material perdido.

---

## RN004 - Auditoría obligatoria

Toda acción que modifique información deberá generar automáticamente un registro de auditoría.

---

## RN005 - Trazabilidad completa

Toda entrada, salida, préstamo, devolución o traslado deberá registrarse como movimiento de inventario.

---

## RN006 - Control de stock

La cantidad disponible nunca podrá ser negativa.

---

## RN007 - Material prestable

Solo podrá prestarse material con estado:

- Disponible

No podrá prestarse material:

- Averiado
- Retirado
- Perdido
- En reparación

---

## RN008 - Baja lógica

El material nunca será eliminado físicamente de la base de datos.

Las bajas se realizarán mediante cambio de estado.

---

# 25. Gestión de movimientos de inventario

## Objetivo

Registrar cualquier modificación física del inventario.

---

## Tabla MovimientoInventario

### Campos

| Campo | Tipo |
|---------|---------|
| id | BIGINT |
| material_id | FK |
| usuario_id | FK |
| tipo_movimiento | VARCHAR |
| cantidad | INTEGER |
| ubicacion_origen_id | FK |
| ubicacion_destino_id | FK |
| observaciones | TEXT |
| fecha | TIMESTAMP |

---

## Tipos de movimiento

```text
ALTA
BAJA
PRESTAMO
DEVOLUCION
TRASLADO
AJUSTE
REPARACION
COMPRA
PERDIDA
```

---

# 26. Casos de uso del módulo Inventario

---

## CU100 - Crear material

### Actor

- Administrador
- Profesor

### Descripción

Registrar nuevo material.

### Flujo principal

1. Acceder al formulario.
2. Introducir datos.
3. Validar información.
4. Guardar material.
5. Generar auditoría.
6. Registrar movimiento ALTA.

### Resultado

Material disponible en inventario.

---

## CU101 - Modificar material

### Actor

- Administrador
- Profesor

### Flujo principal

1. Buscar material.
2. Editar datos.
3. Guardar cambios.
4. Registrar auditoría.

### Resultado

Material actualizado.

---

## CU102 - Cambiar ubicación

### Actor

- Administrador
- Profesor

### Flujo principal

1. Seleccionar material.
2. Seleccionar nueva ubicación.
3. Guardar cambio.
4. Registrar movimiento TRASLADO.

### Resultado

Material trasladado.

---

## CU103 - Dar de baja material

### Actor

- Administrador

### Flujo principal

1. Seleccionar material.
2. Confirmar baja.
3. Cambiar estado.
4. Registrar movimiento BAJA.

### Resultado

Material retirado.

---

# 27. Casos de uso del módulo Préstamos

---

## CU200 - Registrar préstamo

### Actor

- Profesor
- Administrador

### Flujo principal

1. Buscar material.
2. Seleccionar usuario.
3. Registrar fecha prevista.
4. Guardar préstamo.
5. Cambiar estado del material.
6. Registrar movimiento PRESTAMO.

### Resultado

Préstamo activo.

---

## CU201 - Registrar devolución

### Actor

- Profesor
- Administrador

### Flujo principal

1. Localizar préstamo.
2. Registrar devolución.
3. Actualizar estado del material.
4. Registrar movimiento DEVOLUCION.

### Resultado

Material disponible.

---

## CU202 - Renovar préstamo

### Actor

- Profesor

### Flujo principal

1. Seleccionar préstamo.
2. Modificar fecha prevista.
3. Guardar cambios.

### Resultado

Préstamo renovado.

---

## CU203 - Declarar pérdida

### Actor

- Administrador

### Flujo principal

1. Seleccionar préstamo.
2. Marcar material como perdido.
3. Registrar movimiento PERDIDA.
4. Crear incidencia automática.

### Resultado

Material marcado como perdido.

---

# 28. Casos de uso del módulo Incidencias

---

## CU300 - Crear incidencia

### Actor

- Profesor
- Técnico

### Flujo principal

1. Seleccionar material.
2. Describir problema.
3. Seleccionar prioridad.
4. Guardar incidencia.

### Resultado

Incidencia abierta.

---

## CU301 - Asignar incidencia

### Actor

- Administrador

### Flujo principal

1. Seleccionar incidencia.
2. Seleccionar técnico.
3. Guardar asignación.

### Resultado

Incidencia asignada.

---

## CU302 - Resolver incidencia

### Actor

- Técnico

### Flujo principal

1. Abrir incidencia.
2. Registrar solución.
3. Cambiar estado.
4. Cerrar incidencia.

### Resultado

Incidencia resuelta.

---

# 29. Casos de uso del módulo Mantenimiento

---

## CU400 - Registrar mantenimiento

### Actor

- Técnico

### Flujo principal

1. Seleccionar material.
2. Registrar trabajo realizado.
3. Guardar mantenimiento.

### Resultado

Mantenimiento registrado.

---

## CU401 - Programar revisión

### Actor

- Técnico

### Flujo principal

1. Seleccionar material.
2. Definir fecha.
3. Guardar planificación.

### Resultado

Revisión programada.

---

## CU402 - Consultar histórico

### Actor

- Técnico

### Resultado

Visualización de mantenimientos realizados.

---

# 30. Casos de uso del módulo Usuarios

---

## CU500 - Iniciar sesión

### Actor

- Usuario registrado

### Flujo principal

1. Introducir credenciales.
2. Validar acceso.
3. Mostrar dashboard.

---

## CU501 - Cerrar sesión

### Actor

- Usuario autenticado

### Resultado

Sesión cerrada.

---

## CU502 - Crear usuario

### Actor

- Administrador

### Resultado

Nuevo usuario registrado.

---

## CU503 - Modificar usuario

### Actor

- Administrador

### Resultado

Usuario actualizado.

---

# 31. Casos de uso del módulo Informes

---

## CU600 - Generar informe de inventario

### Actor

- Administrador
- Profesor

### Resultado

Informe PDF o Excel.

---

## CU601 - Generar informe de préstamos

### Actor

- Administrador

### Resultado

Listado de préstamos.

---

## CU602 - Generar informe de incidencias

### Actor

- Administrador

### Resultado

Listado de incidencias.

---

## CU603 - Generar informe económico

### Actor

- Administrador

### Resultado

Valor económico total del inventario.

---

# 32. Dashboard principal

## Información mostrada

### Inventario

- Total de materiales.
- Material disponible.
- Material prestado.
- Material averiado.

### Préstamos

- Préstamos activos.
- Préstamos vencidos.

### Incidencias

- Incidencias abiertas.
- Incidencias críticas.

### Mantenimiento

- Revisiones pendientes.
- Mantenimientos programados.

---

# 33. Alertas automáticas

El sistema deberá generar alertas cuando:

## Stock bajo

```text
cantidad <= stock_minimo
```

---

## Préstamo vencido

```text
fecha_actual > fecha_prevista_devolucion
```

---

## Garantía próxima a vencer

```text
menos de 30 días
```

---

## Mantenimiento pendiente

```text
fecha revisión superada
```

---

# 34. Reglas de permisos

## Administrador

Acceso completo.

---

## Profesor

Puede:

- Gestionar inventario.
- Gestionar préstamos.
- Crear incidencias.
- Consultar informes.

---

## Técnico

Puede:

- Gestionar incidencias.
- Gestionar mantenimiento.

---

## Alumno

Puede:

- Consultar material autorizado.
- Consultar sus préstamos.

---

# 35. Flujos de negocio principales

## Flujo de alta de material

```text
Alta material
    ↓
Asignación ubicación
    ↓
Registro auditoría
    ↓
Movimiento ALTA
    ↓
Disponible
```

---

## Flujo de préstamo

```text
Disponible
    ↓
Préstamo
    ↓
Movimiento PRESTAMO
    ↓
Prestado
    ↓
Devolución
    ↓
Movimiento DEVOLUCION
    ↓
Disponible
```

---

## Flujo de incidencia

```text
Crear incidencia
      ↓
Asignar técnico
      ↓
Reparar
      ↓
Resolver
      ↓
Cerrar
```

---

# 36. Objetivos de la Versión 1.0

La primera versión deberá permitir:

- Gestión de usuarios.
- Gestión de inventario.
- Gestión de ubicaciones.
- Gestión de préstamos.
- Auditoría.
- Informes básicos.
- Persistencia PostgreSQL.

---

# Fin de la Parte 3
# Parte 4 - Seguridad, Calidad, Pruebas y Despliegue

---

# 37. Seguridad del Sistema

## Objetivos de seguridad

La aplicación deberá garantizar:

- Confidencialidad de los datos.
- Integridad de la información.
- Disponibilidad del sistema.
- Trazabilidad de las acciones.
- Protección frente a accesos no autorizados.

---

# 38. Autenticación

## Sistema de autenticación

Se utilizará el sistema de autenticación nativo de Django.

Características:

- Login mediante usuario y contraseña.
- Contraseñas cifradas.
- Gestión de sesiones.
- Recuperación de contraseña.
- Cierre de sesión seguro.

---

## Requisitos mínimos de contraseña

La contraseña deberá cumplir:

- Longitud mínima de 8 caracteres.
- Al menos una letra mayúscula.
- Al menos una letra minúscula.
- Al menos un número.

---

# 39. Autorización

## Control de acceso basado en roles

Se utilizará RBAC (Role Based Access Control).

Roles definidos:

```text
Administrador
Profesor
Técnico
Alumno
```

---

## Matriz de permisos

| Funcionalidad | Admin | Profesor | Técnico | Alumno |
|---------------|--------|-----------|----------|---------|
| Consultar inventario | Sí | Sí | Sí | Limitado |
| Crear material | Sí | Sí | No | No |
| Editar material | Sí | Sí | No | No |
| Eliminar material | Sí | No | No | No |
| Gestionar usuarios | Sí | No | No | No |
| Registrar préstamo | Sí | Sí | No | No |
| Registrar devolución | Sí | Sí | No | No |
| Crear incidencia | Sí | Sí | Sí | No |
| Resolver incidencia | Sí | No | Sí | No |
| Registrar mantenimiento | Sí | No | Sí | No |
| Ver auditoría | Sí | No | No | No |

---

# 40. Protección frente a amenazas

## Protección CSRF

Django deberá proteger todos los formularios mediante:

```python
{% csrf_token %}
```

---

## Protección XSS

Todo contenido mostrado al usuario deberá escapar automáticamente el HTML.

No se permitirá:

- Scripts embebidos.
- Código HTML sin validar.

---

## Protección SQL Injection

Todas las consultas deberán utilizar:

- ORM de Django.
- Parámetros seguros.

Nunca se construirán consultas SQL concatenando cadenas.

---

# 41. Gestión de sesiones

## Tiempo máximo de sesión

```text
30 minutos de inactividad
```

---

## Acciones obligatorias

- Renovación automática de sesión.
- Cierre de sesión manual.
- Invalidación tras cambio de contraseña.

---

# 42. Auditoría

## Acciones auditables

La auditoría deberá registrar:

### Inventario

- Alta.
- Modificación.
- Baja.
- Cambio de ubicación.

### Usuarios

- Alta.
- Modificación.
- Desactivación.

### Préstamos

- Préstamo.
- Devolución.
- Renovación.

### Incidencias

- Creación.
- Modificación.
- Resolución.

### Mantenimiento

- Alta.
- Modificación.

---

## Datos registrados

| Campo | Descripción |
|---------|---------|
| Usuario | Usuario que realizó la acción |
| Fecha | Fecha |
| Hora | Hora |
| Acción | Acción realizada |
| Entidad | Tabla afectada |
| Registro | ID afectado |
| Descripción | Detalle del cambio |

---

# 43. Registro de logs

## Objetivo

Facilitar la detección de errores y el análisis del sistema.

---

## Tipos de logs

### Logs de aplicación

```text
Alta material
Préstamo
Incidencia
Login
Logout
```

---

### Logs de error

```text
Error base datos
Error autenticación
Error permisos
Error servidor
```

---

### Logs de seguridad

```text
Intentos de acceso fallidos
Cambios de contraseña
Accesos administrativos
```

---

# 44. Estrategia de pruebas

## Objetivos

Garantizar:

- Calidad del código.
- Estabilidad.
- Fiabilidad.
- Ausencia de errores críticos.

---

# 45. Pruebas unitarias

## Alcance

### Modelos

Validar:

- Creación.
- Actualización.
- Eliminación.
- Restricciones.

---

### Formularios

Validar:

- Campos obligatorios.
- Formatos.
- Reglas de negocio.

---

### Vistas

Validar:

- Permisos.
- Respuestas HTTP.
- Redirecciones.

---

# 46. Pruebas de integración

## Inventario

Verificar:

```text
Alta material
↓
Guardar PostgreSQL
↓
Registro auditoría
```

---

## Préstamos

Verificar:

```text
Crear préstamo
↓
Actualizar estado material
↓
Registrar movimiento
```

---

## Incidencias

Verificar:

```text
Crear incidencia
↓
Asignar técnico
↓
Resolver incidencia
```

---

# 47. Pruebas funcionales

## Casos críticos

### Inventario

- Crear material.
- Editar material.
- Eliminar material.

### Préstamos

- Registrar préstamo.
- Registrar devolución.

### Usuarios

- Login.
- Logout.
- Gestión usuarios.

---

# 48. Pruebas de rendimiento

## Objetivos

La aplicación deberá responder:

### Búsquedas

```text
< 3 segundos
```

---

### Listados

```text
< 3 segundos
```

---

### Dashboard

```text
< 5 segundos
```

---

# 49. Pruebas de seguridad

Verificar:

- Accesos no autorizados.
- Manipulación de formularios.
- Inyección SQL.
- XSS.
- CSRF.

---

# 50. Estándares de desarrollo

## Convenciones Python

Seguir PEP8.

---

## Nombres de clases

```python
class Material(models.Model):
```

---

## Nombres de funciones

```python
def crear_material():
```

---

## Nombres de variables

```python
material_disponible
```

---

# 51. Gestión del código fuente

## Repositorio Git

Nombre:

```text
inventario_taller_sdd
```

---

## Rama principal

```text
main
```

---

## Rama de desarrollo

```text
develop
```

---

## Convención de commits

### Ejemplos

```text
feat: añadir modelo material

feat: crear módulo préstamos

fix: corregir validación stock

docs: actualizar PRD

test: añadir pruebas unitarias
```

---

# 52. Gestión de dependencias

## Archivo requirements.txt

Dependencias iniciales:

```text
Django
psycopg2-binary
Pillow
openpyxl
reportlab
pytest
pytest-django
django-crispy-forms
crispy-bootstrap5
```

---

# 53. Copias de seguridad

## Base de datos

Realizar:

```text
Backup diario
```

---

## Retención

```text
30 días
```

---

## Elementos incluidos

- PostgreSQL.
- Fotografías.
- Documentos.
- Informes.

---

# 54. Configuración de entornos

## Desarrollo

Sistema:

```text
Windows 11
```

Herramientas:

```text
VS Code
Python
PostgreSQL
Git
```

---

## Producción

Sistema:

```text
Ubuntu Server LTS
```

Servicios:

```text
Gunicorn
Nginx
PostgreSQL
```

---

# 55. Variables de entorno

La configuración sensible no deberá almacenarse en el código.

Ejemplos:

```text
SECRET_KEY
DB_NAME
DB_USER
DB_PASSWORD
DB_HOST
DB_PORT
```

---

# 56. Configuración PostgreSQL

## Motor

```python
django.db.backends.postgresql
```

---

## Codificación

```text
UTF-8
```

---

## Zona horaria

```text
Europe/Madrid
```

---

# 57. Gestión de archivos

## Fotografías

Ruta:

```text
/media/fotos_material/
```

---

## Documentación

Ruta:

```text
/media/documentos/
```

---

## Informes

Ruta:

```text
/media/informes/
```

---

# 58. Escalabilidad futura

La arquitectura deberá permitir:

- Nuevos módulos Django.
- Nuevos tipos de material.
- Nuevos roles.
- Nuevas integraciones.

---

# 59. Integraciones previstas

## Industria

- PLC Omron NX102.
- Robots UR3.
- OPC UA.

---

## IoT

- MQTT.
- ESP32.
- Raspberry Pi.

---

## Identificación

- QR.
- RFID.
- NFC.

---

## Inteligencia Artificial

- Búsqueda semántica.
- Clasificación automática.
- Predicción de averías.

---

# 60. Criterios de calidad

El sistema será aceptado cuando:

- Todas las pruebas críticas superen el 100%.
- No existan errores bloqueantes.
- La auditoría funcione correctamente.
- Los permisos estén correctamente aplicados.
- PostgreSQL almacene correctamente los datos.
- Los informes se generen correctamente.

---

# Fin de la Parte 4
# Parte 5 - Roadmap, Backlog y Planificación del Proyecto

---

# 61. Estrategia de desarrollo

## Metodología

El proyecto seguirá la metodología Specification Driven Development (SDD).

### Fases

```text
1. PRD
2. SDD
3. Backlog
4. Jira
5. Desarrollo
6. Pruebas
7. Despliegue
```

---

# 62. Estrategia de versiones

## Versión 1.0

Objetivo:

Disponer de un sistema funcional para la gestión básica del inventario.

Incluye:

- Usuarios.
- Inventario.
- Ubicaciones.
- Préstamos.
- PostgreSQL.
- Auditoría básica.

---

## Versión 1.1

Incluye:

- Incidencias.
- Mantenimiento.
- Informes PDF.
- Exportación Excel.

---

## Versión 1.2

Incluye:

- Dashboard avanzado.
- Alertas automáticas.
- Estadísticas.

---

## Versión 2.0

Incluye:

- Generación automática de códigos QR.
- Lectura QR.
- Gestión documental avanzada.

---

## Versión 2.5

Incluye:

- RFID.
- NFC.
- Inventario automático.

---

## Versión 3.0

Incluye:

- MQTT.
- ESP32.
- Raspberry Pi.
- Integración IoT.

---

## Versión 4.0

Incluye:

- Integración PLC Omron.
- Integración OPC UA.
- Integración Robot UR3.

---

## Versión 5.0

Incluye:

- Inteligencia Artificial.
- Clasificación automática.
- Predicción de averías.
- Asistente inteligente.

---

# 63. Épicas del proyecto

## EP001 Usuarios

Gestión completa de usuarios y permisos.

---

## EP002 Inventario

Gestión de materiales.

---

## EP003 Ubicaciones

Gestión de ubicaciones físicas.

---

## EP004 Préstamos

Gestión de préstamos y devoluciones.

---

## EP005 Incidencias

Gestión de averías e incidencias.

---

## EP006 Mantenimiento

Gestión de mantenimientos.

---

## EP007 Informes

Generación de informes.

---

## EP008 Auditoría

Registro de acciones.

---

## EP009 Integraciones

QR, RFID, MQTT y sistemas externos.

---

# 64. Historias de Usuario

---

## HU001

### Título

Como administrador quiero crear usuarios.

### Prioridad

Alta

### Criterio de aceptación

El usuario queda registrado correctamente.

---

## HU002

### Título

Como administrador quiero editar usuarios.

### Prioridad

Alta

### Criterio de aceptación

Los cambios se guardan correctamente.

---

## HU003

### Título

Como profesor quiero consultar el inventario.

### Prioridad

Alta

### Criterio de aceptación

Puedo visualizar todos los materiales autorizados.

---

## HU004

### Título

Como profesor quiero buscar material.

### Prioridad

Alta

### Criterio de aceptación

Puedo localizar material mediante filtros.

---

## HU005

### Título

Como profesor quiero registrar nuevo material.

### Prioridad

Alta

### Criterio de aceptación

El material aparece en el inventario.

---

## HU006

### Título

Como profesor quiero modificar material.

### Prioridad

Alta

### Criterio de aceptación

Los cambios se guardan correctamente.

---

## HU007

### Título

Como administrador quiero dar de baja material.

### Prioridad

Alta

### Criterio de aceptación

El estado cambia a retirado.

---

## HU008

### Título

Como profesor quiero registrar préstamos.

### Prioridad

Alta

### Criterio de aceptación

El préstamo queda registrado.

---

## HU009

### Título

Como profesor quiero registrar devoluciones.

### Prioridad

Alta

### Criterio de aceptación

El material vuelve a estar disponible.

---

## HU010

### Título

Como técnico quiero registrar incidencias.

### Prioridad

Media

### Criterio de aceptación

La incidencia queda registrada.

---

## HU011

### Título

Como técnico quiero resolver incidencias.

### Prioridad

Media

### Criterio de aceptación

La incidencia pasa a estado resuelta.

---

## HU012

### Título

Como técnico quiero registrar mantenimientos.

### Prioridad

Media

### Criterio de aceptación

El mantenimiento queda registrado.

---

## HU013

### Título

Como administrador quiero consultar auditoría.

### Prioridad

Alta

### Criterio de aceptación

Puedo consultar acciones realizadas.

---

## HU014

### Título

Como administrador quiero generar informes.

### Prioridad

Media

### Criterio de aceptación

Se genera el informe solicitado.

---

# 65. Product Backlog Inicial

## Sprint 0

Preparación del entorno.

Tareas:

- Crear repositorio GitHub.
- Crear proyecto Jira.
- Crear entorno virtual.
- Instalar Django.
- Instalar PostgreSQL.
- Configurar VS Code.

---

## Sprint 1

Usuarios y autenticación.

Tareas:

- Crear aplicación usuarios.
- Configurar login.
- Configurar logout.
- Configurar permisos.

---

## Sprint 2

Inventario.

Tareas:

- Crear aplicación inventario.
- Crear modelo Material.
- Crear modelo Categoria.
- Crear CRUD Material.

---

## Sprint 3

Ubicaciones.

Tareas:

- Crear aplicación ubicaciones.
- Crear modelos ubicación.
- Crear CRUD ubicación.

---

## Sprint 4

Préstamos.

Tareas:

- Crear aplicación prestamos.
- Crear modelo Prestamo.
- Crear devolución.

---

## Sprint 5

Auditoría.

Tareas:

- Crear aplicación auditoria.
- Registrar acciones automáticas.

---

## Sprint 6

Incidencias.

Tareas:

- Crear aplicación incidencias.
- Crear modelo incidencia.
- Resolver incidencias.

---

## Sprint 7

Mantenimiento.

Tareas:

- Crear aplicación mantenimiento.
- Registrar mantenimientos.

---

## Sprint 8

Informes.

Tareas:

- Exportación CSV.
- Exportación Excel.
- PDF.

---

# 66. Definición de Hecho (Definition of Done)

Una tarea se considerará terminada cuando:

- El código compile.
- Las pruebas pasen.
- La funcionalidad funcione.
- Exista documentación.
- Se haya realizado commit.
- Se haya actualizado Jira.

---

# 67. Convención de ramas Git

## Rama principal

```text
main
```

---

## Rama de integración

```text
develop
```

---

## Ramas de funcionalidad

Ejemplos:

```text
feature/usuarios
feature/inventario
feature/prestamos
feature/incidencias
```

---

## Correcciones

Ejemplos:

```text
fix/login
fix/stock
fix/permisos
```

---

# 68. Convención de commits

Formato:

```text
tipo: descripción
```

Ejemplos:

```text
feat: crear modelo material
feat: implementar login
fix: corregir validación stock
docs: actualizar SDD
test: añadir pruebas inventario
```

---

# 69. Métricas del proyecto

## Calidad

- Cobertura mínima de pruebas: 80%.

---

## Rendimiento

- Consultas inferiores a 3 segundos.

---

## Seguridad

- Sin vulnerabilidades críticas.

---

## Mantenibilidad

- Código documentado.

---

# 70. Riesgos del proyecto

## Riesgo 1

Complejidad creciente del inventario.

Mitigación:

- Diseño modular.

---

## Riesgo 2

Cambios de requisitos.

Mitigación:

- Uso de SDD.

---

## Riesgo 3

Crecimiento de la base de datos.

Mitigación:

- Índices y optimización.

---

## Riesgo 4

Integraciones futuras complejas.

Mitigación:

- Arquitectura desacoplada.

---

# 71. Futuras ampliaciones específicas del taller

## Redes

- Gestión de routers Cisco.
- Gestión de switches Cisco.
- Gestión de puntos de acceso.

---

## Robótica

- Gestión del UR3.
- Gestión de herramientas del robot.

---

## Automatización

- Gestión de PLC Omron.
- Gestión de módulos NX.
- Gestión de sensores industriales.

---

## IoT

- Gestión de ESP32.
- Gestión de Raspberry Pi.
- Gestión de sensores.

---

# 72. Cierre del documento

Este documento SDD define la arquitectura, modelo de datos, reglas de negocio, seguridad, planificación y estrategia de desarrollo del proyecto Inventario Taller SDD.

Cualquier cambio significativo en los requisitos deberá reflejarse mediante una nueva versión de este documento.

---

# Fin del SDD