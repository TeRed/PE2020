Feature: Show borrowed articles
  In order to see borrow article
  As a user
  I want to see articles with status 'no'

  Scenario: Show borrowed articles
    Given I have the following articles in my database:
      | id  | name        | is_available |
      | 1   | Drill       | no           |
      | 2   | Drill Press | no           |
      | 3   | Grinder     | yes          |
      | 4   | Spade       | no           |
      | 5   | Axe         | yes          |
      | 6   | Compactor   | yes          |
    When I show borrowed articles
    Then I see those listed articles:
      | id  | name        | is_available |
      | 1   | Drill       | no           |
      | 2   | Drill Press | no           |
      | 4   | Spade       | no           |