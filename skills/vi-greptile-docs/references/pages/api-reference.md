# Index Repository

URL: https://www.greptile.com/docs/api-reference

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

remote

string

Supported values are "github" or "gitlab".

repository

string

Repository identifier in "owner/repository" format.

branch

string

Branch name to index.

reload

boolean

If false, won't reprocess if previously successful. Optional, default true.

notify

boolean

Whether to notify the user upon completion. Optional, default true.

#### Response

200 - application/json

Repository processing started.

message

string

Processing status message.

statusEndpoint

string

URL to check the status of the repository processing.
