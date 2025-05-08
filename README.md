# MCP Leantime Client

A proof-of-concept FastMCP server that provides a convenient AI-powered interface to the Leantime project management
system.

## Overview

This project implements a Model Control Protocol (MCP) server that connects to Leantime's API, allowing AI assistants to
interact with Leantime ticket and user data. It uses the FastMCP framework to expose Leantime functionality through a
set of well-defined tools.

## Features

- Get tickets assigned to specific users
- Retrieve all registered Leantime users
- Look up users by email address
- Clean data formatting for easy consumption by AI assistants

## Requirements

- Python 3.11+
- Leantime instance with API access
- Leantime API key

## Setup

1. Clone the repository
2. Install dependencies:
   ```
   pip install -e .
   ```
3. Create a `.env` file in the project root with the following variables:
   ```
   LEANTIME_URL=https://your-leantime-instance.com
   LEANTIME_KEY=lt_YOUR_API_KEY
   ```

## Usage

Start the MCP server:

```bash
python main.py
```