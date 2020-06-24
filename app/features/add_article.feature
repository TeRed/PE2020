Feature: Add article
  As a user
  I want to be able to add article

  Scenario: Add article
    Given I have the following articles in my database:
      | id  | name_pl   | name_en     | total_quantity | quantity | is_available |
      | 1   | Wiertarka | Drill       | 50             | 50       | no           |
      | 2   |           | Drill Press | 50             | 50       | no           |
    When I add following article:
      | name_pl    | name_en     | total_quantity | quantity | is_available |
      | Szlifierka | Grinder     | 50             | 50       | yes          |
    Then I see those listed articles:
      | id  | name_pl    | name_en     | total_quantity | quantity | is_available |
      | 1   | Wiertarka  | Drill       | 50             | 50       | no           |
      | 2   |            | Drill Press | 50             | 50       | no           |
      | 3   | Szlifierka | Grinder     | 50             | 50       | yes          |