from collections import defaultdict

class CacheChatUser:
    def __init__(self):
        self._cache_user_data: dict[int, set[int]] = defaultdict(set)
        self._cache_chat_data: dict[int, set[int]] = defaultdict(set)
        self._count_connections:  dict[int, int] = defaultdict(int)
    
    def get_counter(self, chat_id: int) -> int:
        return self._count_connections[chat_id]
    
    def add(self, user_id: int, chat_ids: list[int]) -> None:
        user_data = self._cache_user_data.setdefault(user_id, set())
        
        for chat_id in chat_ids:
            self._count_connections[chat_id] += 1
            self._cache_chat_data[chat_id].add(user_id)
            user_data.add(chat_id)
    
    def remove(self, user_id: int, chat_ids: list[int]) -> None:
        user_data = self._cache_user_data.get(user_id)
        if user_id is None:
            return
        
        for chat_id in chat_ids:
            self._count_connections[chat_id] -= 1
            chat_data = self._cache_chat_data.get(chat_id)
            if chat_data is not None:
                chat_data.discard(user_id)
            user_data.discard(chat_id)
    
    def remove_all(self, chat_ids: list[int]) -> None:
        for chat_id in chat_ids:
            chat_data = self._cache_chat_data.pop(chat_id, None)
            if chat_data is None:
                continue
            for item in chat_data:
                self._count_connections[chat_id] -= 1
                user_data = self._cache_user_data.get(item)
                if user_data is not None:
                    user_data.discard(chat_id)
                    
cache_chat_user = CacheChatUser()