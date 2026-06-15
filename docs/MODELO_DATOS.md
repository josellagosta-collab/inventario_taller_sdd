# Modelo de datos - Inventario Taller SDD

Documento de referencia del modelo de datos actual de la aplicación.

## Base de datos

El proyecto usa PostgreSQL mediante Django ORM.

Configuración local actual:

```txt
ENGINE: django.db.backends.postgresql
NAME: inventario_taller
USER: inventario_user
HOST: localhost
PORT: 5432
```

## Aplicaciones con modelos

- `usuarios`
- `inventario`
- `ubicaciones`
- `prestamos`
- `incidencias`
- `mantenimiento`
- `documentos`
- `auditoria`

`informes` no define modelos propios actualmente; consume datos del resto de aplicaciones.

## Usuarios y permisos

### User

Modelo estándar de Django: `django.contrib.auth.models.User`.

Se usa para:

- Autenticación.
- Asignación a grupos.
- Responsables de préstamos.
- Técnicos de mantenimiento.
- Usuarios de auditoría.

### Group

Modelo estándar de Django para roles.

Grupos base:

- `Administradores`
- `Profesores`
- `Técnicos`
- `Alumnos`

Se inicializan con:

```powershell
python manage.py inicializar_grupos
```

### PerfilUsuario

Extiende a `User` mediante relación uno a uno.

Campos principales:

- `user`: OneToOne con `User`.
- `tipo_usuario`: administrador, profesor, tecnico, alumno.
- `departamento`.
- `telefono`.
- `puede_recibir_prestamos`.
- `observaciones`.
- `creado_en`.
- `actualizado_en`.

Relación:

```txt
User 1 -- 1 PerfilUsuario
```

## Inventario

### Categoria

Agrupa materiales por categoría.

Campos:

- `nombre`: único.
- `descripcion`.

Relaciones:

```txt
Categoria 1 -- N Subcategoria
Categoria 1 -- N Material
```

### Subcategoria

Subgrupo dentro de una categoría.

Campos:

- `categoria`: FK a `Categoria`, `CASCADE`.
- `nombre`.
- `descripcion`.

Restricción:

```txt
unique_together = (categoria, nombre)
```

### Proveedor

Proveedor del material.

Campos:

- `nombre`: único.
- `telefono`.
- `email`.
- `web`.
- `observaciones`.

Relación:

```txt
Proveedor 1 -- N Material
```

Si se elimina un proveedor, los materiales conservan el registro y quedan con proveedor nulo.

### Material

Entidad central del sistema.

Campos principales:

- `codigo_inventario`: único.
- `nombre`.
- `descripcion`.
- `categoria`: FK protegida.
- `subcategoria`: FK protegida, opcional.
- `proveedor`: FK opcional con `SET_NULL`.
- `marca`.
- `modelo`.
- `numero_serie`.
- `cantidad`.
- `stock_minimo`.
- `precio_compra`.
- `fecha_compra`.
- `garantia_hasta`.
- `estado`.
- `ubicacion`: FK opcional con `SET_NULL`.
- `observaciones`.
- `fecha_creacion`.
- `fecha_actualizacion`.

Estados:

- `disponible`
- `prestado`
- `reservado`
- `averiado`
- `en_reparacion`
- `fuera_servicio`
- `retirado`
- `perdido`

Reglas de validación:

- El precio no puede ser negativo.
- La fecha de compra no puede ser futura.
- La garantía no puede ser anterior a la compra.
- La subcategoría debe pertenecer a la categoría seleccionada.
- Un material disponible, reservado o prestado debe tener cantidad mayor que cero.

### MovimientoInventario

Registra trazabilidad de cambios sobre materiales.

Campos:

- `material`: FK a `Material`, `CASCADE`.
- `tipo`.
- `usuario`: FK opcional a `User`, `SET_NULL`.
- `descripcion`.
- `fecha`.

Tipos:

- `alta`
- `edicion`
- `retirada`
- `prestamo`
- `devolucion`
- `traslado`
- `ajuste`

Relación:

```txt
Material 1 -- N MovimientoInventario
```

## Ubicaciones

La ubicación se modela de forma jerárquica.

