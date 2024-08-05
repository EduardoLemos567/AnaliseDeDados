from decimal import Decimal


def convert_BR_money_to_decimal(text: str) -> Decimal:
    text = text.replace("R$ ", "").replace(",", ".")
    return Decimal(text if text else 0)

def convert_text_seconds_to_float(text: str) -> float:
    text = text.replace("s", "")
    return float(text if text else 0)


def get_domain_from_url(url: str) -> str:
    parts = url.split("/")
    return "/".join(parts[:3])
