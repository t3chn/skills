# Search Repo(s)

URL: https://www.greptile.com/docs/api-reference/search

Submit a natural language search query to find relevant code references without generating an AI response.
Returns a list of relevant code files, functions, and snippets based on your search query, similar to the query endpoint but **without the AI-generated answer** .
Use this endpoint when you only need the source references and dont need an AI explanation.

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

query

string

Natural language search query to find the right code in the repo.

repositories

`object[]`

List of repos that Greptile should reference while answering your question.

sessionId

string

Optional, defaults to a new session. You only need this if you want to retrieve this query/response later.

stream

boolean

Optional, default false.

#### Response

200 - application/json

Query executed successfully. Response may be streamed.

repository

string

The name of the repository where the file resides.

remote

string

The remote service or platform where the repository is hosted.

branch

string

The branch of the repository where the file is found.

filepath

string

The relative path to the file within the repository.

linestart

integer | null

The starting line number of the code that is relevant, if applicable.

lineend

integer | null

The ending line number of the code that is relevant, if applicable.

summary

string

A summary or description of the contents and functionalities of the file.

distance

number | null

Similarity score for the source returned by the API. Lower values indicate higher similarity.
