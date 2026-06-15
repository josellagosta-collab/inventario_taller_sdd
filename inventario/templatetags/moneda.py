from decimal import Decimal, InvalidOperation

from django import template


register = template.Library()


@register.filter
def euros(valor):
    if valor in (None, ""):
        return "-"

    try:
        numero = Decimal(str(valor))
    except (InvalidOperation, TypeError, ValueError):
        return "-"

    formateado = f"{numero:,.2f}"
    formateado = formateado.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{formateado} €"
