# BACKLOG - Inventario Taller SDD

## Información del proyecto

**Proyecto:** Inventario Taller SDD  
**Versión objetivo:** 1.0  
**Metodología:** SDD  
**Estado:** Planificación  

## Estados de las tareas

- **Hecho:** existe implementación en el proyecto.
- **Parcial:** existe una parte, pero falta completar funcionalidad o integración.
- **Pendiente:** no se aprecia implementación todavía.
- **Por revisar:** necesita validación manual o decisión de alcance.

## Cambios aceptados

- **2026-06-14:** Navegación superior simplificada y menú lateral izquierdo aceptados por ahora. La cabecera queda reservada para Dashboard, Administración, usuario autenticado y cierre de sesión. El resto de accesos se agrupan en menú lateral por módulos.

---

# EP001 - Configuración inicial del proyecto

## Objetivo

Preparar el entorno de desarrollo.

## Tareas

- BL-001 [Hecho] Crear repositorio GitHub.
- BL-002 [Hecho] Crear proyecto Jira.
- BL-003 [Hecho] Crear entorno virtual Python.
- BL-004 [Hecho] Configurar VS Code.
- BL-005 [Hecho] Instalar Django.
- BL-006 [Hecho] Instalar PostgreSQL.
- BL-007 [Hecho] Configurar conexión PostgreSQL.
- BL-008 [Hecho] Crear archivo `requirements.txt`.
- BL-009 [Hecho] Configurar Git.
- BL-010 [Hecho] Crear estructura inicial del proyecto.

---

# EP002 - Gestión de usuarios

## HU001 - Iniciar sesión

**Como** administrador  
**quiero** iniciar sesión  
**para** acceder al sistema.

### Tareas

- BL-011 [Hecho] Crear aplicación `usuarios`.
- BL-012 [Hecho] Configurar Django Authentication.
- BL-013 [Hecho] Crear página de login.
- BL-014 [Hecho] Crear página de logout.
- BL-015 [Hecho] Crear recuperación de contraseña.

---

## HU002 - Gestionar usuarios

**Como** administrador  
**quiero** gestionar usuarios  
**para** controlar quién puede acceder al sistema.

### Tareas

- BL-016 [Hecho] Crear modelo `PerfilUsuario`.
- BL-017 [Hecho] Crear modelo `Rol` resuelto mediante `Group` de Django.
- BL-018 [Hecho] Crear CRUD de usuarios.
- BL-019 [Hecho] Crear CRUD de roles.
- BL-020 [Hecho] Implementar permisos.

---

# EP003 - Gestión de inventario

## HU003 - Registrar material

**Como** profesor  
**quiero** registrar material  
**para** tener controlado el inventario del taller.

### Tareas

- BL-021 [Hecho] Crear aplicación `inventario`.
- BL-022 [Hecho] Crear modelo `Categoria`.
- BL-023 [Hecho] Crear modelo `Subcategoria`.
- BL-024 [Hecho] Crear modelo `Proveedor`.
- BL-025 [Hecho] Crear modelo `Material`.
- BL-026 [Hecho] Crear migraciones.
- BL-027 [Hecho] Aplicar migraciones.

---

## HU004 - Consultar material

**Como** profesor  
**quiero** consultar material  
**para** saber qué elementos hay en el taller.

### Tareas

- BL-028 [Hecho] Crear vista de listado de material.
- BL-029 [Hecho] Crear vista de detalle de material.
- BL-030 [Hecho] Crear paginación.
- BL-031 [Hecho] Crear filtros básicos.

---

## HU005 - Editar material

**Como** profesor  
**quiero** editar material  
**para** mantener actualizada la información.

### Tareas

- BL-032 [Hecho] Crear formulario de edición.
- BL-033 [Hecho] Validar datos.
- BL-034 [Hecho] Registrar auditoría.

---

## HU006 - Retirar material

**Como** administrador  
**quiero** retirar material  
**para** marcarlo como fuera de uso sin borrarlo físicamente.

### Tareas

- BL-035 [Hecho] Implementar baja lógica.
- BL-036 [Hecho] Registrar movimiento de baja.
- BL-037 [Hecho] Actualizar estado.

---

# EP004 - Gestión de ubicaciones

## HU007 - Asignar ubicaciones

**Como** profesor  
**quiero** asignar ubicaciones  
**para** saber dónde se encuentra cada material.

