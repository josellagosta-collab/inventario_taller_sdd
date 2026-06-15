# API futura - Inventario Taller SDD

Documento de diseño preliminar para una futura API HTTP del sistema.

> Estado actual: la aplicación no expone una API REST pública. Todas las operaciones principales se realizan mediante vistas Django renderizadas en servidor. Este documento define una propuesta para una futura evolución.

## Objetivos

- Permitir integración con clientes externos.
- Facilitar consultas desde aplicaciones móviles.
- Preparar futuras integraciones con QR, RFID, MQTT o IA.
- Exponer datos de inventario, préstamos, incidencias, mantenimiento e informes de forma controlada.
- Mantener trazabilidad mediante auditoría.

## Principios de diseño

- API versionada desde el inicio.
- Autenticación obligatoria salvo endpoints explícitamente públicos.
- Permisos alineados con los grupos actuales.
- Respuestas JSON.
- Paginación en listados.
- Filtros similares a los formularios web.
- Auditoría en operaciones de escritura.
- No exponer rutas físicas internas de archivos.

## Versión base propuesta

Prefijo:

```txt
/api/v1/
```

Ejemplos:

```txt
/api/v1/materiales/
/api/v1/prestamos/
/api/v1/incidencias/
```

## Autenticación

Opciones recomendadas:

### Sesión Django

Útil si la API se consume desde la misma aplicación web.

Ventajas:

- Reutiliza login actual.
- Menos complejidad inicial.

Limitaciones:

- Menos cómoda para clientes externos.

### Token o JWT

Útil para clientes móviles, integraciones o servicios externos.

Ventajas:

- Mejor para integraciones.
- Permite separar clientes.

Limitaciones:

- Requiere gestión segura de tokens.
- Conviene añadir dependencia específica.

## Permisos

La API debe respetar los grupos ya definidos:

- `Administradores`
- `Profesores`
- `Técnicos`
- `Alumnos`

Matriz inicial propuesta:

| Recurso | Administradores | Profesores | Técnicos | Alumnos |
|---|---|---|---|---|
| Materiales | CRUD | Lectura, creación y edición limitada | Lectura | Lectura limitada |
| Ubicaciones | CRUD | Lectura | Lectura | Lectura limitada |
| Préstamos | CRUD | Crear, devolver, consultar | Consulta técnica si procede | Consultar propios |
| Reservas | CRUD | Crear, cancelar, convertir | Consulta | Consultar propias |
| Incidencias | CRUD | Crear y consultar | Crear, resolver, consultar | Crear o consultar propias si procede |
| Mantenimiento | CRUD | Consulta | Crear, editar, consultar | Sin acceso |
| Documentos | CRUD | Consulta y subida si procede | Consulta | Sin acceso o limitado |
| Auditoría | Consulta total | Sin acceso | Sin acceso | Sin acceso |
| Informes | Consulta total | Consulta limitada | Consulta técnica | Sin acceso |

## Formato de respuesta

Respuesta de detalle:

```json
{
  "id": 1,
  "codigo_inventario": "MAT-001",
  "nombre": "Router Cisco",
  "estado": "disponible"
}
```

Respuesta paginada:

```json
{
  "count": 125,
  "next": "/api/v1/materiales/?page=2",
  "previous": null,
  "results": []
}
```

Respuesta de error:

```json
{
  "error": {
    "code": "validation_error",
    "message": "Los datos enviados no son válidos.",
    "fields": {
      "cantidad": ["La cantidad debe ser mayor que cero."]
    }
  }
}
```

## Recursos propuestos

### Materiales

```txt
GET    /api/v1/materiales/
POST   /api/v1/materiales/
GET    /api/v1/materiales/{id}/
PATCH  /api/v1/materiales/{id}/
DELETE /api/v1/materiales/{id}/
POST   /api/v1/materiales/{id}/retirar/
POST   /api/v1/materiales/{id}/trasladar/
```

Filtros:

- `busqueda`
- `categoria`
- `estado`
- `ubicacion`
- `stock_bajo`
- `con_reserva`

Campos mínimos:

- `id`
- `codigo_inventario`
- `nombre`
- `categoria`
- `subcategoria`
- `proveedor`
- `cantidad`
- `stock_minimo`
- `estado`
- `ubicacion`
- `fecha_creacion`
- `fecha_actualizacion`

### Categorías, subcategorías y proveedores

```txt
GET /api/v1/categorias/
GET /api/v1/subcategorias/
GET /api/v1/proveedores/
```

Operaciones de escritura reservadas a administradores.

### Ubicaciones

```txt
GET    /api/v1/ubicaciones/
POST   /api/v1/ubicaciones/
GET    /api/v1/ubicaciones/{id}/
PATCH  /api/v1/ubicaciones/{id}/
DELETE /api/v1/ubicaciones/{id}/
```

Filtros:

- `busqueda`
- `edificio`
- `aula`
- `armario`
- `estanteria`
- `caja`

### Préstamos

```txt
GET   /api/v1/prestamos/
POST  /api/v1/prestamos/
GET   /api/v1/prestamos/{id}/
POST  /api/v1/prestamos/{id}/devolver/
GET   /api/v1/prestamos/historico/
```

Reglas:

- Crear préstamo debe cambiar material a `prestado`.
- Devolver préstamo debe cambiar material a `disponible`.
- Ambas operaciones deben crear `MovimientoInventario`.
- Ambas operaciones deben crear `RegistroAuditoria`.

### Reservas

