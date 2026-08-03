from collections import defaultdict
from typing import Any


class NotificationCache:
    def __init__(self):
        self._cache_client: dict[int, set[int]] = defaultdict(set)
        self._cache_channels: dict[int, set[int]] = defaultdict(set)
        self._count_connections:  dict[int, int] = defaultdict(int)
    
    def get_counter(self, channel_id: int) -> int:
        return self._count_connections[channel_id]
    
    def get_channels(self, user_id: int, default: Any = None) -> set:
        return self._cache_client.get(user_id, default)
    
    def add(self, user_id: int, channel_ids: list[int]) -> None:
        user_data = self._cache_client.setdefault(user_id, set())
        
        for channel_id in channel_ids:
            self._count_connections[channel_id] += 1
            self._cache_channels[channel_id].add(user_id)
            user_data.add(channel_id)
    
    def remove(self, user_id: int, channel_ids: list[int]) -> None:
        user_data = self._cache_client.get(user_id)
        if user_data is None:
            return
        
        for channel_id in channel_ids:
            self._count_connections[channel_id] -= 1
            chat_data = self._cache_channels.get(channel_id)
            if chat_data is not None:
                chat_data.discard(user_id)
            user_data.discard(channel_id)
    
    def remove_all(self, channel_ids: list[int]) -> None:
        for channel_id in channel_ids:
            chat_data = self._cache_channels.pop(channel_id, None)
            if chat_data is None:
                continue
            for item in chat_data:
                self._count_connections[channel_id] -= 1
                user_data = self._cache_client.get(item)
                if user_data is not None:
                    user_data.discard(channel_id)