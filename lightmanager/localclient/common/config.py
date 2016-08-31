"""
Configuration module to use INI config files within the micro services framework.
"""
from os.path import join, dirname, isfile, isdir, expanduser
import os
import configparser
import logging

logger = logging.getLogger(__name__)
config = configparser.ConfigParser()


def load_config(module_path=None, file_list=None):
    """
    Load configuration files supplying either a module name or a list of files
    :param module_path:
    :param file_list:
    :return:
    """
    if file_list:
        for c_file in file_list:
            config.read(c_file)

    elif module_path:
        default_conf_file = join(dirname(module_path), "config", "default.ini")
        user_conf_dir = join(expanduser("~"), "lm_config")
        user_conf_file = join(user_conf_dir, os.path.basename(dirname(module_path)) + '.ini')

        if isfile(default_conf_file):
            logger.info("found default config file at: {}".format(default_conf_file))
            config.read(default_conf_file)
        else:
            logger.warning("No default config file found in module path {}".format(module_path))

        if not isdir(user_conf_dir):
            os.mkdir(user_conf_dir)
        if isfile(user_conf_file):
            logger.info("found user config file at: {}".format(user_conf_file))
            config.read(user_conf_file)
        else:
            logger.warning("User config file {} not found".format(user_conf_file))


def get_sections_containing(text):
    return [section for section in config.sections() if text in str(section)]


def get_section_options(section):
    return config.options(section)


def get(section, option, default=None):
    try:
        return config.get(section, option)
    except (configparser.NoSectionError, configparser.NoOptionError):
        return default


def getint(section, option, default=None):
    try:
        return config.getint(section, option)
    except (configparser.NoSectionError, configparser.NoOptionError):
        return default


def getfloat(section, option, default=None):
    try:
        return config.getfloat(section, option)
    except (configparser.NoSectionError, configparser.NoOptionError):
        return default


def getboolean(section, option, default=None):
    try:
        return config.getboolean(section, option)
    except (configparser.NoSectionError, configparser.NoOptionError):
        return default