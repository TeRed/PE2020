Feature: Show all articles
  In order to see article
  As a user
  I want to see articles as a table

  Scenario: Show all articles
    Given I have the following articles in my database:
      | id  | name_pl    | name_en     | total_quantity | quantity | is_available |
      | 1   | Wiertarka  | Drill       | 50             | 50       | no           |
      | 2   |            | Drill Press | 50             | 50       | no           |
      | 3   | Szlifierka | Grinder     | 50             | 50       | yes          |
    When I show articles
    Then I see those listed articles:
      | id  | name_pl    | name_en     | total_quantity | quantity | is_available |
      | 1   | Wiertarka  | Drill       | 50             | 50       | no           |
      | 2   |            | Drill Press | 50             | 50       | no           |
      | 3   | Szlifierka | Grinder     | 50             | 50       | yes          |