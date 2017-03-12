# Objects

- GithubIssuesRepository
  - retrieve github issues (with query filter)
  - update issues (state, label)

- TriageWorkflow
    - find_issues
        - (defines) filters (which issues to find)
        - associates issues with actions
    - process_issues
        - (defines) actions (against issues)


# Data Structures

## Issue (object)
+ title: (string) - The issue title
+ description (string) - A description of the issue
+ state (enum)
    - opened (string)
    - closed (string)
+ tags (array[string])


boolean, string, number
array, enum, object
