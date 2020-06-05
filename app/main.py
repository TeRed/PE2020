from interface import Interface
from config_manager import ConfigManager
from db_connector import DBConnector
from logger_connector import LoggerConnector
from file_connector import LoggerFileConnector
from file_connector import DbFileConnector

config_manager = ConfigManager("config.json")
logger_file_connector = LoggerFileConnector(config_manager)
db_file_connector = DbFileConnector(config_manager)

logger_connector = LoggerConnector(logger_file_connector)
db_connector = DBConnector(db_file_connector)

application = Interface(db_connector, logger_connector, config_manager)
application.menu()
