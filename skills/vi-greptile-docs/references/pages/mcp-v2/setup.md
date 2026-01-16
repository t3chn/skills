# IDE Setup

URL: https://www.greptile.com/docs/mcp-v2/setup

Configure the Greptile MCP server in your IDE to access code review tools and custom context.

**Prerequisite:** Get your API key from [app.greptile.com/settings/api](https://app.greptile.com/settings/api)

## Setup by IDE

* Cursor
* Claude Code (CLI)
* VS Code

Open Settings

Click the Settings icon or press `Ctrl + Shift + J` (Windows/Linux) or `Cmd + Shift + J` (macOS).

Go to Tools & MCP

Click **Tools & MCP** in the left sidebar.

Add Custom MCP

Click **Add Custom MCP** .

Configure mcp.json

Add the following configuration:

```
{
"mcpServers": {
"greptile": {
"type": "http",
"url": "https://api.greptile.com/mcp",
"headers": {
"Authorization": "Bearer YOUR_GREPTILE_API_KEY"
}
}
}
}
```

Replace `YOUR_GREPTILE_API_KEY` with your actual API key. Save the file.

Verify Connection

Return to **Tools & MCP** . You should see Greptile with all 11 tools enabled.

Add Greptile MCP Server

Run the following command in your terminal:

```
claude mcp add --transport http greptile https://api.greptile.com/mcp \
--header "Authorization: Bearer YOUR_GREPTILE_API_KEY"
```

Replace `YOUR_GREPTILE_API_KEY` with your actual API key.

Verify Installation

Check that the server was added:

`claude mcp list`

You should see:

```
greptile: https://api.greptile.com/mcp (HTTP) - Connected
```

Start Using

Open Claude Code. The Greptile MCP tools are now available automatically.

### Project-Level Configuration

For team-shared configuration, create a `.mcp.json` file in your project root:

```
{
"servers": {
"greptile": {
"transport": "http",
"url": "https://api.greptile.com/mcp",
"headers": {
"Authorization": "Bearer ${GREPTILE_API_KEY}"
}
}
}
}
```

Then set the environment variable:

```
export GREPTILE_API_KEY=your-api-key-here
```

Open Command Palette

Press `Ctrl + Shift + P` (Windows/Linux) or `Cmd + Shift + P` (macOS).

Add MCP Server

Type `MCP` and select **MCP: Add Server** .

Select HTTP Type

Choose **HTTP (HTTP or Server-Sent-Events)** .

Enter URL

Enter: https://api.greptile.com/mcp

Select Scope

Choose **Global** or **Workspace**.

Add Authorization Header

An `mcp.json` file will be created. Add the Authorization header:

```
{
"servers": {
"greptile": {
"url": "https://api.greptile.com/mcp",
"type": "http",
"headers": {
"Authorization": "Bearer YOUR_GREPTILE_API_KEY"
}
}
}
}
```

Replace `YOUR_GREPTILE_API_KEY` with your actual API key.

Verify Installation

Run **MCP: List Servers** from Command Palette. You should see Greptile with status ** Running**.

## Verify Connection

Test your setup with curl:

```
curl -H "Authorization: Bearer YOUR_GREPTILE_API_KEY" https://api.greptile.com/mcp
```

Expected response:

```
{
"jsonrpc": "2.0",
"id": null,
"result": {
"protocolVersion": "2025-03-26",
"capabilities": {"tools": {}},
"serverInfo": {"name": "Greptile MCP Server", "version": "1.0.0"}
}
}
```

## Troubleshooting

Server shows as disconnected

**Check:**

* API key is correct and hasnt expired
* URL is exactly `https://api.greptile.com/mcp`
* Authorization header format: `Bearer YOUR_API_KEY` (with Bearer prefix)

**Fix:** Restart your IDE after making configuration changes.

Authentication failed

**Verify:**

* API key was copied without extra spaces
* Your account has access to the repositories youre querying
* API key hasnt been revoked

**Test:** Use the curl command above to verify your API key works.

No tools available

**Solutions:**

1. Restart your IDE completely
2. Check server shows Connected or Running status
3. Verify MCP is enabled in IDE settings

Tools return empty results

**Check:**

* You have repositories indexed with Greptile
* Your API key has access to those repositories
* There are actual Greptile comments on your PRs

## Configuration File Locations

| IDE | Config File |
| --- | --- |
| Claude Code | `~/.mcp.json` or project `.mcp.json` |
| Cursor | `~/.cursor/mcp.json` |
| VS Code | `~/.config/Code/User/mcp.json` (Linux) `~/Library/Application Support/Code/User/mcp.json` (macOS) |

## Next Steps