```txt
Edificio -> Aula -> Armario -> Estanteria -> Caja -> Ubicacion
```

### Edificio

Campos:

- `nombre`: único.
- `descripcion`.

### Aula

Campos:

- `edificio`: FK a `Edificio`, `CASCADE`.
- `nombre`.
- `descripcion`.

Restricción:

```txt
unique_together = (edificio, nombre)
```

### Armario

Campos:

- `aula`: FK a `Aula`, `CASCADE`.
- `nombre`.
- `descripcion`.

Restricción:

```txt
unique_together = (aula, nombre)
```

### Estanteria

Campos:

- `armario`: FK a `Armario`, `CASCADE`.
- `nombre`.
- `descripcion`.

Restricción:

```txt
unique_together = (armario, nombre)
```

### Caja

Campos:

- `estanteria`: FK a `Estanteria`, `CASCADE`.
- `nombre`.
- `descripcion`.

Restricción:

```txt
unique_together = (estanteria, nombre)
```

### Ubicacion

Campos:

- `edificio`: FK protegida.
- `aula`: FK protegida, opcional.
- `armario`: FK protegida, opcional.
- `estanteria`: FK protegida, opcional.
- `caja`: FK protegida, opcional.
- `posicion`.
- `descripcion`.

Uso:

- Un `Material` puede apuntar a una `Ubicacion`.
- Si una ubicación está asociada a materiales, no debe eliminarse sin gestionar antes esos materiales.

## Préstamos y reservas

### Prestamo

Representa la entrega de material a un usuario.

Campos:

- `usuario_receptor`: FK protegida a `User`.
- `profesor_responsable`: FK protegida a `User`.
- `fecha_prestamo`.
- `fecha_prevista_devolucion`.
- `fecha_devolucion_real`.
- `estado`.
- `observaciones`.

Estados:

- `activo`
- `devuelto`
- `retrasado`
- `perdido`

Método relevante:

- `esta_retrasado()`.

### LineaPrestamo

Material incluido en un préstamo.

Campos:

- `prestamo`: FK a `Prestamo`, `CASCADE`.
- `material`: FK protegida a `Material`.
- `cantidad`.

Relación:

```txt
Prestamo 1 -- N LineaPrestamo
Material 1 -- N LineaPrestamo
```

### Reserva

Solicitud o bloqueo previo de material.

Campos:

- `usuario_reserva`: FK protegida a `User`.
- `profesor_responsable`: FK protegida a `User`.
- `material`: FK protegida a `Material`.
- `cantidad`.
- `fecha_reserva`.
- `fecha_prevista_recogida`.
- `estado`.
- `observaciones`.

Estados:

- `activa`
- `convertida`
- `cancelada`
- `caducada`

Método relevante:

- `esta_caducada()`.

## Incidencias

### Incidencia

Registra averías o problemas asociados a un material.

Campos:

- `material`: FK protegida a `Material`.
- `usuario`: FK opcional a `User`, `SET_NULL`.
- `titulo`.
- `descripcion`.
- `prioridad`.
- `estado`.
- `solucion`.
- `fecha_creacion`.
- `fecha_actualizacion`.
- `fecha_cierre`.

Prioridades:

- `baja`
- `media`
- `alta`
- `critica`

Estados:

- `abierta`
- `en_revision`
- `en_reparacion`
- `resuelta`
- `cerrada`

### ComentarioIncidencia

Comentario asociado a una incidencia.

Campos:

- `incidencia`: FK a `Incidencia`, `CASCADE`.
- `usuario`: FK opcional a `User`, `SET_NULL`.
- `comentario`.
- `fecha`.

## Mantenimiento

### Mantenimiento

Histórico de actuaciones técnicas sobre materiales.

Campos:

- `material`: FK protegida a `Material`.
- `tecnico`: FK opcional a `User`, `SET_NULL`.
- `tipo`.
- `fecha`.
- `descripcion`.
- `resultado`.
- `coste`.
- `proxima_revision`.
- `observaciones`.
- `creado_en`.
- `actualizado_en`.

Tipos:

- `preventivo`
- `correctivo`
- `predictivo`

