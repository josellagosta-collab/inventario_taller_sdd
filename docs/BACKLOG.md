# BACKLOG - Inventario Taller SDD

## Información del proyecto

**Proyecto:** Inventario Taller SDD  
**Versión objetivo:** 1.0  
**Metodología:** SDD  
**Estado:** Planificación  

---

# EP001 - Configuración inicial del proyecto

## Objetivo

Preparar el entorno de desarrollo.

## Tareas

- BL-001 Crear repositorio GitHub.
- BL-002 Crear proyecto Jira.
- BL-003 Crear entorno virtual Python.
- BL-004 Configurar VS Code.
- BL-005 Instalar Django.
- BL-006 Instalar PostgreSQL.
- BL-007 Configurar conexión PostgreSQL.
- BL-008 Crear archivo `requirements.txt`.
- BL-009 Configurar Git.
- BL-010 Crear estructura inicial del proyecto.

---

# EP002 - Gestión de usuarios

## HU001 - Iniciar sesión

**Como** administrador  
**quiero** iniciar sesión  
**para** acceder al sistema.

### Tareas

- BL-011 Crear aplicación `usuarios`.
- BL-012 Configurar Django Authentication.
- BL-013 Crear página de login.
- BL-014 Crear página de logout.
- BL-015 Crear recuperación de contraseña.

---

## HU002 - Gestionar usuarios

**Como** administrador  
**quiero** gestionar usuarios  
**para** controlar quién puede acceder al sistema.

### Tareas

- BL-016 Crear modelo `PerfilUsuario`.
- BL-017 Crear modelo `Rol`.
- BL-018 Crear CRUD de usuarios.
- BL-019 Crear CRUD de roles.
- BL-020 Implementar permisos.

---

# EP003 - Gestión de inventario

## HU003 - Registrar material

**Como** profesor  
**quiero** registrar material  
**para** tener controlado el inventario del taller.

### Tareas

- BL-021 Crear aplicación `inventario`.
- BL-022 Crear modelo `Categoria`.
- BL-023 Crear modelo `Subcategoria`.
- BL-024 Crear modelo `Proveedor`.
- BL-025 Crear modelo `Material`.
- BL-026 Crear migraciones.
- BL-027 Aplicar migraciones.

---

## HU004 - Consultar material

**Como** profesor  
**quiero** consultar material  
**para** saber qué elementos hay en el taller.

### Tareas

- BL-028 Crear vista de listado de material.
- BL-029 Crear vista de detalle de material.
- BL-030 Crear paginación.
- BL-031 Crear filtros básicos.

---

## HU005 - Editar material

**Como** profesor  
**quiero** editar material  
**para** mantener actualizada la información.

### Tareas

- BL-032 Crear formulario de edición.
- BL-033 Validar datos.
- BL-034 Registrar auditoría.

---

## HU006 - Retirar material

**Como** administrador  
**quiero** retirar material  
**para** marcarlo como fuera de uso sin borrarlo físicamente.

### Tareas

- BL-035 Implementar baja lógica.
- BL-036 Registrar movimiento de baja.
- BL-037 Actualizar estado.

---

# EP004 - Gestión de ubicaciones

## HU007 - Asignar ubicaciones

**Como** profesor  
**quiero** asignar ubicaciones  
**para** saber dónde se encuentra cada material.

### Tareas

- BL-038 Crear aplicación `ubicaciones`.
- BL-039 Crear modelo `Edificio`.
- BL-040 Crear modelo `Aula`.
- BL-041 Crear modelo `Armario`.
- BL-042 Crear modelo `Estanteria`.
- BL-043 Crear modelo `Caja`.
- BL-044 Crear modelo `Ubicacion`.
- BL-045 Crear CRUD de ubicaciones.

---

# EP005 - Gestión documental

## HU008 - Asociar documentación al material

**Como** profesor  
**quiero** asociar documentación al material  
**para** guardar manuales, facturas y fichas técnicas.

### Tareas

