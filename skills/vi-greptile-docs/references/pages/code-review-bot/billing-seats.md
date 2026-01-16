# Billing

URL: https://www.greptile.com/docs/code-review-bot/billing-seats

Greptile bills based on **active developers** in your billing period.

## What is an Active Developer?

An active developer is anyone who has **2 or more PRs reviewed by Greptile** during a billing period.
**Doesnt count toward billing:**

* Developers with only 0-1 reviewed PRs
* Bot accounts youve excluded (e.g., `dependabot[bot]`)
* Users who only view reviews but dont author PRs

## Excluding Bots from Billing

Bot accounts that are excluded from reviews dont count toward your active developer count.

* Dashboard
* greptile.json

Go to **Settings Review Triggers Excluded Authors** and add:

* `dependabot[bot]`
* `renovate[bot]`
* Any service accounts

```
{
"excludeAuthors": ["dependabot[bot]", "renovate[bot]"]
}
```

## Managing Your Subscription

| Action | When it takes effect |
| --- | --- |
| Upgrade | Immediately |
| Downgrade | Next billing cycle |
| Cancel | Contact support |

```
Track active developers in your [organization dashboard](https://app.greptile.com).
```

For specific billing questions, subscription changes, or custom enterprise pricing, contact [[email protected]](/cdn-cgi/l/email-protection#bdd5d8d1d1d2fddacfd8cdc9d4d1d893ded2d0).
