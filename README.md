# Backend Stage 1 Task

## Submission

The endpoint is available [here](http://seyipythonian.pythonanywhere.com/api/?slack_name=Pythonian&track=backend/)

### Task Objective

Create and host an endpoint using any programming language of your choice.
The endpoint should take two GET request query parameters and return specific information in JSON format.

### Task Requirements

The information required includes:
* Slack name
* Current day of the week
* Current UTC time (with validation of +/-2)
* Track
* The GitHub URL of the file being run
* The GitHub URL of the full source code.
* A Status Code of Success

**Sample Input** 

`http://example.com/api?slack_name=example_name&track=backend.`

**Sample Response Format** 

```bash
{
  "slack_name": "example_name",
  "current_day": "Monday",
  "utc_time": "2023-08-21T15:04:05Z",
  "track": "backend",
  "github_file_url": "https://github.com/username/repo/blob/main/file_name.ext",
  "github_repo_url": "https://github.com/username/repo",
  “status_code”: 200
}
```

### Submission Details:

Please follow these submission guidelines
* Get into your DM
* Type /grade <your-api-endpoint-url-with-the-query-parameters>
* E.g: /grade http://example.com/api?slack_name=example_name&track=backend
* Check your result

### Deadline: 

**12th September 2023, 11:59 PM GMT + 1**
