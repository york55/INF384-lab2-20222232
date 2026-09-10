"""Calculo de tarifas de despacho."""

from __future__ import annotations

from dataclasses import dataclass

TARIFA_BASE = 12.50
COSTO_POR_KILO = 1.80
RECARGO_ZONA_ALEJADA = 0.35
UMBRAL_ENVIO_GRATIS = 250.00

ZONAS_ALEJADAS = {"selva", "sierra_alta", "frontera"}


class ZonaDesconocida(Exception):
    """La zona indicada no esta en el tarifario."""


ZONAS = {
    "lima_metropolitana": 1.00,
    "costa_norte": 1.20,
    "costa_sur": 1.20,
    "sierra": 1.45,
    "sierra_alta": 1.65,
    "selva": 1.80,
    "frontera": 2.10,
}


@dataclass
class Envio:
    zona: str
    peso_kg: float
    valor_declarado: float
    urgente: bool = False


def factor_zona(zona: str) -> float:
    if zona not in ZONAS:
        raise ZonaDesconocida(f"zona no reconocida: {zona}")
    return ZONAS[zona]


def costo_peso(peso_kg: float) -> float:
    if peso_kg <= 0:
        return 0.0
    return round(peso_kg * COSTO_POR_KILO, 2)


def aplica_envio_gratis(envio: Envio) -> bool:
    if envio.urgente:
        return False
    if envio.zona in ZONAS_ALEJADAS:
        return False
    return envio.valor_declarado >= UMBRAL_ENVIO_GRATIS


def calcular(envio: Envio) -> float:
    if aplica_envio_gratis(envio):
        return 0.0

    total = TARIFA_BASE + costo_peso(envio.peso_kg)
    total = total * factor_zona(envio.zona)

    if envio.zona in ZONAS_ALEJADAS:
        total = total * (1 + RECARGO_ZONA_ALEJADA)

    if envio.urgente:
        total = total * 1.5

    return round(total, 2)


def desglose(envio: Envio) -> dict[str, float]:
    base = TARIFA_BASE
    peso = costo_peso(envio.peso_kg)
    factor = factor_zona(envio.zona)
    return {
        "base": base,
        "peso": peso,
        "factor_zona": factor,
        "total": calcular(envio),
    }

def recargo_temporada_alta(mes: int, envio: Envio) -> float:
    """Calcula un recargo adicional durante los meses de alta demanda.

    Diciembre y julio son los meses de mayor volumen por fiestas y
    vacaciones. El recargo final depende de la zona, la urgencia y el
    valor declarado del envio.
    """
    if mes not in (7, 12):
        return 0.0

    if mes == 12:
        base = 0.10
    else:
        base = 0.05

    if envio.zona in ZONAS_ALEJADAS:
        base += 0.08
    elif envio.zona == "lima_metropolitana":
        base += 0.02
    elif envio.zona in ("costa_norte", "costa_sur"):
        base += 0.04
    else:
        base += 0.05

    if envio.urgente and envio.valor_declarado > 500:
        base += 0.20
    elif envio.urgente:
        base += 0.15
    elif envio.valor_declarado > 500:
        base += 0.03

    if base > 0.35:
        base = 0.35

    recargo = calcular(envio) * base
    return round(recargo, 2)
