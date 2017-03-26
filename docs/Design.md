# Functionality

[display issues]
=> app: list issues to triage
=> workflow: list issues according to (configured) filters
=> repository: query api with params
<= repository: returns json
<= workflow: converts to issue objects
<= app: displays issue objects

[select an action per issue]
=> app: specify the label the selected issue should have
    (issue, action)
=> workflow: perform the label action
=> repository: post api with label params
<= repository: success/fail
<= workflow: trap success and return display action
<= app: either update the issue display to show the added tag
        OR display the error message


# Components And Interactions

- GithubIssuesRepository
    - (requires)
    - (config) auth token, owner/repo
        - declares it's config dependencies to allow for external prompting
    - (functionality) retrieve github issues (with query filters)

    - query filters
        - state
        - labels
        - sort: created, updated, comments

    - update issues (state, label)
        - state (open, closed)
        - labels (string[] replaces)

- TriageWorkflow
    - (defines) filters (which issues to find)
        - filterset:
            - unlabelled
            - open issues
            - zero comments [post query filter]
    - (defines) available issue actions
    - find_issues
    - process_issues

- Application
    - instantiate and configure repository
        - repo config (token, owner/repo)
    - use workflow
        - find_issues => display issues
        - ui_loop => prompt for actions per issue
        - process issues with actions => process_issues

# Data Model

## Issue (object)
+ title: (string) - The issue title
+ description (string) - A description of the issue
+ state (enum)
    - open (string)
    - closed (string)
+ tags (array[string])
+ comments (number) - The number of comments


## Action (object)
+ name: (string) - The name of the action