- BL-046 Crear modelo `Documento`.
- BL-047 Crear subida de archivos.
- BL-048 Crear descarga de archivos.
- BL-049 Crear eliminación de documentos.

---

## HU009 - Almacenar fotografías

**Como** profesor  
**quiero** almacenar fotografías  
**para** identificar visualmente el material.

### Tareas

- BL-050 Crear modelo `Fotografia`.
- BL-051 Configurar `MEDIA_ROOT`.
- BL-052 Crear carga de imágenes.
- BL-053 Mostrar imágenes.

---

# EP006 - Gestión de préstamos

## HU010 - Prestar material

**Como** profesor  
**quiero** prestar material  
**para** controlar qué material se entrega a alumnos o compañeros.

### Tareas

- BL-054 Crear aplicación `prestamos`.
- BL-055 Crear modelo `Prestamo`.
- BL-056 Crear modelo `LineaPrestamo`.
- BL-057 Crear formulario de préstamo.
- BL-058 Actualizar estado del material.
- BL-059 Registrar movimiento de préstamo.

---

## HU011 - Registrar devoluciones

**Como** profesor  
**quiero** registrar devoluciones  
**para** actualizar el estado del material prestado.

### Tareas

- BL-060 Crear formulario de devolución.
- BL-061 Actualizar estado del material.
- BL-062 Registrar movimiento de devolución.

---

## HU012 - Consultar préstamos

**Como** profesor  
**quiero** consultar préstamos  
**para** ver préstamos activos e históricos.

### Tareas

- BL-063 Crear listado de préstamos.
- BL-064 Crear filtros de préstamos.
- BL-065 Crear histórico.

---

# EP007 - Gestión de movimientos

## HU013 - Consultar movimientos de inventario

**Como** administrador  
**quiero** conocer todos los movimientos del inventario  
**para** mantener la trazabilidad completa del material.

### Tareas

- BL-066 Crear modelo `MovimientoInventario`.
- BL-067 Registrar altas.
- BL-068 Registrar bajas.
- BL-069 Registrar préstamos.
- BL-070 Registrar devoluciones.
- BL-071 Registrar traslados.
- BL-072 Crear listado de movimientos.

---

# EP008 - Gestión de incidencias

## HU014 - Registrar incidencias

**Como** técnico  
**quiero** registrar incidencias  
**para** documentar averías o problemas.

### Tareas

- BL-073 Crear aplicación `incidencias`.
- BL-074 Crear modelo `Incidencia`.
- BL-075 Crear modelo `ComentarioIncidencia`.
- BL-076 Crear formulario de incidencia.
- BL-077 Crear listado de incidencias.

---

## HU015 - Resolver incidencias

**Como** técnico  
**quiero** resolver incidencias  
**para** dejar constancia de la solución aplicada.

### Tareas

- BL-078 Cambiar estado de incidencia.
- BL-079 Registrar solución.
- BL-080 Cerrar incidencia.

---

# EP009 - Gestión de mantenimiento

## HU016 - Registrar mantenimientos

**Como** técnico  
**quiero** registrar mantenimientos  
**para** guardar el historial técnico del material.

### Tareas

- BL-081 Crear aplicación `mantenimiento`.
- BL-082 Crear modelo `Mantenimiento`.
- BL-083 Crear formulario de mantenimiento.
- BL-084 Crear histórico de mantenimiento.

---

## HU017 - Programar revisiones

**Como** técnico  
**quiero** programar revisiones  
**para** controlar el mantenimiento preventivo.

### Tareas

- BL-085 Crear modelo `PlanMantenimiento`.
- BL-086 Crear planificación.
- BL-087 Generar alertas de revisión.

---

# EP010 - Auditoría

## HU018 - Consultar auditoría

**Como** administrador  
**quiero** conocer todas las acciones realizadas  
**para** tener trazabilidad del sistema.

### Tareas

