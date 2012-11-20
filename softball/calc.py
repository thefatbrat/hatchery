from decimal import Decimal


def average(at_bats, hits):
    """
    Avg = H / AB

    >>> average(0, 0)
    Decimal("0")
    >>> average(4, 2)
    Decimal("0.5")
    >>> average(1, 1)
    Decimal("1")
    >>> average(2, 1)
    Decimal("0.5")
    >>> average(1, 0)
    Decimal("0")
    """
    if not at_bats:
        return Decimal("0")
    if at_bats < hits:
        return Decimal("0")
    return (Decimal(hits) / Decimal(at_bats)).quantize(Decimal('.001'))

def on_base_percentage(at_bats, walks, hits):
    """
    OBP = (H + BB) / (AB + BB)

    >>> on_base_percentage(0, 0, 0)
    Decimal("0")
    >>> on_base_percentage(1, 0, 0)
    Decimal("0")
    >>> on_base_percentage(1, 0, 1)
    Decimal("1")
    >>> on_base_percentage(2, 1, 1)
    Decimal("0.6666666666666666666666666667")
    >>> on_base_percentage(4, 1, 1)
    Decimal("0.4")
    >>> on_base_percentage(4, 0, 1)
    Decimal("0.25")
    >>> on_base_percentage(4, 1, 0)
    Decimal("0.2")
    """
    if not at_bats:
        return Decimal("0")
    return (Decimal(hits + walks) / Decimal(at_bats + walks)
        ).quantize(Decimal('.001'))

def slugging_percentage(at_bats, hits, doubles, triples, home_runs):
    """
    SLG = (1B + (2B * 2) + (3B * 2) + (HR * 3)) / AB

    >>> slugging_percentage(0, 0, 0, 0, 0)
    Decimal("0")
    >>> slugging_percentage(3, 0, 0, 0, 0)
    Decimal("0")
    >>> slugging_percentage(3, 1, 1, 1, 0)
    Decimal("2")
    >>> slugging_percentage(4, 1, 1, 1, 1)
    Decimal("2.5")
    >>> slugging_percentage(1, 1, 0, 0, 0)
    Decimal("1")
    >>> slugging_percentage(1, 0, 1, 0, 0)
    Decimal("2")
    >>> slugging_percentage(1, 0, 0, 1, 0)
    Decimal("3")
    >>> slugging_percentage(1, 0, 0, 0, 1)
    Decimal("4")
    >>> slugging_percentage(8, 2, 2, 2, 2)
    Decimal("2.5")
    """
    if not at_bats:
        return Decimal("0")
    return (Decimal(hits + (2 * doubles) + (3 * triples) + (4 * home_runs)) /
            Decimal(at_bats)).quantize(Decimal('.001'))