### Tareas

- BL-038 [Hecho] Crear aplicación `ubicaciones`.
- BL-039 [Hecho] Crear modelo `Edificio`.
- BL-040 [Hecho] Crear modelo `Aula`.
- BL-041 [Hecho] Crear modelo `Armario`.
- BL-042 [Hecho] Crear modelo `Estanteria`.
- BL-043 [Hecho] Crear modelo `Caja`.
- BL-044 [Hecho] Crear modelo `Ubicacion`.
- BL-045 [Hecho] Crear CRUD de ubicaciones.

---

# EP005 - Gestión documental

## HU008 - Asociar documentación al material

**Como** profesor  
**quiero** asociar documentación al material  
**para** guardar manuales, facturas y fichas técnicas.

### Tareas

- BL-046 [Hecho] Crear modelo `Documento`.
- BL-047 [Hecho] Crear subida de archivos.
- BL-048 [Hecho] Crear descarga de archivos.
- BL-049 [Hecho] Crear eliminación de documentos.

---

## HU009 - Almacenar fotografías

**Como** profesor  
**quiero** almacenar fotografías  
**para** identificar visualmente el material.

### Tareas

- BL-050 [Hecho] Crear modelo `Fotografia`.
- BL-051 [Hecho] Configurar `MEDIA_ROOT`.
- BL-052 [Hecho] Crear carga de imágenes.
- BL-053 [Hecho] Mostrar imágenes.

---

# EP006 - Gestión de préstamos

## HU010 - Prestar material

**Como** profesor  
**quiero** prestar material  
**para** controlar qué material se entrega a alumnos o compañeros.

### Tareas

- BL-054 [Hecho] Crear aplicación `prestamos`.
- BL-055 [Hecho] Crear modelo `Prestamo`.
- BL-056 [Hecho] Crear modelo `LineaPrestamo`.
- BL-057 [Hecho] Crear formulario de préstamo.
- BL-058 [Hecho] Actualizar estado del material.
- BL-059 [Hecho] Registrar movimiento de préstamo.

---

## HU011 - Registrar devoluciones

**Como** profesor  
**quiero** registrar devoluciones  
**para** actualizar el estado del material prestado.

### Tareas

- BL-060 [Hecho] Crear formulario de devolución.
- BL-061 [Hecho] Actualizar estado del material.
- BL-062 [Hecho] Registrar movimiento de devolución.

---

## HU012 - Consultar préstamos

**Como** profesor  
**quiero** consultar préstamos  
**para** ver préstamos activos e históricos.

### Tareas

- BL-063 [Hecho] Crear listado de préstamos.
- BL-064 [Hecho] Crear filtros de préstamos.
- BL-065 [Hecho] Crear histórico.

---

# EP007 - Gestión de movimientos

## HU013 - Consultar movimientos de inventario

**Como** administrador  
**quiero** conocer todos los movimientos del inventario  
**para** mantener la trazabilidad completa del material.

### Tareas

- BL-066 [Hecho] Crear modelo `MovimientoInventario`.
- BL-067 [Hecho] Registrar altas.
- BL-068 [Hecho] Registrar bajas.
- BL-069 [Hecho] Registrar préstamos.
- BL-070 [Hecho] Registrar devoluciones.
- BL-071 [Hecho] Registrar traslados.
- BL-072 [Hecho] Crear listado de movimientos.
- BL-123 [Hecho] Crear historial completo del material.

---

# EP008 - Gestión de incidencias

## HU014 - Registrar incidencias

**Como** técnico  
**quiero** registrar incidencias  
**para** documentar averías o problemas.

### Tareas

- BL-073 [Hecho] Crear aplicación `incidencias`.
- BL-074 [Hecho] Crear modelo `Incidencia`.
- BL-075 [Hecho] Crear modelo `ComentarioIncidencia`.
- BL-076 [Hecho] Crear formulario de incidencia.
- BL-077 [Hecho] Crear listado de incidencias.

---

## HU015 - Resolver incidencias

**Como** técnico  
**quiero** resolver incidencias  
**para** dejar constancia de la solución aplicada.

### Tareas

- BL-078 [Hecho] Cambiar estado de incidencia.
- BL-079 [Hecho] Registrar solución.
- BL-080 [Hecho] Cerrar incidencia.

---

