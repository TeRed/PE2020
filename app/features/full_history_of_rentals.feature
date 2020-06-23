Feature: Full history of rentals
  As a user
  I want to be able to see full history of rentals

  Scenario: Full history of rentals
    Given I have the following logs in logger:
      | id  | data        | text        |
      | 1   | 2020-06-17  | Added       |
      | 1   | 2020-06-17  | Borrowed 2  |
      | 2   | 2020-05-08  | Added       |
      | 2   | 2020-05-10  | Borrowed 4  |
      | 2   | 2020-05-15  | Returned 2  |
      | 2   | 2020-06-17  | Borrowed 4  |
    When I show full history of rentals
    Then I see those listed logs:
      | id  | data        | text        |
      | 1   | 2020-06-17  | Borrowed 2  |
      | 2   | 2020-05-10  | Borrowed 4  |
      | 2   | 2020-05-15  | Returned 2  |
      | 2   | 2020-06-17  | Borrowed 4  |
