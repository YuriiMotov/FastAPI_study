from fastapi import APIRouter, BackgroundTasks, Depends

from auth.router import fastapi_users

from .tasks import send_email_report_dashboard

router = APIRouter(prefix="/report")


# Sending in blocking mode
@router.get("/dashboard-blocking")
def get_dashboard_blocking_report(
    user=Depends(fastapi_users.current_user())
):
    send_email_report_dashboard(user.username)
    return "The email has been sent"


# Sending in background using FastAPI BackgroundTasks
@router.get("/dashboard-background")
def get_dashboard_background_report(
    background_tasks: BackgroundTasks, user=Depends(fastapi_users.current_user())
):
    background_tasks.add_task(send_email_report_dashboard, user.username)
    return "The email will be sent in the background"


# Sending in background using Celery
@router.get("/dashboard-celery")
def get_dashboard_background_report(
    user=Depends(fastapi_users.current_user())
):
    send_email_report_dashboard.delay(user.username)
    return "The email will be sent in the background"
