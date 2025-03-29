import uuid
from global_state import DEBUG


def get_random_uuid():
    return str(uuid.uuid4())