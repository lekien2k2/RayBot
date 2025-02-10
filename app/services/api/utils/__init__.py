import math


def build_meta_data(*, page: int, limit: int, total_count: int) -> dict:
    """Build metadata for pagination."""
    return {
        "page": page,
        "limit": limit,
        "total_count": total_count,
        "total_pages": math.ceil(total_count / limit),
    }
