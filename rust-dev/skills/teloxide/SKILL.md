---
name: Teloxide
description: This skill should be used when the user asks about "teloxide", "Telegram bot Rust", "Rust bot", "Telegram Rust", or needs guidance on building Telegram bots with Rust.
version: 1.0.0
---

# Teloxide

Telegram bot framework for Rust.

## Setup

```toml
# Cargo.toml
[dependencies]
teloxide = { version = "0.13", features = ["macros"] }
tokio = { version = "1", features = ["full"] }
serde = { version = "1", features = ["derive"] }
serde_json = "1"
sqlx = { version = "0.8", features = ["runtime-tokio", "sqlite"] }
tracing = "0.1"
tracing-subscriber = "0.3"
dotenvy = "0.15"
```

## Basic Bot

```rust
use teloxide::{prelude::*, utils::command::BotCommands};

#[derive(BotCommands, Clone)]
#[command(rename_rule = "lowercase", description = "Available commands:")]
enum Command {
    #[command(description = "Start the bot")]
    Start,
    #[command(description = "Show help")]
    Help,
    #[command(description = "Add a task")]
    Add(String),
    #[command(description = "List tasks")]
    Tasks,
}

#[tokio::main]
async fn main() {
    dotenvy::dotenv().ok();
    tracing_subscriber::fmt::init();

    let bot = Bot::from_env();

    Command::repl(bot, handle_command).await;
}

async fn handle_command(bot: Bot, msg: Message, cmd: Command) -> ResponseResult<()> {
    match cmd {
        Command::Start => {
            bot.send_message(msg.chat.id, "Welcome! Use /help to see commands.").await?;
        }
        Command::Help => {
            bot.send_message(msg.chat.id, Command::descriptions().to_string()).await?;
        }
        Command::Add(task) => {
            bot.send_message(msg.chat.id, format!("Task added: {task}")).await?;
        }
        Command::Tasks => {
            bot.send_message(msg.chat.id, "Your tasks:\n1. Example task").await?;
        }
    }
    Ok(())
}
```

## Bot with State and Dialogue

```rust
use teloxide::{
    dispatching::{dialogue, dialogue::InMemStorage, UpdateHandler},
    prelude::*,
};

type MyDialogue = Dialogue<State, InMemStorage<State>>;
type HandlerResult = Result<(), Box<dyn std::error::Error + Send + Sync>>;

#[derive(Clone, Default)]
pub enum State {
    #[default]
    Start,
    ReceiveTaskTitle,
    ReceiveTaskDueDate { title: String },
}

fn schema() -> UpdateHandler<Box<dyn std::error::Error + Send + Sync + 'static>> {
    use dptree::case;

    let command_handler = teloxide::filter_command::<Command, _>()
        .branch(case![Command::Start].endpoint(start))
        .branch(case![Command::Add].endpoint(add_task_start));

    let message_handler = Update::filter_message()
        .branch(command_handler)
        .branch(case![State::ReceiveTaskTitle].endpoint(receive_title))
        .branch(case![State::ReceiveTaskDueDate { title }].endpoint(receive_due_date));

    dialogue::enter::<Update, InMemStorage<State>, State, _>()
        .branch(message_handler)
}

async fn start(bot: Bot, dialogue: MyDialogue, msg: Message) -> HandlerResult {
    dialogue.update(State::Start).await?;
    bot.send_message(msg.chat.id, "Welcome!").await?;
    Ok(())
}

async fn add_task_start(bot: Bot, dialogue: MyDialogue, msg: Message) -> HandlerResult {
    dialogue.update(State::ReceiveTaskTitle).await?;
    bot.send_message(msg.chat.id, "What's the task title?").await?;
    Ok(())
}

async fn receive_title(bot: Bot, dialogue: MyDialogue, msg: Message) -> HandlerResult {
    if let Some(title) = msg.text() {
        dialogue.update(State::ReceiveTaskDueDate { title: title.into() }).await?;
        bot.send_message(msg.chat.id, "When is it due? (YYYY-MM-DD)").await?;
    }
    Ok(())
}

async fn receive_due_date(
    bot: Bot,
    dialogue: MyDialogue,
    msg: Message,
    title: String,
) -> HandlerResult {
    if let Some(due_date) = msg.text() {
        // Save to database
        bot.send_message(
            msg.chat.id,
            format!("Task '{title}' due {due_date} created!")
        ).await?;
        dialogue.update(State::Start).await?;
    }
    Ok(())
}
```

