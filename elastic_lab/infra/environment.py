"""
Functions regarding environment variables.
"""
import os
from distutils.util import strtobool


def getenv_or_default(env_name: str, default_value: str) -> str:
    """
    Gets an env variable or returns a default value.
    """
    if (env_value := os.getenv(env_name)) is None:
        return default_value

    return env_value


def getenv_or_exception(env_name: str) -> str:
    """
    Gets an env variable or raises an exception.
    """
    if (env_value := os.getenv(env_name)) is None:
        raise Exception("Missing required env var is missing: %s", env_name)

    return env_value


def getenvbool_or_exception(env_name: str) -> bool:
    """
    Evals env var string as booleans. Raises an exception if the env var was not found.
    """
    env_var = getenv_or_exception(env_name)

    return strtobool(env_var)
