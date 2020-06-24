Feature: View current configuration
  As a user
  I want to be able to view current configuration

  Scenario: View current configuration
    Given I have the following parameters in my configuration file:
      | key         | value       |
      | db_path     | db.json     |
      | language    | pl          |
      | logger_path | logger.json |
    When I view current configuration
    Then I see those listed parameters:
      | key         | value       |
      | db_path     | db.json     |
      | language    | pl          |
      | logger_path | logger.json |

  Scenario: View current configuration with no configuration file
    Given I have no configuration file
    When I view current configuration
    Then I see those listed parameters:
      | key         | value       |
      | db_path     | db.json     |
      | language    | en          |
      | logger_path | logger.json |