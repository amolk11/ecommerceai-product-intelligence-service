PROFILE_TTL_SECONDS = 21600


def product_profile_key(
    product_id: int,
) -> str:
    return f"product:profile:{product_id}"


TOP_PRODUCTS_TTL_SECONDS = 3600


def top_products_key(
    metric: str,
    limit: int,
) -> str:
    return f"top_products:{metric}:{limit}"
