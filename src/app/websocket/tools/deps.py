from dataclasses import dataclass
from typing import Coroutine, AsyncGenerator

@dataclass
class WSDependsParams:
    func: AsyncGenerator | Coroutine

def WSDpends(func: AsyncGenerator | Coroutine):
    return WSDependsParams(func)