import time
import inspect
from pydantic import BaseModel, TypeAdapter

from typing import Type, List
from datetime import datetime, date


def json_response(schema: Type[BaseModel]):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            # Check if the schema is a generic with __origin__ attribute (for Python 3.8, we handle lists specifically)
            if hasattr(schema, "__origin__") and schema.__origin__ is list:
                # Extract the model class from List[Model]
                model_cls = schema.__args__[0]
                # Use model_validate to parse the result as a list of model instances
                type_adapter = TypeAdapter(List[model_cls])
                model_list = type_adapter.validate_python(result)
                # Convert each model in the list to a dict
                serializable_list = [convert_to_serializable(model.model_dump()) for model in model_list]
                return serializable_list
            else:
                # If it's a single model, parse and convert to dict
                model_instance = schema.model_validate(result)
                return convert_to_serializable(model_instance.model_dump())

        return wrapper

    return decorator

def convert_to_serializable(obj):
    if isinstance(obj, datetime) or isinstance(obj, date):
        return obj.isoformat()
    if isinstance(obj, list):
        return [convert_to_serializable(item) for item in obj]
    if isinstance(obj, dict):
        return {key: convert_to_serializable(value) for key, value in obj.items()}
    return obj


def controllers_to_fns(controllers):
    funcs = {}
    for controller_prefix, controller_instance in controllers.items():
        for method_name in dir(controller_instance):
            if not method_name.startswith("_"):  # Avoid dunder methods and private methods
                method = getattr(controller_instance, method_name)
                if callable(method):
                    funcs[f"{controller_prefix}_{method_name}"] = method
    return funcs


def expose_fns(window, functions):
    func_list = []
    for func_name, func in functions.items():
        name = func_name
        window._functions[name] = func
        params = list(inspect.getfullargspec(func).args)
        func_list.append({"func": name, "params": params})

    if window.events.loaded.is_set():
        window.evaluate_js(f"window.pywebview._createApi({func_list})")


def update_listener(window=None, controllers={}):
    if not window:
        return

    while True:
        funcs = controllers_to_fns(controllers)
        expose_fns(window, funcs)
        time.sleep(1)

def get_or_create(session, model, defaults=None, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        params = {**kwargs, **(defaults or {})}
        instance = model(**params)
        session.add(instance)
        session.commit()
        return instance, True


def update_or_create(session, model, defaults=None, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        for key, value in defaults.items():
            setattr(instance, key, value)
        session.commit()
        return instance, False
    else:
        params = {**kwargs, **(defaults or {})}
        instance = model(**params)
        session.add(instance)
        session.commit()
        return instance, True