- BL-088 Crear aplicación `auditoria`.
- BL-089 Crear modelo `RegistroAuditoria`.
- BL-090 Registrar acciones de inventario.
- BL-091 Registrar acciones de usuarios.
- BL-092 Registrar acciones de préstamos.
- BL-093 Crear listado de auditoría.

---

# EP011 - Informes

## HU019 - Exportar inventario

**Como** administrador  
**quiero** exportar inventario  
**para** obtener listados externos.

### Tareas

- BL-094 Crear aplicación `informes`.
- BL-095 Exportar CSV.
- BL-096 Exportar Excel.
- BL-097 Exportar PDF.

---

## HU020 - Generar informes

**Como** administrador  
**quiero** generar informes  
**para** analizar el estado del taller.

### Tareas

- BL-098 Informe de inventario.
- BL-099 Informe de préstamos.
- BL-100 Informe de incidencias.
- BL-101 Informe económico.

---

# EP012 - Dashboard

## HU021 - Visualizar resumen del sistema

**Como** usuario  
**quiero** visualizar información resumida  
**para** conocer rápidamente el estado del taller.

### Tareas

- BL-102 Crear dashboard principal.
- BL-103 Mostrar estadísticas de inventario.
- BL-104 Mostrar estadísticas de préstamos.
- BL-105 Mostrar incidencias abiertas.
- BL-106 Mostrar mantenimientos pendientes.

---

# EP013 - Seguridad

## HU022 - Proteger la aplicación

**Como** administrador  
**quiero** proteger la aplicación  
**para** evitar accesos indebidos.

### Tareas

- BL-107 Configurar permisos.
- BL-108 Configurar grupos.
- BL-109 Configurar CSRF.
- BL-110 Configurar validaciones.
- BL-111 Configurar logs.

---

# EP014 - Pruebas

## HU023 - Validar el sistema

**Como** desarrollador  
**quiero** validar el sistema  
**para** comprobar que funciona correctamente.

### Tareas

- BL-112 Crear pruebas de modelos.
- BL-113 Crear pruebas de formularios.
- BL-114 Crear pruebas de vistas.
- BL-115 Crear pruebas de permisos.
- BL-116 Crear pruebas de integración.
- BL-117 Crear pruebas de rendimiento.

---

# EP015 - Documentación

## HU024 - Documentar el proyecto

**Como** desarrollador  
**quiero** documentar el proyecto  
**para** facilitar su instalación, mantenimiento y uso.

### Tareas

- BL-118 Actualizar `README.md`.
- BL-119 Documentar instalación.
- BL-120 Documentar despliegue.
- BL-121 Documentar base de datos.
- BL-122 Documentar API futura.

---

# MVP - Versión mínima viable

Para considerar finalizada la versión 1.0 deberán estar completadas:

- EP001 - Configuración inicial del proyecto.
- EP002 - Gestión de usuarios.
- EP003 - Gestión de inventario.
- EP004 - Gestión de ubicaciones.
- EP006 - Gestión de préstamos.
- EP007 - Gestión de movimientos.
- EP010 - Auditoría.

---

# Resumen del backlog

| Elemento | Cantidad |
|---|---:|
| Épicas | 15 |
| Historias de usuario | 24 |
| Tareas técnicas | 122 |

---

# Prioridades

## Prioridad alta

- Usuarios.
- Inventario.
- Ubicaciones.
- Préstamos.
- Movimientos.
- Auditoría.

## Prioridad media

- Incidencias.
- Mantenimiento.
- Informes.
- Dashboard.

## Prioridad baja

- Integraciones futuras.
- QR.
- RFID.
- MQTT.
- IA.

---

# Próximo paso recomendado

Crear en Jira las siguientes épicas iniciales:

- EP001 - Configuración inicial del proyecto.
- EP002 - Gestión de usuarios.
- EP003 - Gestión de inventario.
- EP004 - Gestión de ubicaciones.
- EP006 - Gestión de préstamos.
- EP007 - Gestión de movimientos.
- EP010 - Auditoría.

Después se irán creando las historias de usuario y tareas técnicas asociadas.

---

# Fin del Backlog