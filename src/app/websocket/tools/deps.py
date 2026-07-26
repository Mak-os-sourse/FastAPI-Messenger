from dataclasses import dataclass
from typing import Coroutine, AsyncGenerator

@dataclass
class WSDependsParams:
    func: AsyncGenerator | Coroutine
    use_cache: bool

def WSDpends(func: AsyncGenerator | Coroutine, use_cache: bool = True):
    return WSDependsParams(func=func, use_cache=use_cache)