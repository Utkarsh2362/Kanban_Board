from flask_caching import Cache
from flask import current_app as app

def create_cache():

	cache_config = {
		"DEBUG": True,    
		"CACHE_TYPE": "RedisCache",
		"CACHE_REDIS_URL": "redis://localhost:6379/1" 

	}
	
	app.config.from_mapping(cache_config)
	cache = Cache(app)
	app.app_context().push()
	return cache


cache_create = create_cache()    