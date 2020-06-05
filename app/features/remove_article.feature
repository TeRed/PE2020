Feature: Remove article
  In order to see article
  As a user
  I want to see articles as a table

  Scenario: Remove article
    Given I have the following articles in my database:
      | id  | name        | is_available |
      | 1   | Drill       | no           |
      | 2   | Drill Press | no           |
      | 3   | Grinder     | yes          |
    When I remove article 3
    Then I see those listed articles:
      | id  | name        | is_available |
      | 1   | Drill       | no           |
      | 2   | Drill Press | no           |