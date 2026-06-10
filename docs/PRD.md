# PRD - Sistema Web de Gestión de Inventario de Taller Hardware

## 1. Información general

**Nombre del proyecto:** Inventario Taller SDD  
**Versión:** 1.0  
**Autor:** José Aguilera  
**Tipo de aplicación:** Aplicación web  
**Metodología:** SDD  
**Backend:** Python + Django  
**Base de datos:** PostgreSQL  

---

## 2. Objetivo del proyecto

Desarrollar una aplicación web para gestionar de forma centralizada el inventario del taller de hardware.

La aplicación permitirá registrar, consultar, modificar, eliminar, prestar, devolver, mantener y auditar material técnico del taller.

---

## 3. Problema a resolver

Actualmente el material del taller puede estar repartido en aulas, armarios, cajas, estanterías o zonas de trabajo sin un control centralizado.

Esto provoca:

- Pérdida de material.
- Dificultad para localizar componentes.
- Falta de control sobre préstamos.
- Desconocimiento del estado real del inventario.
- Material duplicado.
- Material averiado sin registrar.
- Falta de trazabilidad.

---

## 4. Alcance de la aplicación

La aplicación gestionará:

- Equipos informáticos.
- Componentes de hardware.
- Material de redes.
- Herramientas.
- Electrónica.
- Robótica.
- Automatización industrial.
- Consumibles.
- Préstamos.
- Incidencias.
- Mantenimientos.
- Ubicaciones.
- Informes.

---

## 5. Tipos de usuarios

### 5.1 Administrador

Puede:

- Gestionar usuarios.
- Gestionar permisos.
- Crear, editar y eliminar material.
- Gestionar préstamos.
- Gestionar incidencias.
- Gestionar informes.
- Acceder a auditoría.

### 5.2 Profesor

Puede:

- Consultar inventario.
- Crear material.
- Editar material.
- Registrar préstamos.
- Registrar devoluciones.
- Crear incidencias.

### 5.3 Técnico

Puede:

- Consultar inventario.
- Registrar reparaciones.
- Registrar mantenimientos.
- Cambiar estados técnicos.

### 5.4 Alumno

Puede:

- Consultar material autorizado.
- Consultar sus préstamos.
- Solicitar material si el sistema lo permite.

---

## 6. Gestión de material

Cada elemento del inventario tendrá los siguientes datos:

### 6.1 Identificación

- ID interno.
- Código de inventario.
- Código QR.
- Número de serie.
- Código RFID futuro.

### 6.2 Datos generales

- Nombre.
- Descripción.
- Categoría.
- Subcategoría.
- Marca.
- Modelo.
- Estado.
- Cantidad.
- Observaciones.

### 6.3 Datos económicos

- Precio de compra.
- Fecha de compra.
- Proveedor.
- Garantía.
- Número de factura.

### 6.4 Ubicación

- Edificio.
- Planta.
- Aula.
- Armario.
- Estantería.
- Caja.
- Posición concreta.

### 6.5 Documentación asociada

- Fotografías.
- Manuales.
- Facturas.
- Fichas técnicas.
- Certificados.

---

## 7. Categorías iniciales

### 7.1 Equipos informáticos

- PC sobremesa.
- Portátil.
- Servidor.
- Mini PC.
- Thin Client.

### 7.2 Componentes

- Placa base.
- CPU.
- Memoria RAM.
- Disco SSD.
- Disco HDD.
- Tarjeta gráfica.
- Fuente de alimentación.
- Caja.
- Ventilador.

### 7.3 Redes

- Router.
- Switch.
- Firewall.
- Punto de acceso.
- Cable de red.
- Patch panel.
- Roseta.
- Latiguillo.
- Módulo SFP.

### 7.4 Electrónica e IoT

- Arduino.
- ESP32.
- ESP8266.
- Raspberry Pi.
- Sensor.
- Actuador.
- Protoboard.
- Módulo electrónico.

### 7.5 Automatización industrial

- PLC.
- HMI.
- Variador de frecuencia.
- Fuente industrial.
- Sensor inductivo.
- Sensor fotoeléctrico.
- Relé.
- Contactor.

### 7.6 Robótica

- Robot industrial.
- Cobot.
- Pinza.
- Herramienta de robot.
- Cinta transportadora.
- Encoder.

### 7.7 Herramientas

- Destornillador.
- Alicates.
- Crimpadora.
- Pelacables.
- Multímetro.
- Osciloscopio.
- Soldador.

### 7.8 Consumibles

- Tornillos.
- Resistencias.
- Cables.
- Conectores.
- Bridas.
- Filamento 3D.
- Cinta aislante.
- Estaño.

---

## 8. Estados del material

Un elemento podrá tener uno de estos estados:

- Disponible.
- Prestado.
- Reservado.
- Averiado.
- En reparación.
- Fuera de servicio.
- Retirado.
- Perdido.

---

## 9. Tipos de inventario

### 9.1 Material individual

Material que se controla unidad por unidad.

Ejemplos:

- Router Cisco.
- PLC Omron.
- Robot UR3.
- Portátil.
- Osciloscopio.

### 9.2 Material por cantidad

Material que se controla por stock.

Ejemplos:

- Cables.
- Conectores RJ45.
- Resistencias.
- Tornillos.
- Bridas.

