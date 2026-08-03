from app.services.notification_cache import NotificationCache


def test_add_cache_chat():
    cache = NotificationCache()
    
    cache.add(1, channel_ids=[2])
    
    assert cache._count_connections[2] == 1
    assert cache._cache_channels[2].pop() == 1
    assert cache._cache_client[1].pop() == 2

def test_remove_cache_chat():
    cache = NotificationCache()
    
    cache.add(1, channel_ids=[2])
    cache.remove(1, channel_ids=[2])
    
    assert cache._count_connections[2] == 0
    assert not cache._cache_channels[2]
    assert not cache._cache_client[1]
    
def test_remove_all_cache_chat():
    cache = NotificationCache()
    
    cache.add(1, channel_ids=[2, 3])
    cache.remove_all(channel_ids=[2, 3])
    
    assert cache._count_connections[2] == 0
    assert not cache._cache_channels[2]
    assert not cache._cache_channels[3]
    assert not cache._cache_client[1]

def test_get_counter_cache_chat():
    cache = NotificationCache()
    
    cache.add(1, channel_ids=[2])
    
    assert cache.get_counter(channel_id=2) == 1

def test_get_channels_cache_chat():
    cache = NotificationCache()
    
    cache.add(1, channel_ids=[2])
    
    assert cache.get_channels(user_id=1)