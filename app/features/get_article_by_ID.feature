Feature: Get article by ID
  As a user
  I want to be able to get article by ID

  Scenario: Get one article
    Given I have the following articles in my database:
      | id  | name_pl    | name_en     | total_quantity | quantity | is_available |
      | 1   | Wiertarka  | Drill       | 50             | 50       | no           |
      | 2   |            | Drill Press | 50             | 50       | no           |
      | 3   | Szlifierka | Grinder     | 50             | 50       | yes          |
    When I get article by ID "1"
    Then I see those listed articles:
      | id  | name_pl    | name_en     | total_quantity | quantity | is_available |
      | 1   | Wiertarka  | Drill       | 50             | 50       | no           |

  Scenario: Get nonexistent article
    Given I have the following articles in my database:
      | id  | name_pl    | name_en     | total_quantity | quantity | is_available |
      | 1   | Wiertarka  | Drill       | 50             | 50       | no           |
      | 2   |            | Drill Press | 50             | 50       | no           |
      | 3   | Szlifierka | Grinder     | 50             | 50       | yes          |
    When I get article by ID "10"
    Then I see no listed articles