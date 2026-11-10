
# INF601 - Advanced Programming in Python
# Adeola Ajayi
# Mini Project 7 - MCP Server

import os
import httpx
from mcp.server.fastmcp import FastMCP

BASE = os.environ["PRACTICE_API_URL"].rstrip("/")
TOKEN = os.environ["PRACTICE_API_TOKEN"]

mcp = FastMCP("practice-hub")


@mcp.tool()
def list_posts(mine: bool = False) -> dict:
    """List Practice Hub posts. Set mine=True to see only your own posts."""
    try:
        response = httpx.get(
            f"{BASE}/api/v1/posts",
            params={"mine": str(mine).lower()},
            headers={"Authorization": f"Bearer {TOKEN}"},
            timeout=15.0,
        )
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as exc:
        return {
            "error": f"API returned HTTP {exc.response.status_code}"
        }
    except httpx.RequestError as exc:
        return {"error": f"Connection failed: {exc}"}


@mcp.tool()
def get_post(post_id: int) -> dict:
    """Retrieve a Practice Hub post by its ID."""
    try:
        response = httpx.get(
            f"{BASE}/api/v1/posts/{post_id}",
            headers={"Authorization": f"Bearer {TOKEN}"},
            timeout=15.0,
        )
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as exc:
        return {"error": f"HTTP {exc.response.status_code}: {exc.response.text}"}
    except httpx.RequestError as exc:
        return {"error": f"Connection failed: {exc}"}


@mcp.tool()
def create_post(title: str, body: str, tags: list[str]) -> dict:
    """Create a new Practice Hub post with a title, body, and tags."""
    try:
        response = httpx.post(
            f"{BASE}/api/v1/posts",
            json={"title": title, "body": body, "tags": tags},
            headers={"Authorization": f"Bearer {TOKEN}"},
            timeout=15.0,
        )
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as exc:
        return {"error": f"HTTP {exc.response.status_code}: {exc.response.text}"}
    except httpx.RequestError as exc:
        return {"error": f"Connection failed: {exc}"}


@mcp.tool()
def update_post(post_id: int, title: str, body: str) -> dict:
    """Update the title and body of one of your own Practice Hub posts."""
    try:
        response = httpx.patch(
            f"{BASE}/api/v1/posts/{post_id}",
            json={"title": title, "body": body},
            headers={"Authorization": f"Bearer {TOKEN}"},
            timeout=15.0,
        )
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as exc:
        return {"error": f"HTTP {exc.response.status_code}: {exc.response.text}"}
    except httpx.RequestError as exc:
        return {"error": f"Connection failed: {exc}"}


@mcp.tool()
def delete_post(post_id: int) -> dict:
    """Delete one of your own Practice Hub posts by its ID."""
    try:
        response = httpx.delete(
            f"{BASE}/api/v1/posts/{post_id}",
            headers={"Authorization": f"Bearer {TOKEN}"},
            timeout=15.0,
        )
        response.raise_for_status()
        return {"success": True, "message": "Post deleted successfully"}
    except httpx.HTTPStatusError as exc:
        return {"error": f"HTTP {exc.response.status_code}: {exc.response.text}"}
    except httpx.RequestError as exc:
        return {"error": f"Connection failed: {exc}"}


if __name__ == "__main__":
    mcp.run()
