import os
import configparser
from dotenv import load_dotenv

# Load the .env file
load_dotenv(override=True)

# Determine the directory containing this script
base_dir = os.path.dirname(os.path.abspath(__file__))

# Load the configuration from the .ini file
config = configparser.ConfigParser()
config.read(os.path.join(base_dir, '../', 'config.ini'))


DEFAULT_SECTION = "DEFAULT"


def get_setting(setting, section=DEFAULT_SECTION, default=None):
    """
    Retrieve the configuration setting from the provided section.

    This function first checks for an environment variable corresponding to the setting.
    If the environment variable isn't set, it then checks the configuration file.
    If the setting isn't in the configuration file, it returns the provided default value or None.

    Args:
    section (str): The section in which to look for the setting.
    setting (str): The setting to retrieve.
    default (str, optional): The default value to return if the setting isn't found.

    Returns:
    str: The value of the setting, or the default value if the setting isn't found.
    """
    # Create the environment variable name from the section and setting
    env_var = os.getenv(f"{setting}".upper())

    # If the environment variable is set, use its value
    if env_var is not None:
        return env_var
    else:
        # If the environment variable isn't set, try to get the value from the configuration file
        return config.get(section, setting, fallback=default)
