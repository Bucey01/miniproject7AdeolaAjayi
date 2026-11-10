# INF601 Mini Project 7 — MCP Acceptance Test Transcript

**Test date:** November 10, 2026  
**Client:** Claude Code 2.1.294  
**MCP server:** `practice-hub` (Python FastMCP, stdio)  
**API:** Practice Hub REST API

> This is a reconstructed, abbreviated transcript of the Claude Code commands and results captured during testing. It is not a verbatim terminal export. No credentials are included.

## 1. Connect and list posts

**Request:** Using the `practice-hub` MCP server, call `list_posts` with `mine=true`.

**Result:** The tool returned an empty list, with no error. At that time, the authenticated account had no posts.

**Request:** Call `list_posts` with `mine=false`.

**Result:** The tool returned 42 posts, including course and student posts.

## 2. Create a post

**Request:** Call `create_post` with:

- **Title:** Mini Project 7 MCP Test
- **Body:** This post was created using Claude Code through my Python FastMCP server for INF601 Mini Project 7.
- **Tags:** `mcp`, `python`, `inf601`

**Result:** Claude Code reported that the API successfully created **post ID 47** under author account ID 11, without errors.

## 3. Read the created post

**Request:** Call `get_post` with `post_id=47`.

**Result:** The tool returned post 47, matching the submitted title, body, and tags. The reported creation time was `2026-11-10 21:37:49`.

## 4. Update the post

**Request:** Call `update_post` on post 47, changing the title to **Mini Project 7 MCP Test - Updated**, while preserving the existing body.

**Result:** The tool reported that post 47 was updated. The title changed; the body and tags remained unchanged. The reported update time was `2026-11-10 21:40:18`.

## 5. Delete and verify

**Request:** Call `delete_post` with `post_id=47`.

**Result:** Claude Code reported:

```json
{"success": true, "message": "Post deleted successfully"}
```

**Verification:** A subsequent `get_post(post_id=47)` returned HTTP 404, with the message `Post not found.` This confirmed that the test post had been deleted.

## Outcome

All five required MCP tools were exercised through Claude Code:

| Tool | Observed result |
|---|---|
| `list_posts` | Successfully listed own posts and all posts |
| `create_post` | Created post 47 |
| `get_post` | Retrieved post 47; returned 404 after deletion |
| `update_post` | Updated the title of post 47 |
| `delete_post` | Deleted post 47 |

## Troubleshooting note

Initially, Claude Code exposed only `list_posts` because the `mcp.run()` startup block appeared before the remaining tool definitions in `server.py`. Claude Code moved the startup block to the end of the file. After reconnecting `practice-hub` using `/mcp`, all five tools were available and the acceptance tests above succeeded.

## AI Usage

Claude Code performed the MCP tool calls and reported their results. This document summarizes the test requests and responses shown in the Claude Code session.
