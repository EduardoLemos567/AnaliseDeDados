from decimal import Decimal


def convert_money_to_decimal(text: str) -> Decimal:
    text = text.replace("R$ ", "").replace(",", ".")
    return Decimal(text if text else 0)


def get_domain_from_url(url: str) -> str:
    parts = url.split("/")
    return "/".join(parts[:3])
