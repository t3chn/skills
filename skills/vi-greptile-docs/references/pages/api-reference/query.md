# Query Repo(s)

URL: https://www.greptile.com/docs/api-reference/query

Submit a natural language query about the codebase, **get a natural language answer** with a list of relevant code references (filepaths, line numbers, etc)

1. How does auth work in this codebase?
2. Generate a description for the JIRA ticket with codebase context
3. Rewrite this code snippet using relevant abstractions already in the repo

#### Authorizations

Authorization

string

header

required

Bearer authentication header of the form `Bearer <token>`, where `<token>` is your auth token.

X-GitHub-Token

string

header

required

#### Body

application/json

messages

`object[]`

List of chat messages until now. For a single query, include only one entry in the list with a natural language query.

repositories

`object[]`

List of repos that Greptile should reference while answering your question.

sessionId

string

Optional, defaults to a new session. Only use this if you intend to need to retrieve chat history later.

stream

boolean

Optional, default false.

genius

boolean

Optional, default false. Genius requests are smarter but 8-10 seconds slower, great for complex usecases like reviewing PR and updating technical docs.

#### Response

200 - application/json

Query executed successfully. Response may be streamed.

message

string

sources

`object[]`
