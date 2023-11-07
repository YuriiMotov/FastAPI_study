from .tasks import router as router_tasks
from .users import router as router_users


all_routers = [
    router_tasks,
    router_users,
]