# HNG 11 Backend Stage 1 Task

## Task Objective

Set up a basic web server in your preferred stack. Deploy it to any free hosting platform and expose an API endpoint that conforms to the criteria below:

- Endpoint: [GET] `<example.com>/api/hello?visitor_name="Mark"` (where `<example.com>` is your server origin)

**Response**

```json
{
  "client_ip": "127.0.0.1", // The IP address of the requester
  "location": "New York", // The city of the requester
  "greeting": "Hello, Mark!, the temperature is 11 degrees Celsius in New York"
}
```

### Testing the Submission

To access the endpoint, open your browser and visit the following URL:

```bash
http://seyipythonian.pythonanywhere.com/api/hello?visitor_name=YourName
```

Replace `YourName` with your desired name.

To test with the name "Sapagrammer", the URL will be: <http://seyipythonian.pythonanywhere.com/api/hello?visitor_name=Sapagrammer>

The response will be in JSON format and will include:

- client_ip: Your public IP address.
- location: The city corresponding to your IP address.
- greeting: A personalized greeting message including your name and the current temperature in your location.

**Example response**

```json
{
  "client_ip":"197.220.45.88",
  "greeting":"Hello, Sapagrammer!, the temperature is 26.1 degrees Celsius in Lagos",
  "location":"Lagos"
}
```
