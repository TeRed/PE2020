Feature: Show borrowed articles
  In order to see borrow article
  As a user
  I want to see articles with total_quantity > quantity

  Scenario: Show borrowed articles
    Given I have the following articles in my database:
      | id  | name_pl      | name_en   | total_quantity | quantity | is_available |
      | 1   | Wiertarka    | Drill     | 50             | 50       | no           |
      | 2   | Młotek       | Hammer    | 250            | 240      | no           |
      | 3   | Szlifierka   | Grinder   | 25             | 25       | yes          |
      | 4   | Łopata       | Spade     | 50             | 50       | yes          |
      | 5   | Siekierka    | Axe       | 0              | 0        | yes          |
      | 6   | Zagęszczarka | Compactor | 250            | 150      | yes          |
    When I show borrowed articles
    Then I see those listed articles:
      | id  | name_pl      | name_en   | total_quantity | quantity | is_available |
      | 2   | Młotek       | Hammer    | 250            | 240      | no           |
      | 6   | Zagęszczarka | Compactor | 250            | 150      | yes          |