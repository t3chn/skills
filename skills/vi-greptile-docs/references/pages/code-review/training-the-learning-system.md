# Training the Learning System

URL: https://www.greptile.com/docs/code-review/training-the-learning-system

Greptile learns from your teams feedback to provide increasingly relevant suggestions. The primary training methods are emoji reactions and explanatory comments.

Learning is continuous. noticeable improvement in the first few weeks of consistent feedback, and it keeps getting better over time.

## Using Reactions (/)

Reactions are the fastest way to train Greptile. Every reaction teaches it what matters to your team.

| Your Reaction | What Greptile Learns |
| --- | --- |
| This is useful - make more comments like this |
| This isnt helpful - stop making these comments |
| No reaction | Neutral signal, lower priority over time |

Only and train the system. Other emojis (, , etc.) are treated as neutral.

**For reactions** , add a quick comment explaining why:

@greptileai We don't enforce this in test files

This helps Greptile understand the context, not just that you disagreed.

## Explaining Preferences

While reactions teach **what** you like, comments teach ** why**.
**Be specific:**

"We don't do this"
"We avoid wildcard imports because they hide dependencies"

**Keep it short:**

[Long paragraph about company history]
"Webhooks must be synchronous - provider requires immediate response"

## Tracking Progress

The **Analytics** page in your dashboard shows how training is going:

| Metric | What it tells you |
| --- | --- |
| **Feedback Reactions** | How consistently your team is reacting to comments |
| **Addressed Comments per PR** | Whether Greptiles suggestions are being implemented |
| **Recent Issues Caught** | Types of issues Greptile is flagging |

Low reaction counts? Remind the team to / comments. High addressed rates mean Greptile is learning what matters.

## Accelerating Learning

Instead of waiting for organic learning, you can:

2. **Create explicit rules** - Define standards in the dashboard or `greptile.json`

## Whats next?
