# Get Repository Info

URL: https://www.greptile.com/docs/api-reference/get-repository

Retrieves information about a specific repository. The `repositoryId` should be URL-encoded in the format `remote:branch:owner/repository`.

#### Authorizations

ApiKeyAuth & GitHubToken

Authorization

string

header

required

Bearer authentication header of the form `Bearer <token>`, where `<token>` is your auth token.

#### Path Parameters

repositoryId

string

required

#### Response

200 - application/json

Repository information retrieved successfully.

repository

string

remote

string

branch

string

private

boolean

status

string

filesProcessed

integer

numFiles

integer

sha

string
