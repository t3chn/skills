# Developer Essentials

URL: https://www.greptile.com/docs/code-review/developer-essentials

This guide covers what you need to know when working with Greptile in your day-to-day workflow.

## Triggering Reviews

Tag Greptile in a GitHub/GitLab comment to trigger a review:

@greptileai

You can also ask specific questions:

@greptileai check for memory leaks
@greptileai review the database queries
@greptileai is this thread-safe?

If `@greptileai` doesnt trigger a review, check:

1. Repository is enabled in dashboard
2. PR isnt in an excluded branch
3. Greptile isnt still indexing (first time takes a couple of hours)

### Draft PRs

By default, Greptile **skips draft PRs** to reduce noise.
To review a draft:

@greptileai review this draft

---

## Example Prompts

### Code improvements

@greptileai are there code improvements I can make?

### Explain code

@greptileai can you explain the code in this file?

### Generate tests

@greptileai can you create a test for this file?

---

## Training Greptile

Your reactions shape future reviews:

| Action | What Greptile Learns |
| --- | --- |
| on a comment | Keep flagging issues like this |
| on a comment | Stop mentioning this pattern |
| Reply with context | This is our pattern because... |

It takes 2-3 weeks of consistent reactions for Greptile to adapt to your teams preferences.

### Providing Context

When Greptile flags something intentional, explain why:

@greptileai This is intentional - we use sync calls here
because the webhook requires immediate response

When Greptile misses something:

@greptileai you missed a null check on line 45

Both help Greptile learn your patterns.

---

## Troubleshooting

Review didn't appear

**Check:**

1. Repo enabled in dashboard
2. Indexing complete (first time: a couple of hours)
3. Not a draft PR
4. Branch not excluded by filters

**Fix:** Comment `@greptileai` to force a review

Too many/too few comments

**Too many?** Ask admin to increase severity threshold, or unwanted patterns consistently.** Too few?** Check if repo is fully indexed, or lower severity threshold.

Reviews taking too long

* Small PR: ~1-2 minutes
* Medium PR: ~3 minutes
* Large PR: 3-5 minutes

If longer, repository might be re-indexing.

---

## Whats Next
