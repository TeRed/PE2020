Feature: Save current configuration
  As a user
  I want to be able to save current configuration

  Scenario: Save current configuration
    Given I have the following parameters in my configuration file:
      | key         | value       |
      | db_path     | db.json     |
      | language    | en          |
      | logger_path | logger.json |
    And I change parameter "db_path" to value "test.json"
    When I save current configuration
    Then I see those listed parameters when application is reloaded:
      | key         | value       |
      | db_path     | test.json   |
      | language    | en          |
      | logger_path | logger.json |