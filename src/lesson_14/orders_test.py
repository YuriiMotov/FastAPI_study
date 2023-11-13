from typing import Annotated

from fastapi import APIRouter, Depends, BackgroundTasks


orders_router = APIRouter()


async def dep_a():
    print("dep_a before yield")
    try:
        yield "value of the `a`"
    except Exception as e:
        print("dep_a caught an exception")
        raise
    finally:
        print("dep_a after yield")


async def dep_b(a: Annotated[str, Depends(dep_a)]):
    print("dep_b before yield")
    try:
        yield a
    except Exception as e:
        print("dep_b caught an exception")
        raise
    finally:
        print("dep_b after yield")


async def dep_c(a: Annotated[str, Depends(dep_a)]):
    print("dep_c before yield")
    try:
        yield a
    except Exception as e:
        print("dep_c caught an exception")
        raise
    finally:
        print("dep_c after yield")


##########################################################################################
# Just nested dependencies
@orders_router.post("/operation-with-dependencies-1")
async def operation_with_dependencies_1(
    b: Annotated[str, Depends(dep_b)],
    c: Annotated[str, Depends(dep_c)]
):
    print("Sending response from the endpoint's function")
    return (b, c)

    # dep_a before yield
    # dep_b before yield
    # dep_c before yield
    # Sending response from the endpoint's function
    # INFO:     127.0.0.1:55586 - "POST /orders-tests/operation-with-dependencies-1 HTTP/1.1" 200 OK
    # dep_c after yield
    # dep_b after yield
    # dep_a after yield



##########################################################################################
# Nested dependancies and exception in the endpoint's function
@orders_router.post("/operation-with-dependencies-2")
async def operation_with_dependencies_2(
    b: Annotated[str, Depends(dep_b)],
    c: Annotated[str, Depends(dep_c)]
):
    print("Raising exception from the endpoint's function")
    raise Exception("Exception from the endpoint's function")
    return (b, c)

    # dep_a before yield
    # dep_b before yield
    # dep_c before yield
    # Raising exception from the endpoint's function
    # dep_c caught an exception
    # dep_c after yield
    # dep_b caught an exception
    # dep_b after yield
    # dep_a caught an exception
    # dep_a after yield
    # INFO:     127.0.0.1:50824 - "POST /orders-tests/operation-with-dependencies-2 HTTP/1.1" 500 Internal Server Error
    


##########################################################################################
# Nested dependencies with background task and exception in the background task

async def function_with_exception():
    print("Start background task's execution and raise exception")
    raise Exception("Exception from the background task's function")
    print("Background task finished")

@orders_router.post("/operation-with-dependencies-3")
async def operation_with_dependencies_3(
    b: Annotated[str, Depends(dep_b)],
    c: Annotated[str, Depends(dep_c)],
    background_tasks: BackgroundTasks
):
    background_tasks.add_task(function_with_exception)
    print("Sending response from the endpoint's function")
    return (b, c)

    # dep_a before yield
    # dep_b before yield
    # dep_c before yield
    # Sending response  from the endpoint's function
    # INFO:     127.0.0.1:53498 - "POST /orders-tests/operation-with-dependencies-3 HTTP/1.1" 200 OK
    # Start background task's execution and raise exception
    # dep_c caught an exception
    # dep_c after yield
    # dep_b caught an exception
    # dep_b after yield
    # dep_a caught an exception
    # dep_a after yield

