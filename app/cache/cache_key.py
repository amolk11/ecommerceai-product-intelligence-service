PROFILE_TTL_SECONDS = 21600


def product_profile_key(
    product_id: int,
) -> str:
    return f"product:profile:{product_id}"
