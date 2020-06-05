Feature: Full history of rentals
  As a user
  I want to be able to see full history of rentals

  Scenario: Full history of rentals
    Given I have the following logs in logger:
      | id  | data        | text         |
      | 1   | 08-05-2020  | Added        |
      | 1   | 12-05-2020  | Borrowed     |
      | 2   | 08-05-2020  | Added        |
      | 2   | 08-05-2020  | Borrowed     |
      | 2   | 08-05-2020  | Returned     |
      | 2   | 10-05-2020  | Borrowed     |
    When I show full history of rentals
    Then I see those listed logs:
      | id  | data        | text         |
      | 1   | 12-05-2020  | Borrowed     |
      | 2   | 08-05-2020  | Borrowed     |
      | 2   | 08-05-2020  | Returned     |
      | 2   | 10-05-2020  | Borrowed     |
