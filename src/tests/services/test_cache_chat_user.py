from app.services.cache_user_chat import CacheChatUser

def test_add_cache_chat():
    cache_chat_user = CacheChatUser()
    
    cache_chat_user.add(1, chat_ids=[2])
    
    assert cache_chat_user._count_connections[2] == 1
    assert cache_chat_user._cache_chat_data[2].pop() == 1
    assert cache_chat_user._cache_user_data[1].pop() == 2

def test_remove_cache_chat():
    cache_chat_user = CacheChatUser()
    
    cache_chat_user.add(1, chat_ids=[2])
    cache_chat_user.remove(1, chat_ids=[2])
    
    assert cache_chat_user._count_connections[2] == 0
    assert not cache_chat_user._cache_chat_data[2]
    assert not cache_chat_user._cache_user_data[1]
    
def test_remove_all_cache_chat():
    cache_chat_user = CacheChatUser()
    
    cache_chat_user.add(1, chat_ids=[2, 3])
    cache_chat_user.remove_all(chat_ids=[2, 3])
    
    assert cache_chat_user._count_connections[2] == 0
    assert not cache_chat_user._cache_chat_data[2]
    assert not cache_chat_user._cache_chat_data[3]
    assert not cache_chat_user._cache_user_data[1]

def test_get_counter_cache_chat():
    cache_chat_user = CacheChatUser()
    
    cache_chat_user.add(1, chat_ids=[2])
    
    assert cache_chat_user.get_counter(chat_id=2) == 1