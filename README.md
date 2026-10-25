# iTerm2 MCP Server AI Coding Agent 🐒

A Model Context Protocol (MCP) server that transforms iTerm2 into a powerful AI coding agent. It provides a structured toolkit for agents to interact with the terminal, manipulate the filesystem, and search code with precision.

This server is designed to be the bridge between a large language model's reasoning capabilities and the practical, hands-on tasks of software development.

## Core Capabilities

-   🧠 **Code Intelligence:** Perform structured, gitignore-aware code searches using `ripgrep`. Instead of parsing `grep` output, the agent receives clean JSON with file paths, line numbers, and matching content.
-   📂 **Precise Filesystem I/O:** Read, write, and perform surgical line-based edits on files. This avoids the ambiguity of `sed` or `echo` and allows the agent to safely manipulate code.
-   🖥️ **Full Terminal Control:** Create tabs, split panes, run commands, and read screen output. The agent has a visible, interactive workspace within iTerm2.
-   ⭐ **Shell Integration Support:** Enhanced command execution with prompt monitoring, accurate exit codes, and access to shell variables (requires Shell Integration).
-   🤖 **Structured JSON API:** All tools return predictable JSON objects, making it easy for an agent to parse success/failure states and data without guessing.
-   🛡️ **Safety Features:** Automatic detection and handling of complex quoting, heredoc prevention, and unicode/emoji handling to prevent terminal state corruption.

## Installation

A complete step-by-step guide is available in [`INSTALL.md`](./INSTALL.md). The user-focused setup is:

