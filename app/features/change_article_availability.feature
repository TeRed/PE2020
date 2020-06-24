Feature: Change article availability
  As a user
  I want to be able to change article availability

  Scenario: Change to available
    Given I have the following articles in my database:
      | id  | name_pl      | name_en   | total_quantity | quantity | is_available |
      | 1   | Wiertarka    | Drill     | 50             | 50       | no           |
      | 2   | Młotek       | Hammer    | 250            | 240      | no           |
    When I change to available article 1
    Then I see those listed articles:
      | id  | name_pl      | name_en   | total_quantity | quantity | is_available |
      | 1   | Wiertarka    | Drill     | 50             | 50       | yes          |
      | 2   | Młotek       | Hammer    | 250            | 240      | no           |

  Scenario: Change to available
    Given I have the following articles in my database:
      | id  | name_pl      | name_en   | total_quantity | quantity | is_available |
      | 1   | Wiertarka    | Drill     | 50             | 50       | no           |
      | 2   | Młotek       | Hammer    | 250            | 240      | no           |
    When I change to available article 2
    Then I see those listed articles:
      | id  | name_pl      | name_en   | total_quantity | quantity | is_available |
      | 1   | Wiertarka    | Drill     | 50             | 50       | no           |
      | 2   | Młotek       | Hammer    | 250            | 240      | yes          |

  Scenario: Change to not available
    Given I have the following articles in my database:
      | id  | name_pl      | name_en   | total_quantity | quantity | is_available |
      | 1   | Wiertarka    | Drill     | 50             | 50       | no           |
      | 2   | Młotek       | Hammer    | 250            | 240      | yes          |
    When I change to not available article 2
    Then I see those listed articles:
      | id  | name_pl      | name_en   | total_quantity | quantity | is_available |
      | 1   | Wiertarka    | Drill     | 50             | 50       | no           |
      | 2   | Młotek       | Hammer    | 250            | 240      | no           |

  Scenario: Change to unchanged
    Given I have the following articles in my database:
      | id  | name_pl      | name_en   | total_quantity | quantity | is_available |
      | 1   | Wiertarka    | Drill     | 50             | 50       | no           |
      | 2   | Młotek       | Hammer    | 250            | 240      | no           |
    When I change to not available article 2
    Then I see those listed articles:
      | id  | name_pl      | name_en   | total_quantity | quantity | is_available |
      | 1   | Wiertarka    | Drill     | 50             | 50       | no           |
      | 2   | Młotek       | Hammer    | 250            | 240      | no           |