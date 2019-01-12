from typing import TypeVar, Type
from tortoise.exceptions import DoesNotExist

M = TypeVar("M")


async def get_or_404(model: Type[M], prefetch_related=None, **kwargs) -> M:
    qs = model.get(**kwargs)
    if prefetch_related is not None:
        qs = qs.prefetch_related(prefetch_related)
    try:
        return await qs
    except DoesNotExist:
        raise HTTPError(404)
