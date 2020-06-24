Feature: Change current configuration
  As a user
  I want to be able to change current configuration

  Scenario: Change current configuration
    Given I have the following parameters in my configuration file:
      | key         | value       |
      | db_path     | db.json     |
      | language    | en          |
      | logger_path | logger.json |
    When I change parameter "db_path" to value "test.json"
    Then I see those listed parameters:
      | key         | value       |
      | db_path     | test.json   |
      | language    | en          |
      | logger_path | logger.json |