from django.db import models


class Edificio(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Edificio"
        verbose_name_plural = "Edificios"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Aula(models.Model):
    edificio = models.ForeignKey(
        Edificio,
        on_delete=models.CASCADE,
        related_name="aulas"
    )
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Aula"
        verbose_name_plural = "Aulas"
        ordering = ["edificio__nombre", "nombre"]
        unique_together = ("edificio", "nombre")

    def __str__(self):
        return f"{self.edificio.nombre} - {self.nombre}"


class Armario(models.Model):
    aula = models.ForeignKey(
        Aula,
        on_delete=models.CASCADE,
        related_name="armarios"
    )
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Armario"
        verbose_name_plural = "Armarios"
        ordering = ["aula__edificio__nombre", "aula__nombre", "nombre"]
        unique_together = ("aula", "nombre")

    def __str__(self):
        return f"{self.aula} - {self.nombre}"


class Estanteria(models.Model):
    armario = models.ForeignKey(
        Armario,
        on_delete=models.CASCADE,
        related_name="estanterias"
    )
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Estantería"
        verbose_name_plural = "Estanterías"
        ordering = ["armario__aula__nombre", "armario__nombre", "nombre"]
        unique_together = ("armario", "nombre")

    def __str__(self):
        return f"{self.armario} - {self.nombre}"


class Caja(models.Model):
    estanteria = models.ForeignKey(
        Estanteria,
        on_delete=models.CASCADE,
        related_name="cajas"
    )
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Caja"
        verbose_name_plural = "Cajas"
        ordering = ["estanteria__nombre", "nombre"]
        unique_together = ("estanteria", "nombre")

    def __str__(self):
        return f"{self.estanteria} - {self.nombre}"


class Ubicacion(models.Model):
    edificio = models.ForeignKey(
        Edificio,
        on_delete=models.PROTECT,
        related_name="ubicaciones"
    )
    aula = models.ForeignKey(
        Aula,
        on_delete=models.PROTECT,
        related_name="ubicaciones",
        blank=True,
        null=True
    )
    armario = models.ForeignKey(
        Armario,
        on_delete=models.PROTECT,
        related_name="ubicaciones",
        blank=True,
        null=True
    )
    estanteria = models.ForeignKey(
        Estanteria,
        on_delete=models.PROTECT,
        related_name="ubicaciones",
        blank=True,
        null=True
    )
    caja = models.ForeignKey(
        Caja,
        on_delete=models.PROTECT,
        related_name="ubicaciones",
        blank=True,
        null=True
    )
    posicion = models.CharField(max_length=100, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Ubicación"
        verbose_name_plural = "Ubicaciones"
        ordering = [
            "edificio__nombre",
            "aula__nombre",
            "armario__nombre",
            "estanteria__nombre",
            "caja__nombre",
            "posicion",
        ]

    def __str__(self):
        partes = [self.edificio.nombre]

        if self.aula:
            partes.append(self.aula.nombre)

        if self.armario:
            partes.append(self.armario.nombre)

        if self.estanteria:
            partes.append(self.estanteria.nombre)

        if self.caja:
            partes.append(self.caja.nombre)

        if self.posicion:
            partes.append(self.posicion)

        return " / ".join(partes)