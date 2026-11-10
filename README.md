# INF601 Mini Project 7 – Practice Hub MCP Server

**Course:** INF601 – Advanced Programming in Python
**Author:** Adeola Ajayi

## Overview

This project is a Python [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server built with **FastMCP**. It connects an AI assistant (Claude Code) to the course **Practice Hub REST API**. With the server connected, the assistant can list, read, create, update, and delete Practice Hub posts by calling MCP tools.

The server runs locally over **stdio**. Claude Code starts it as a subprocess and talks to it through the MCP protocol. Each tool sends an authenticated HTTP request to the Practice Hub API with `httpx`.

```
Claude Code  ──(MCP over stdio)──▶  server.py (FastMCP)  ──(HTTPS + Bearer token)──▶  Practice Hub API
```

## Project Structure

| File | Purpose |
|---|---|
| `server.py` | FastMCP server that defines the five Practice Hub tools |
| `requirements.txt` | Pinned Python dependencies |
| `.gitignore` | Excludes the virtual environment, bytecode, and `.env` files |
| `README.md` | Project documentation |

## Practice Hub API Integration

The server reads two environment variables at startup:

| Variable | Description |
|---|---|
| `PRACTICE_API_URL` | Base URL of the Practice Hub API (a trailing slash is removed automatically) |
| `PRACTICE_API_TOKEN` | Your personal Practice Hub API token |

Every request sends the token in an `Authorization: Bearer <token>` header and has a 15-second timeout. The endpoints used are:

| Tool | HTTP method | Endpoint |
|---|---|---|
| `list_posts` | `GET` | `/api/v1/posts?mine=<true|false>` |
| `get_post` | `GET` | `/api/v1/posts/{post_id}` |
| `create_post` | `POST` | `/api/v1/posts` |
| `update_post` | `PATCH` | `/api/v1/posts/{post_id}` |
| `delete_post` | `DELETE` | `/api/v1/posts/{post_id}` |

**Error handling:** none of the tools raise an exception back to the client. An HTTP error status, such as `404` or `401`, is returned as `{"error": "..."}` with the status code. `get_post`, `create_post`, `update_post`, and `delete_post` also include the API's response body in that message. A network failure is returned as `{"error": "Connection failed: ..."}`.

## MCP Tools

### `list_posts(mine: bool = False)`
Lists Practice Hub posts. With `mine=False` (the default) it returns all posts. With `mine=True` it returns only posts written by the account that owns the API token.

### `get_post(post_id: int)`
Returns one post by ID, including its title, body, tags, author, timestamps, and attachments. If no post has that ID, it returns an error such as `HTTP 404: {"detail":"Post not found."}`.

### `create_post(title: str, body: str, tags: list[str])`
Creates a new post under your account and returns the post the API created, including its new `id`.

### `update_post(post_id: int, title: str, body: str)`
Updates the title and body of one of your own posts. Both fields are required, so to change only the title, pass the existing body back unchanged. Tags are not sent, so they keep their current values.

### `delete_post(post_id: int)`
Deletes one of your own posts. On success it returns `{"success": true, "message": "Post deleted successfully"}`.

## Setup

### Requirements
- Python 3.13 (developed with 3.13.15)
- A Practice Hub account and API token
- [Claude Code](https://docs.claude.com/en/docs/claude-code)

### Dependencies
The main libraries are:
- **`mcp`** (1.30.0): the MCP Python SDK, which provides `FastMCP`
- **`httpx`** (0.28.1): the HTTP client used to call the Practice Hub API

The other packages in `requirements.txt` are their dependencies, pinned for reproducibility.

### Installation

```bash
git clone https://github.com/Bucey01/miniproject7AdeolaAjayi.git
cd miniproject7AdeolaAjayi

python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Environment variables
Keep your token out of source control. `.gitignore` already excludes `.env` files. Give the values to Claude Code when you register the server (see below), or export them in your shell for local testing:

```bash
export PRACTICE_API_URL="<practice-hub-base-url>"
export PRACTICE_API_TOKEN="<your-api-token>"
```

## Connecting the Server to Claude Code

From the project root, register the server with Claude Code. Use absolute paths to the virtual environment's Python interpreter and to `server.py`:

```bash
claude mcp add practice-hub \
  --env PRACTICE_API_URL="<practice-hub-base-url>" \
  --env PRACTICE_API_TOKEN="<your-api-token>" \
  -- "$(pwd)/.venv/bin/python" "$(pwd)/server.py"
```

Then, inside Claude Code:

1. Run `/mcp` and confirm that **practice-hub** is connected.
2. Ask Claude to use the tools, for example: *"Using the practice-hub MCP server, call list_posts with mine=true."*
3. After you edit `server.py`, run `/mcp`, select **practice-hub**, and choose **Reconnect** so Claude Code loads the new tool definitions.

## Testing

All five tools were tested through Claude Code on **November 10, 2026** against the live Practice Hub API.

| # | Tool | Call | Result |
|---|---|---|---|
| 1 | `list_posts` | `mine=true` | ✅ Returned an empty list. The account had no posts yet. |
| 2 | `list_posts` | `mine=false` | ✅ Returned 42 posts: instructor posts (check-ins, syllabus, Week 5 Pandas notes, lab info), student posts, and seed posts |
| 3 | `create_post` | title `Mini Project 7 MCP Test`, tags `mcp, python, inf601` | ✅ Created **post ID 47**, authored by account ID 11 |
| 4 | `get_post` | `post_id=47` | ✅ Returned post 47 with the title, body, and tags that were sent |
| 5 | `update_post` | `post_id=47`, title `Mini Project 7 MCP Test - Updated`, same body | ✅ Title changed. The body and tags stayed the same, and `updated_at` advanced. |
| 6 | `delete_post` | `post_id=47` | ✅ Returned `{"success": true, "message": "Post deleted successfully"}` |
| 7 | `get_post` | `post_id=47` (after the delete) | ✅ Returned `HTTP 404: {"detail":"Post not found."}`, which confirms the delete |

### Issue found and fixed during testing
At first, Claude Code could see only `list_posts`. The `if __name__ == "__main__": mcp.run()` block came right after `list_posts` in `server.py`. `mcp.run()` blocks while the server runs, so the four tools defined below it were never registered. Moving the block to the end of the file fixed this, and the server now registers all five tools. After that change, the server was reconnected in Claude Code with `/mcp`.

## AI Usage

### AI Tools Used

I used Claude Code and ChatGPT to assist with developing, troubleshooting, testing, and documenting this project. I reviewed their output and verified the test results.

- **Claude Code:** Ran the MCP tool calls against the Practice Hub API, identified and fixed the misplaced `mcp.run()` block, and drafted the initial README from the project files and test session.

- **ChatGPT:** Assisted with understanding the assignment, structuring the FastMCP server and `httpx` API calls, and troubleshooting setup issues.

### Changes Made to AI-Generated Code

During testing, the server initially exposed only `list_posts`. Claude Code identified that the `mcp.run()` startup block was placed before the other four tool definitions in `server.py`. Claude Code moved the startup block to the end of the file so all five tools would register before the server started.

I reconnected the server through `/mcp` and verified that all five tools were available. I also reviewed the generated README and expanded its AI Usage documentation to explain the assistance, changes, and my contributions.

### My Contributions

My hands-on work included:

- Setting up the project directory and Python virtual environment on my MacBook.
- Installing the required Python dependencies.
- Configuring the Practice Hub API environment variables.
- Registering the MCP server with Claude Code.
- Running terminal commands to verify the server connection.
- Directing Claude Code to test the five required MCP tools.
- Reviewing the API results and confirming that the operations worked.
- Creating the GitHub repository and preparing the project files for submission.

### Testing and Verification

I used Claude Code to test `list_posts`, `create_post`, `get_post`, `update_post`, and `delete_post` through the MCP server. The test created post ID 47, retrieved it, updated its title, and deleted it. A subsequent `get_post` request returned HTTP 404, confirming that the deleted post was no longer available. Detailed results are recorded in the **Testing** section above.

## Security Notes

- No API tokens or credentials are stored in this repository.
- Tokens come only from environment variables. `.env` files are listed in `.gitignore`.
