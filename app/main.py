from interface import Interface
from config_manager import ConfigManager
from db_connector import DBConnector
from logger_connector import LoggerConnector

config_manager = ConfigManager("config.json")
logger_connector = LoggerConnector(config_manager)
db_connector = DBConnector(config_manager)

application = Interface(db_connector, logger_connector, config_manager)
application.menu()