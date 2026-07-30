from collections.abc import AsyncGenerator, Coroutine
from dataclasses import dataclass


@dataclass
class WSDependsParams:
    func: AsyncGenerator | Coroutine
    use_cache: bool

def WSDpends(func: AsyncGenerator | Coroutine, use_cache: bool = True):
    return WSDependsParams(func=func, use_cache=use_cache)