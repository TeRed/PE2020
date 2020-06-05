Feature: History of rentals of article
  As a user
  I want to be able to see history of rentals of article

  Scenario: History of rentals of article
    Given I have the following logs in logger:
      | id  | data        | text         |
      | 1   | 08-05-2020  | Added        |
      | 1   | 12-05-2020  | Borrowed     |
      | 2   | 08-05-2020  | Added        |
      | 2   | 08-05-2020  | Borrowed     |
      | 2   | 08-05-2020  | Returned     |
      | 2   | 10-05-2020  | Borrowed     |
    When I show history of rentals of article 2
    Then I see those listed logs:
      | id  | data        | text         |
      | 2   | 08-05-2020  | Borrowed     |
      | 2   | 08-05-2020  | Returned     |
      | 2   | 10-05-2020  | Borrowed     |
