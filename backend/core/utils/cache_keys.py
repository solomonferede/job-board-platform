def job_list_key():
    return "jobs:list"


def job_detail_key(job_id: int):
    return f"jobs:detail:{job_id}"
