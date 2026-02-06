from core.utils.cache_keys import job_detail_key, job_list_key
from django.core.cache import cache

JOB_LIST_TTL = 60 * 5  # 5 minutes
JOB_DETAIL_TTL = 60 * 10


def get_job_list():
    return cache.get(job_list_key())


def set_job_list(data):
    cache.set(job_list_key(), data, JOB_LIST_TTL)


def get_job_detail(job_id):
    return cache.get(job_detail_key(job_id))


def set_job_detail(job_id, data):
    cache.set(job_detail_key(job_id), data, JOB_DETAIL_TTL)


def invalidate_job_cache(job_id=None):
    cache.delete(job_list_key())
    if job_id:
        cache.delete(job_detail_key(job_id))
