Feature: Show article by name
  In order to see article
  As a user
  I want to see article as a table

  Scenario: Show one article
    Given I have the following articles in my database:
      | id  | name        | is_available |
      | 1   | Drill       | no           |
      | 2   | Drill Press | no           |
      | 3   | Grinder     | yes          |
      | 4   | Spade       | no           |
      | 5   | Axe         | yes          |
      | 6   | Compactor   | yes          |
    When I show article by name Grinder
    Then I see those listed articles:
      | id  | name        | is_available |
      | 3   | Grinder     | yes          |