# SSO/SAML

URL: https://www.greptile.com/docs/security/sso

These instructions are for Greptiles Self-Hosted SSO service. If you are using Greptile on the web and want to enable SSO, please contact us at [[email protected]](/cdn-cgi/l/email-protection#c3b0b6b3b3acb1b783a4b1a6b3b7aaafa6eda0acae).

Follow these instructions to enable Enterprise Single Sign-On (SSO) with SAML via BoxyHQ for your Greptile application.

## Prerequisites

Ensure the following services are operational:

* `web` (Greptile web application)
* `jackson` (BoxyHQ SSO service)

## Configure Jackson Service

Set these environment variables for the Jackson service:

| Variable | Description | Example |
| --- | --- | --- |
| `DB_ENCRYPTION_KEY` | Encryption key | `openssl rand -base64 32` |
| `HOST_URL` | Jackson service URL | `sso.greptile.com` |
```
| `EXTERNAL_URL` | External Jackson URL | `https://sso.greptile.com` |
```
| `JACKSON_API_KEYS` | API Keys for Jackson | `openssl rand -base64 32` |
```
| `SAML_AUDIENCE` | Audience identifier | `https://sso.greptile.com` |
```
| `CLIENT_SECRET_VERIFIER` | Secret verifier (alphanumeric only) | `dummy` |
```
| `NEXTAUTH_ADMIN_CREDENTIALS` | Admin credentials | `[email protected]:mysupersecretpassword` |
| `PUBLIC_KEY` | Certificate (see [Jackson docs](https://boxyhq.com/docs/jackson/deploy/env-variables)) | Starts with `-----BEGIN CERTIFICATE-----` |
| `PRIVATE_KEY` | Private key (see [Jackson docs](https://boxyhq.com/docs/jackson/deploy/env-variables)) | PEM formatted |
| `NEXTAUTH_URL` | Same as `EXTERNAL_URL` | `https://sso.greptile.com` |
```
| `NEXTAUTH_SECRET` | JWT secret from `web` service | JWT secret |
| `IDP_ENABLED` | Enable IdP | `true` |

## Set Up Database Entries

1. Log in to your PostgreSQL database.
2. Create or locate an existing `Organization`.
3. Generate an `InternalApiKey` linked to that `Organization`:


openssl rand -base64 36

4. Create a new `SamlConnection`:
* Set `org_id` to your Organization ID.
* Set `tenant_id` to your email domain (e.g., `example.com`).

## Configure SSO Connection

1. Visit the Jackson admin console.
2. Log in using admin credentials configured earlier.
3. Navigate to **Enterprise SSO Connections** .
4. Click **New Setup Link** .
* Set tenant to users email domain.
* Set product as `greptile`.
* Allowed redirect URL: `https://<greptile_web_domain>`
* Default redirect URL: `https://<greptile_web_domain>/login/saml`
5. Generate the setup link.
6. Share the setup link with your IdP admin for SSO configuration.

## Completing SSO Setup

Once configuration is complete:

* Users can log in to the web app via SSO, by entering their email.
* New SSO users will automatically be added to the configured `Organization`.

## Important Notes

* `AUTH_BOXYHQ_SAML_SECRET` in your web service must match Jacksons `CLIENT_SECRET_VERIFIER` and should **not** include special characters.