# EP009 - Gestión de mantenimiento

## HU016 - Registrar mantenimientos

**Como** técnico  
**quiero** registrar mantenimientos  
**para** guardar el historial técnico del material.

### Tareas

- BL-081 [Hecho] Crear aplicación `mantenimiento`.
- BL-082 [Hecho] Crear modelo `Mantenimiento`.
- BL-083 [Hecho] Crear formulario de mantenimiento.
- BL-084 [Hecho] Crear histórico de mantenimiento.

---

## HU017 - Programar revisiones

**Como** técnico  
**quiero** programar revisiones  
**para** controlar el mantenimiento preventivo.

### Tareas

- BL-085 [Hecho] Crear modelo `PlanMantenimiento`.
- BL-086 [Hecho] Crear planificación.
- BL-087 [Pendiente] Generar alertas de revisión.

---

# EP010 - Auditoría

## HU018 - Consultar auditoría

**Como** administrador  
**quiero** conocer todas las acciones realizadas  
**para** tener trazabilidad del sistema.

### Tareas

- BL-088 [Hecho] Crear aplicación `auditoria`.
- BL-089 [Hecho] Crear modelo `RegistroAuditoria`.
- BL-090 [Hecho] Registrar acciones de inventario.
- BL-091 [Hecho] Registrar acciones de usuarios.
- BL-092 [Hecho] Registrar acciones de préstamos.
- BL-093 [Hecho] Crear listado de auditoría.

---

# EP011 - Informes

## HU019 - Exportar inventario

**Como** administrador  
**quiero** exportar inventario  
**para** obtener listados externos.

### Tareas

- BL-094 [Hecho] Crear aplicación `informes`.
- BL-095 [Pendiente] Exportar CSV.
- BL-096 [Hecho] Exportar Excel.
- BL-097 [Hecho] Exportar PDF.

---

## HU020 - Generar informes

**Como** administrador  
**quiero** generar informes  
**para** analizar el estado del taller.

### Tareas

- BL-098 [Parcial] Informe de inventario.
- BL-099 [Parcial] Informe de préstamos.
- BL-100 [Parcial] Informe de incidencias.
- BL-101 [Pendiente] Informe económico.

---

# EP012 - Dashboard

## HU021 - Visualizar resumen del sistema

**Como** usuario  
**quiero** visualizar información resumida  
**para** conocer rápidamente el estado del taller.

### Tareas

- BL-102 [Hecho] Crear dashboard principal.
- BL-103 [Hecho] Mostrar estadísticas de inventario.
- BL-104 [Hecho] Mostrar estadísticas de préstamos.
- BL-105 [Hecho] Mostrar incidencias abiertas.
- BL-106 [Pendiente] Mostrar mantenimientos pendientes.

---

# EP013 - Seguridad

## HU022 - Proteger la aplicación

**Como** administrador  
**quiero** proteger la aplicación  
**para** evitar accesos indebidos.

### Tareas

- BL-107 [Parcial] Configurar permisos.
- BL-108 [Hecho] Configurar grupos.
- BL-109 [Hecho] Configurar CSRF.
- BL-110 [Hecho] Configurar validaciones.
- BL-111 [Hecho] Configurar logs.

---

# EP014 - Pruebas

## HU023 - Validar el sistema

**Como** desarrollador  
**quiero** validar el sistema  
**para** comprobar que funciona correctamente.

### Tareas

- BL-112 [Pendiente] Crear pruebas de modelos.
- BL-113 [Pendiente] Crear pruebas de formularios.
- BL-114 [Pendiente] Crear pruebas de vistas.
- BL-115 [Pendiente] Crear pruebas de permisos.
- BL-116 [Pendiente] Crear pruebas de integración.
- BL-117 [Pendiente] Crear pruebas de rendimiento.

---

# EP015 - Documentación

## HU024 - Documentar el proyecto

**Como** desarrollador  
**quiero** documentar el proyecto  
**para** facilitar su instalación, mantenimiento y uso.

### Tareas

- BL-118 [Pendiente] Actualizar `README.md`.
- BL-119 [Pendiente] Documentar instalación.
- BL-120 [Pendiente] Documentar despliegue.
- BL-121 [Pendiente] Documentar base de datos.
- BL-122 [Pendiente] Documentar API futura.

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
| Tareas técnicas | 123 |

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
