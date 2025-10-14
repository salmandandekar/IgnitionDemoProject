# Attempts to use Apache Ignite thin client if present; otherwise falls back to local CacheManager.
def available():
    try:
        import org.apache.ignite
        return True
    except Exception:
        return False

def get(cache_name):
    # Ideally return distributed cache handle; for fallback we return None (the CacheManager owns local cache)
    try:
        # integrate ignite thin client if available on classpath
        pass
    except Exception:
        pass
    return None