1.  **Install Prerequisites:**
    You will need [Homebrew](https://brew.sh/) to install `ripgrep`.
    ```bash
    # Install ripgrep for the search_code tool
    brew install ripgrep
    ```

2.  **Download the Server:**
    Download or clone this repository to a permanent location on your computer.

3.  **Configure iTerm2:**
    - Open iTerm2.
    - Go to `Scripts > Manage > Install Python Runtime`.
    - Go to `Scripts > Manage > AutoLaunch` and ensure "Allow all apps to connect to iTerm2" is enabled.

4.  **Optional: Install Shell Integration (Recommended):**
    Shell Integration enables advanced features like prompt monitoring and session variables.
    ```bash
    curl -L https://iterm2.com/shell_integration/install_shell_integration_and_utilities.sh | bash
    ```
    Or visit: https://iterm2.com/documentation-shell-integration.html

## Usage

This server is designed to be run automatically by an MCP client, such as the Claude Desktop app.

Add the following configuration to your client's settings. **You must replace `/path/to/your/coder/iterm2_mcp_server.py` with the actual, absolute path** to the file you downloaded.

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

That's it. The MCP client will now handle starting the server for you.

## Safety Features

The server uses **Smart Command Execution** with automatic complexity detection:

### Smart Command Execution
- **Simple commands** (`ls`, `pwd`, `git status`) execute directly for speed
- **Complex commands** (with quotes, pipes, unicode, subshells) use temporary script files
- Scripts are written to `/tmp/mcp_cmd_*.sh`, executed, then auto-delete themselves
- This completely avoids quote interpretation issues that plague terminal automation
- **Automatic detection**: You don't need to choose - the tool detects complexity automatically
- Supports **heredocs, emojis, complex quoting, and long commands** without any special handling

### What This Means for Agents
- ✅ **Heredocs are fully supported**: Use them freely for multi-line file creation or scripts
- ✅ **Emojis are fully supported**: Unicode characters in commands work reliably
- ✅ **No length limits**: Long commands don't cause buffer issues
- ✅ **Complex quoting works**: Single quotes, double quotes, backticks - all safe
- ✅ **Readable execution**: Commands appear in the terminal exactly as written

### Output Reading Improvements & Limitations
- **`isolate_output=True` is RECOMMENDED**: This mode wraps commands with unique markers and extracts only the command's output, filtering out prompts and terminal noise
- **Active polling for completion**: When using `isolate_output`, the tool actively waits for the command to finish (detecting the END marker) before returning results
- **Longer timeouts for long tasks**: Increase the `timeout` parameter for commands like ffmpeg, large compilations, etc.
- **✅ Full Scrollback Support**: The tool uses `async_get_contents()` with `async_get_line_info()` to read output including scrollback history, not just the visible screen. This means commands with long output (100s of lines) are fully captured when using `isolate_output=True`.
- **Latest-run marker targeting**: Each isolated command uses a unique UUID marker and the reader matches the exact marker pair, so stale scrollback from previous runs can’t confuse the extractor.
- **⚠️ iTerm2 Scrollback Setting**: For best results with long-running commands, set iTerm2's scrollback to "Unlimited". Go to **Settings → Profiles → Terminal → Scrollback Lines** and select "Unlimited scrollback". This ensures all command output is preserved in the scrollback buffer and can be fully captured by the tool.

### Best Practices
- **Use `isolate_output=True` for clean results**: Especially important for commands with verbose output or when parsing results
- **Try `run_command_monitored` for critical commands**: If Shell Integration is installed, it provides better completion detection and exit codes
- **Check Shell Integration with `check_shell_integration`**: Know what features are available before using them
- **Use `get_session_variables` for context**: Get current directory, git branch, etc. without running commands
- **Still prefer specialized tools**: `write_file`, `read_file`, `edit_file` are safer and more reliable for file operations
- **Use heredocs wisely**: While supported, `write_file` is clearer for creating files

## Shell Integration Benefits

When [Shell Integration](https://iterm2.com/documentation-shell-integration.html) is installed, you gain:

- **Accurate command completion detection** - Know exactly when commands finish
- **Exit code retrieval** - Get actual exit codes from shell, not guessed
- **Session context variables** - Access current directory, git branch, running jobs without commands
- **Prompt monitoring** - Detect command start/end events reliably
- **Better reliability** - No more polling or sleep-based waiting for commands

**Check if installed**: Run `check_shell_integration` tool

**Graceful degradation**: All tools work without Shell Integration, but enhanced features (`run_command_monitored`, `get_session_variables`) require it.

## Tool Reference

The following tools are available through the MCP server.

### Terminal Control

| Tool | Parameters | Description |
| :--- | :--- | :--- |
| `run_command` | `command: str`, `wait_for_output: bool = True`, `timeout: int = 10`, `require_confirmation: bool = False`, `working_directory: str = None`, `isolate_output: bool = False`, `max_output_chars: int = 10000` | Executes shell commands with automatic complexity detection. Simple commands run directly; complex commands (quotes, pipes, unicode) use temp scripts. **Fully supports heredocs, emojis, and complex quoting**. For clean output parsing, use `isolate_output=True` and adjust `timeout` based on command duration (ffmpeg: 120-300s, builds: 300-600s). |
| `run_command_monitored` | `command: str`, `timeout: int = 30`, `require_confirmation: bool = False`, `working_directory: str = None` | ⭐ **Enhanced execution** using Prompt Monitor for reliable completion detection and accurate exit codes. **Requires Shell Integration**. Use for long-running commands or when exit codes are critical. Automatically falls back to `run_command` if Shell Integration unavailable. |
| `check_shell_integration` | | Checks if Shell Integration is installed and available. Returns status and lists features available. |
| `get_session_variables` | `variable_names: list = None` | ⭐ Retrieves shell variables exposed by Shell Integration (current directory, job name, git branch, etc.). **Requires Shell Integration**. Get context without running commands. |
| `read_terminal_output` | `timeout: int = 5` | Reads the entire visible contents of the active iTerm2 screen. |
| `send_text` | `text: str`, `paste: bool = True` | Sends text to the terminal. By default uses async_inject for safe insertion. Set `paste=False` to simulate individual keystrokes (slower, riskier). |
| `create_tab` | `profile: str = None` | Creates a new tab in the current iTerm2 window. |
| `create_session` | `profile: str = None` | Creates a new session (split pane) in the current tab. |
| `clear_screen` | | Clears the screen of the active session (like `Ctrl+L`). |
| `list_profiles` | | Retrieves a list of all available iTerm2 profiles. |
| `switch_profile` | `profile: str` | Switches the profile of the current iTerm2 session. |
| `get_session_info` | | Gets information about the current window, tab, and session IDs. |

### Filesystem I/O

| Tool | Parameters | Description |
| :--- | :--- | :--- |
| `read_file` | `file_path: str`, `start_line: int = None`, `end_line: int = None` | Reads a file, with options to specify a range of line numbers. |
| `write_file` | `file_path: str`, `content: str` | Writes content to a file, overwriting it if it exists or creating it if it doesn't. |
| `edit_file` | `file_path: str`, `start_line: int`, `end_line: int`, `new_content: str` | Replaces a specific block of lines in a file with new content. |
| `list_directory` | `path: str`, `recursive: bool = False` | Lists the contents of a directory, returning a structured list of files and subdirectories. |

### Code Intelligence

| Tool | Parameters | Description |
| :--- | :--- | :--- |
| `search_code` | `query: str`, `path: str = "."`, `case_sensitive: bool = True` | Searches for a string/regex in files using `ripgrep` and returns structured results (file, line number, content). |

---

*Made with 🐒 by your favorite coding monkey assistant* 