## Inline Keyboards

```rust
use teloxide::types::{InlineKeyboardButton, InlineKeyboardMarkup};

fn task_keyboard(task_id: i64) -> InlineKeyboardMarkup {
    InlineKeyboardMarkup::new(vec![
        vec![
            InlineKeyboardButton::callback("✅ Done", format!("done_{task_id}")),
            InlineKeyboardButton::callback("🗑 Delete", format!("delete_{task_id}")),
        ],
        vec![
            InlineKeyboardButton::callback("⏰ Snooze 1h", format!("snooze_{task_id}_1h")),
            InlineKeyboardButton::callback("📅 Tomorrow", format!("snooze_{task_id}_1d")),
        ],
    ])
}

// Send message with keyboard
bot.send_message(chat_id, "Task: Buy groceries")
    .reply_markup(task_keyboard(123))
    .await?;
```

## Callback Handling

```rust
async fn handle_callback(bot: Bot, q: CallbackQuery) -> HandlerResult {
    if let Some(data) = q.data {
        if data.starts_with("done_") {
            let task_id: i64 = data.strip_prefix("done_").unwrap().parse()?;
            // Mark as done in database
            bot.answer_callback_query(&q.id).await?;
            if let Some(msg) = q.message {
                bot.edit_message_text(msg.chat.id, msg.id, "✅ Task completed!").await?;
            }
        } else if data.starts_with("delete_") {
            let task_id: i64 = data.strip_prefix("delete_").unwrap().parse()?;
            // Delete from database
            bot.answer_callback_query(&q.id).await?;
            if let Some(msg) = q.message {
                bot.delete_message(msg.chat.id, msg.id).await?;
            }
        }
    }
    Ok(())
}
```

## Dispatcher Setup

```rust
#[tokio::main]
async fn main() {
    dotenvy::dotenv().ok();
    tracing_subscriber::fmt::init();

    let bot = Bot::from_env();

    Dispatcher::builder(bot, schema())
        .dependencies(dptree::deps![InMemStorage::<State>::new()])
        .enable_ctrlc_handler()
        .build()
        .dispatch()
        .await;
}
```

## With Database

```rust
#[derive(Clone)]
pub struct BotState {
    pub db: sqlx::SqlitePool,
}

async fn handle_command(
    bot: Bot,
    msg: Message,
    cmd: Command,
    state: Arc<BotState>,
) -> ResponseResult<()> {
    match cmd {
        Command::Tasks => {
            let tasks = sqlx::query_as!(
                Task,
                "SELECT * FROM tasks WHERE user_id = ?",
                msg.from().map(|u| u.id.0 as i64)
            )
            .fetch_all(&state.db)
            .await
            .unwrap_or_default();

            let text = if tasks.is_empty() {
                "No tasks".to_string()
            } else {
                tasks.iter()
                    .map(|t| format!("• {}", t.title))
                    .collect::<Vec<_>>()
                    .join("\n")
            };

            bot.send_message(msg.chat.id, text).await?;
        }
        // ...
    }
    Ok(())
}
```

## Environment Variables

```bash
# .env
TELOXIDE_TOKEN=your_bot_token
DATABASE_URL=sqlite:data.db
RUST_LOG=info
```

## Related Skills

- **sqlx** - Database for bot data
- **deployment** - Running bots in production
