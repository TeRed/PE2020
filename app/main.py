from interface import Interface
from config_manager import ConfigManager
from db_connector import DBConnector
from logger_connector import LoggerConnector
from file_connector import LoggerFileConnector

config_manager = ConfigManager("config.json")
logger_file_connector = LoggerFileConnector(config_manager)

logger_connector = LoggerConnector(logger_file_connector)
db_connector = DBConnector(config_manager)

application = Interface(db_connector, logger_connector, config_manager)
application.menu()