Resultados:

- `ok`
- `reparado`
- `pendiente`
- `no_reparable`

Validaciones:

- El coste no puede ser negativo.
- La fecha no puede ser futura.
- La próxima revisión no puede ser anterior al mantenimiento.

### PlanMantenimiento

Planificación preventiva de revisiones.

Campos:

- `material`: FK protegida a `Material`.
- `responsable`: FK opcional a `User`, `SET_NULL`.
- `nombre`.
- `tipo`.
- `descripcion`.
- `frecuencia_dias`.
- `fecha_inicio`.
- `proxima_revision`.
- `activo`.
- `observaciones`.
- `creado_en`.
- `actualizado_en`.

Propiedades:

- `dias_hasta_revision`.
- `dias_revision_absolutos`.
- `estado_revision`.
- `estado_revision_display`.

Estados calculados:

- `inactivo`
- `vencido`
- `proximo`
- `al_dia`

## Documentos y fotografías

### Documento

Archivo asociado a un material.

Campos:

- `material`: FK a `Material`, `CASCADE`.
- `nombre`.
- `descripcion`.
- `archivo`.
- `tipo_documento`.
- `usuario`: FK opcional a `User`, `SET_NULL`.
- `fecha_subida`.

Tipos:

- `manual`
- `factura`
- `garantia`
- `esquema`
- `fotografia`
- `proyecto`
- `configuracion`
- `otro`

### Fotografia

Imagen asociada a un material.

Campos:

- `material`: FK a `Material`, `CASCADE`.
- `titulo`.
- `imagen`.
- `descripcion`.
- `usuario`: FK opcional a `User`, `SET_NULL`.
- `fecha_subida`.

## Auditoría

### RegistroAuditoria

Registro central de acciones importantes.

Campos:

- `usuario`: FK opcional a `User`, `SET_NULL`.
- `accion`.
- `descripcion`.
- `content_type`: FK opcional a `ContentType`, `SET_NULL`.
- `object_id`.
- `objeto_repr`.
- `ip`.
- `user_agent`.
- `fecha`.

Acciones:

- `crear`
- `editar`
- `eliminar`
- `retirar`
- `prestar`
- `devolver`
- `reservar`
- `cancelar_reserva`
- `convertir_reserva`
- `exportar`
- `acceder`
- `iniciar_sesion`
- `cerrar_sesion`
- `login_fallido`
- `otro`

## Relaciones principales

```txt
User 1 -- 1 PerfilUsuario
User 1 -- N Prestamo.usuario_receptor
User 1 -- N Prestamo.profesor_responsable
User 1 -- N Reserva.usuario_reserva
User 1 -- N Reserva.profesor_responsable
User 1 -- N RegistroAuditoria

Categoria 1 -- N Subcategoria
Categoria 1 -- N Material
Subcategoria 1 -- N Material
Proveedor 1 -- N Material
Ubicacion 1 -- N Material

Material 1 -- N MovimientoInventario
Material 1 -- N LineaPrestamo
Material 1 -- N Reserva
Material 1 -- N Incidencia
Material 1 -- N Mantenimiento
Material 1 -- N PlanMantenimiento
Material 1 -- N Documento
Material 1 -- N Fotografia

Prestamo 1 -- N LineaPrestamo
Incidencia 1 -- N ComentarioIncidencia
```

## Consideraciones operativas

- `Material` es la entidad central; muchas operaciones deben crear `MovimientoInventario`.
- Las acciones relevantes deben registrarse en `RegistroAuditoria`.
- Los ficheros físicos de `Documento` y `Fotografia` se almacenan en `MEDIA_ROOT`.
- La base de datos no contiene el contenido binario de documentos o fotografías, solo la ruta del archivo.
- Las entidades protegidas con `PROTECT` requieren revisar dependencias antes de borrar registros.

## Copias de seguridad

Una copia completa debe incluir:

- Dump de PostgreSQL.
- Carpeta `media/`.
- Configuración de entorno.

Ejemplo orientativo de backup PostgreSQL:

```powershell
pg_dump -U inventario_user -h localhost -p 5432 inventario_taller > backup_inventario_taller.sql
```
