Feature: Show article by name
  In order to see article
  As a user
  I want to see article as a table

  Scenario: Show one article
    Given I have the following articles in my database:
      | id  | name_pl    | name_en     | total_quantity | quantity | is_available |
      | 1   | Wiertarka  | Drill       | 50             | 50       | no           |
      | 2   |            | Drill Press | 50             | 50       | no           |
      | 3   | Szlifierka | Grinder     | 50             | 50       | yes          |
    When I show article by name "Grinder"
    Then I see those listed articles:
      | id  | name_pl    | name_en     | total_quantity | quantity | is_available |
      | 3   | Szlifierka | Grinder     | 50             | 50       | yes          |

  Scenario: Show empty article
    Given I have the following articles in my database:
      | id  | name_pl    | name_en     | total_quantity | quantity | is_available |
      | 1   | Wiertarka  | Drill       | 50             | 50       | no           |
      | 2   |            | Drill Press | 50             | 50       | no           |
      | 3   | Szlifierka | Grinder     | 50             | 50       | yes          |
    When I show article by name "Drip"
    Then I see those listed articles:
      | id  | name_pl    | name_en     | total_quantity | quantity | is_available |

  Scenario: Show two article
    Given I have the following articles in my database:
      | id  | name_pl    | name_en     | total_quantity | quantity | is_available |
      | 1   | Wiertarka  | Drill       | 50             | 50       | no           |
      | 2   |            | Drill Press | 50             | 50       | no           |
      | 3   | Szlifierka | Grinder     | 50             | 50       | yes          |
    When I show article by name "Drill"
    Then I see those listed articles:
      | id  | name_pl    | name_en     | total_quantity | quantity | is_available |
      | 1   | Wiertarka  | Drill       | 50             | 50       | no           |
      | 2   |            | Drill Press | 50             | 50       | no           |