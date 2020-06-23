Feature: Return articles
  In order to return article
  As a user
  I want to see articles with changed quantity

  Scenario: Return articles happy path
    Given I have the following articles in my database:
      | id  | name_pl      | name_en   | total_quantity | quantity | is_available |
      | 1   | Wiertarka    | Drill     | 50             | 50       | no           |
      | 2   | Młotek       | Hammer    | 250            | 240      | no           |
      | 3   | Szlifierka   | Grinder   | 25             | 20       | yes          |
      | 4   | Łopata       | Spade     | 50             | 50       | yes          |
      | 5   | Siekierka    | Axe       | 0              | 0        | yes          |
      | 6   | Zagęszczarka | Compactor | 250            | 150      | yes          |
    When I return "5" articles with ID "3"
    Then I see those listed articles:
      | id  | name_pl      | name_en   | total_quantity | quantity | is_available |
      | 1   | Wiertarka    | Drill     | 50             | 50       | no           |
      | 2   | Młotek       | Hammer    | 250            | 240      | no           |
      | 3   | Szlifierka   | Grinder   | 25             | 25       | yes          |
      | 4   | Łopata       | Spade     | 50             | 50       | yes          |
      | 5   | Siekierka    | Axe       | 0              | 0        | yes          |
      | 6   | Zagęszczarka | Compactor | 250            | 150      | yes          |

  Scenario: Return articles too many qty
    Given I have the following articles in my database:
      | id  | name_pl      | name_en   | total_quantity | quantity | is_available |
      | 1   | Wiertarka    | Drill     | 50             | 50       | no           |
      | 2   | Młotek       | Hammer    | 250            | 240      | no           |
      | 3   | Szlifierka   | Grinder   | 25             | 20       | yes          |
      | 4   | Łopata       | Spade     | 50             | 50       | yes          |
      | 5   | Siekierka    | Axe       | 0              | 0        | yes          |
      | 6   | Zagęszczarka | Compactor | 250            | 150      | yes          |
    When I return "5" articles with ID "4"
    Then I see those listed articles:
      | id  | name_pl      | name_en   | total_quantity | quantity | is_available |
      | 1   | Wiertarka    | Drill     | 50             | 50       | no           |
      | 2   | Młotek       | Hammer    | 250            | 240      | no           |
      | 3   | Szlifierka   | Grinder   | 25             | 20       | yes          |
      | 4   | Łopata       | Spade     | 50             | 50       | yes          |
      | 5   | Siekierka    | Axe       | 0              | 0        | yes          |
      | 6   | Zagęszczarka | Compactor | 250            | 150      | yes          |

  Scenario: Return articles which is_unavailable
    Given I have the following articles in my database:
      | id  | name_pl      | name_en   | total_quantity | quantity | is_available |
      | 1   | Wiertarka    | Drill     | 50             | 50       | no           |
      | 2   | Młotek       | Hammer    | 250            | 240      | no           |
      | 3   | Szlifierka   | Grinder   | 25             | 20       | yes          |
      | 4   | Łopata       | Spade     | 50             | 50       | yes          |
      | 5   | Siekierka    | Axe       | 0              | 0        | yes          |
      | 6   | Zagęszczarka | Compactor | 250            | 150      | yes          |
    When I return "5" articles with ID "2"
    Then I see those listed articles:
      | id  | name_pl      | name_en   | total_quantity | quantity | is_available |
      | 1   | Wiertarka    | Drill     | 50             | 50       | no           |
      | 2   | Młotek       | Hammer    | 250            | 245      | yes          |
      | 3   | Szlifierka   | Grinder   | 25             | 20       | yes          |
      | 4   | Łopata       | Spade     | 50             | 50       | yes          |
      | 5   | Siekierka    | Axe       | 0              | 0        | yes          |
      | 6   | Zagęszczarka | Compactor | 250            | 150      | yes          |