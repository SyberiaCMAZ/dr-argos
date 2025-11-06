import importlib
import pkgutil
from types import ModuleType
from typing import Iterable
import inspect


def walk_module(module: str) -> Iterable[ModuleType]:
    """Return all modules from a module recursively.

    Note that this will import all the modules and submodules. It returns the
    provided module as well.
    """

    def onerror(err):
        raise err  # pragma: no cover

    spec = importlib.util.find_spec(module)
    if not spec:
        raise ImportError(f"Module {module} not found")
    mod = importlib.import_module(spec.name)
    yield mod
    if spec.submodule_search_locations:
        for info in pkgutil.walk_packages(
            spec.submodule_search_locations, f"{spec.name}.", onerror
        ):
            mod = importlib.import_module(info.name)
            yield mod


def get_subclasses_from_module[TClass](
    module: ModuleType, base_class: type[TClass]
) -> Iterable[type[TClass]]:
    for name, obj in inspect.getmembers(module, inspect.isclass):
        # Ensure it's defined in the module and is subclass of base_class (excluding the base itself)
        if (
            obj.__module__ == module.__name__
            and issubclass(obj, base_class)
            and obj is not base_class
        ):
            yield obj