```txt
GET   /api/v1/reservas/
POST  /api/v1/reservas/
GET   /api/v1/reservas/{id}/
POST  /api/v1/reservas/{id}/cancelar/
POST  /api/v1/reservas/{id}/convertir/
POST  /api/v1/reservas/actualizar-caducadas/
```

Reglas:

- Crear reserva cambia material a `reservado`.
- Cancelar reserva cambia material a `disponible`.
- Convertir reserva crea un préstamo y cambia material a `prestado`.

### Incidencias

```txt
GET   /api/v1/incidencias/
POST  /api/v1/incidencias/
GET   /api/v1/incidencias/{id}/
PATCH /api/v1/incidencias/{id}/
POST  /api/v1/incidencias/{id}/resolver/
POST  /api/v1/incidencias/{id}/comentarios/
```

Reglas:

- Crear incidencia puede cambiar material a `averiado`.
- Resolver incidencia debe registrar solución y fecha de cierre.
- Resolver incidencia puede devolver el material a `disponible`.

### Mantenimiento

```txt
GET  /api/v1/mantenimientos/
POST /api/v1/mantenimientos/
GET  /api/v1/mantenimientos/{id}/
GET  /api/v1/planes-mantenimiento/
POST /api/v1/planes-mantenimiento/
GET  /api/v1/planes-mantenimiento/{id}/
```

Filtros:

- `material`
- `tipo`
- `resultado`
- `fecha_desde`
- `fecha_hasta`
- `alerta`

### Documentos y fotografías

```txt
GET    /api/v1/documentos/
POST   /api/v1/materiales/{id}/documentos/
GET    /api/v1/documentos/{id}/descargar/
DELETE /api/v1/documentos/{id}/

GET    /api/v1/fotografias/
POST   /api/v1/materiales/{id}/fotografias/
DELETE /api/v1/fotografias/{id}/
```

Consideraciones:

- Validar tamaño máximo de archivo.
- Validar tipo MIME.
- No exponer rutas internas de `MEDIA_ROOT`.
- Registrar descargas en auditoría cuando proceda.

### Auditoría

```txt
GET /api/v1/auditoria/
GET /api/v1/auditoria/{id}/
```

Solo administradores.

Filtros:

- `usuario`
- `accion`
- `fecha_desde`
- `fecha_hasta`
- `busqueda`

### Informes

```txt
GET /api/v1/informes/inventario/
GET /api/v1/informes/prestamos/
GET /api/v1/informes/incidencias/
GET /api/v1/informes/economico/
```

La API de informes debería devolver JSON. La exportación CSV, Excel o PDF puede mantenerse en endpoints específicos:

```txt
GET /api/v1/exportaciones/inventario.csv
GET /api/v1/exportaciones/inventario.xlsx
GET /api/v1/exportaciones/inventario.pdf
```

## Auditoría en API

Operaciones que deben registrar auditoría:

- Crear, editar o retirar material.
- Trasladar material.
- Crear o devolver préstamo.
- Crear, cancelar o convertir reserva.
- Crear o resolver incidencia.
- Registrar mantenimiento.
- Subir, descargar o eliminar documentos.
- Acceder a informes sensibles.

## Validación

La API debe reutilizar reglas ya existentes en modelos y formularios:

- Código de inventario único.
- Número de serie no duplicado si se informa.
- Cantidades mayores que cero.
- Fechas no futuras cuando proceda.
- Coherencia entre categoría y subcategoría.
- Coherencia jerárquica de ubicaciones.
- Material disponible para préstamo o reserva.

## Paginación y ordenación

Listados paginados por defecto:

```txt
page=1
page_size=20
ordering=nombre
```

Límites recomendados:

- `page_size` por defecto: 20.
- `page_size` máximo: 100.

## Versionado

La primera versión debe publicarse como:

```txt
/api/v1/
```

Cambios incompatibles deben crear una nueva versión:

```txt
/api/v2/
```

## Pruebas necesarias

Cuando se implemente la API, añadir:

- Pruebas de autenticación.
- Pruebas de permisos por grupo.
- Pruebas de serialización.
- Pruebas de validación.
- Pruebas de integración de flujos completos.
- Pruebas de rendimiento en listados.
- Pruebas de subida y descarga de archivos.

## Dependencias candidatas

Opción recomendada si se decide implementar API REST:

```txt
djangorestframework
```

Opcionales según necesidad:

```txt
djangorestframework-simplejwt
django-filter
drf-spectacular
```

## Documentación OpenAPI

Si se implementa la API, se recomienda publicar documentación automática:

```txt
/api/schema/
/api/docs/
```

## Fases sugeridas

### Fase 1

- API de solo lectura para materiales, ubicaciones y categorías.
- Autenticación obligatoria.
- Paginación y filtros básicos.

### Fase 2

- Préstamos y reservas.
- Incidencias.
- Auditoría de operaciones de escritura.

### Fase 3

- Documentos y fotografías.
- Informes.
- Exportaciones.

### Fase 4

- Integraciones externas: QR, RFID, MQTT o IA.

## Riesgos

- Exponer datos sensibles sin permisos correctos.
- Duplicar reglas de negocio fuera de modelos/formularios.
- Manejar mal archivos adjuntos.
- Romper trazabilidad si las escrituras no registran auditoría.
- Generar endpoints con demasiadas consultas.

## Criterio de aceptación futuro

Una primera API se considerará aceptable cuando:

- Tenga autenticación.
- Tenga permisos por grupo.
- Cubra al menos inventario y ubicaciones.
- Tenga documentación OpenAPI.
- Tenga pruebas automatizadas.
- Registre auditoría en operaciones de escritura.