---

## 10. Gestión de préstamos

La aplicación deberá permitir:

- Registrar préstamo.
- Registrar devolución.
- Registrar renovación.
- Registrar pérdida.
- Consultar préstamos activos.
- Consultar histórico de préstamos.

Datos del préstamo:

- Material prestado.
- Usuario receptor.
- Profesor responsable.
- Fecha de préstamo.
- Fecha prevista de devolución.
- Fecha real de devolución.
- Estado del préstamo.
- Observaciones.

---

## 11. Gestión de incidencias

La aplicación deberá permitir registrar incidencias sobre cualquier material.

Estados de incidencia:

- Abierta.
- En revisión.
- En reparación.
- Resuelta.
- Cerrada.

Datos de incidencia:

- Material afectado.
- Usuario que informa.
- Fecha.
- Descripción.
- Prioridad.
- Fotografías.
- Solución aplicada.

---

## 12. Gestión de mantenimiento

Tipos de mantenimiento:

- Preventivo.
- Correctivo.
- Predictivo.

Datos:

- Material.
- Técnico responsable.
- Fecha.
- Descripción.
- Resultado.
- Coste.
- Próxima revisión.

---

## 13. Búsquedas y filtros

La aplicación deberá permitir buscar por:

- Nombre.
- Categoría.
- Subcategoría.
- Marca.
- Modelo.
- Número de serie.
- Estado.
- Ubicación.
- Usuario responsable.
- Código QR.

También deberá permitir filtrar por:

- Material disponible.
- Material prestado.
- Material averiado.
- Material retirado.
- Material con bajo stock.
- Material sin ubicación asignada.

---

## 14. Informes

La aplicación deberá generar informes de:

- Inventario completo.
- Inventario por aula.
- Inventario por categoría.
- Inventario por estado.
- Material prestado.
- Material averiado.
- Material retirado.
- Stock bajo.
- Valor económico del inventario.
- Histórico de préstamos.
- Histórico de incidencias.

---

## 15. Exportación de datos

Formatos previstos:

- CSV.
- Excel.
- PDF.

---

## 16. Seguridad

La aplicación deberá incluir:

- Inicio de sesión.
- Cierre de sesión.
- Usuarios con roles.
- Permisos por tipo de usuario.
- Protección CSRF.
- Contraseñas cifradas.
- Control de acceso a vistas.
- Registro de acciones importantes.

---

## 17. Auditoría

El sistema registrará acciones como:

- Alta de material.
- Modificación de material.
- Eliminación de material.
- Préstamo.
- Devolución.
- Cambio de estado.
- Cambio de ubicación.
- Creación de incidencia.
- Cierre de incidencia.

Cada registro de auditoría incluirá:

- Usuario.
- Fecha.
- Hora.
- Acción.
- Elemento afectado.
- Descripción del cambio.

---

## 18. Requisitos no funcionales

### 18.1 Rendimiento

- Las búsquedas deberán responder en menos de 3 segundos.
- El sistema deberá soportar miles de registros.

### 18.2 Usabilidad

- Interfaz sencilla.
- Formularios claros.
- Menús comprensibles.
- Diseño adaptado a pantalla de PC.
- Posibilidad futura de adaptación a móvil.

### 18.3 Escalabilidad

El sistema deberá poder crecer para incluir:

- Nuevos módulos.
- Nuevas categorías.
- Más usuarios.
- Más ubicaciones.
- Integraciones externas.

### 18.4 Mantenibilidad

El código deberá estar organizado en aplicaciones Django separadas.

Posibles apps:

- inventario
- usuarios
- prestamos
- incidencias
- mantenimiento
- ubicaciones
- informes
- auditoria

---

## 19. Integraciones futuras

La aplicación podrá integrarse en el futuro con:

- Lectores QR.
- Lectores RFID.
- ESP32.
- Raspberry Pi.
- MQTT.
- PLC Omron.
- Robots UR3 / UR3e.
- APIs externas.
- Sistemas de inteligencia artificial.

---

## 20. Criterios de aceptación

La versión inicial será válida si permite:

- Crear material.
- Listar material.
- Buscar material.
- Editar material.
- Eliminar material.
- Registrar préstamos.
- Registrar devoluciones.
- Registrar incidencias.
- Gestionar ubicaciones.
- Guardar datos en PostgreSQL.
- Controlar usuarios y permisos.
- Generar informes básicos.

---

## 21. Primera versión mínima viable

La primera versión del proyecto deberá incluir:

- Proyecto Django funcionando.
- Conexión con PostgreSQL.
- Aplicación `inventario`.
- Modelo `Material`.
- Vista de listado.
- Vista de detalle.
- Formulario de alta.
- Formulario de edición.
- Eliminación de material.
- Panel de administración Django.
- README inicial.
- Repositorio GitHub.

---

## 22. Futuras mejoras

Posibles mejoras:

- Generación automática de códigos QR.
- Lectura QR desde cámara.
- Control mediante móvil.
- Importación masiva desde Excel.
- Exportación avanzada.
- Dashboard con estadísticas.
- Alertas de stock bajo.
- Historial completo de movimientos.
- Firma digital en préstamos.
- Integración con IA para búsqueda inteligente.