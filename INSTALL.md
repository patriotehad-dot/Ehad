# Installation Guide for iTerm2 MCP Server 🐒

This guide provides the steps to set up the iTerm2 MCP Server for use with an MCP client like Claude Desktop.

## Prerequisites

1.  **macOS**: iTerm2 is macOS-only.
2.  **Homebrew**: A package manager for macOS, used to install `ripgrep`. You can install it from [brew.sh](https://brew.sh/).
3.  **iTerm2**: The latest version, downloadable from [iterm2.com](https://iterm2.com/).
4.  **Python 3.8+**: macOS includes a compatible version of Python by default.
5.  **`ripgrep`**: A system dependency for the `search_code` tool.

## Step 1: Install Ripgrep

Open your terminal and use Homebrew to install `ripgrep`:
```bash
brew install ripgrep
```

## Step 2: Download the Server

Download or clone this repository to a permanent location on your computer (e.g., `~/Documents/coder`). You will need the absolute path to `iterm2_mcp_server.py` for the final step.

## Step 3: Configure iTerm2

You must grant permission for external scripts to control iTerm2. This is a one-time setup step inside iTerm2 itself.

1.  Open iTerm2.
2.  Go to the menu bar and select **Scripts** → **Manage** → **Install Python Runtime**.
3.  Click **Install** if the runtime is not already present.
4.  Go to **Scripts** → **Manage** → **AutoLaunch**.
5.  Ensure the checkbox for **"Allow all apps to connect to iTerm2"** is enabled.

## Step 4: Configure Your MCP Client (Claude Desktop)

1.  Find the absolute path to the `iterm2_mcp_server.py` script you downloaded. You can do this by navigating to the directory in your terminal and running `pwd`.
2.  Open your MCP client's configuration file (e.g., `claude_desktop_config.json`).
3.  Add the following JSON object to the `mcpServers` section.

**Important:** Replace `/path/to/your/coder/iterm2_mcp_server.py` with the real absolute path you found in the previous step.

```json
"iterm2": {
  "command": "uvx",
  "args": [
    "--with", "mcp",
    "--with", "iterm2", 
    "python",
    "/path/to/your/coder/iterm2_mcp_server.py"
  ]
}
```

Setup is now complete. The client will automatically start the server when needed.

## Troubleshooting

-   **"Failed to connect to iTerm2"**: Make sure iTerm2 is running and you have completed Step 3 correctly.
-   **`search_code` tool fails**: This likely means `ripgrep` is not installed correctly. Run `brew install ripgrep` again.

---

*Need help? Check the README.md or open an issue! 🐒* 