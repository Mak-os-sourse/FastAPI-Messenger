from collections.abc import Callable
from dataclasses import dataclass
from typing import Any


@dataclass
class WSDependsParams:
    func: Callable[..., Any]
    use_cache: bool

def WSDpends(func: Callable[..., Any], use_cache: bool = True):
    return WSDependsParams(func=func, use_cache=use_cache)