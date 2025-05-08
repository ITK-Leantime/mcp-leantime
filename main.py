import logging
import os

from fastmcp import FastMCP
from dotenv import load_dotenv
from fastapi import HTTPException
from fastmcp.contrib.mcp_mixin import mcp_tool

from leantime.main import LeantimeClient

load_dotenv()
LEANTIME_URL = os.environ.get("LEANTIME_URL")
LEANTIME_KEY = os.environ.get("LEANTIME_KEY")

print(LEANTIME_URL)

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger("LeantimeMCP")
logger.setLevel(logging.DEBUG)

client = LeantimeClient(
    LEANTIME_URL,
    LEANTIME_KEY,
    logger
)

mcp = FastMCP(
    name="LeantimeMCP",
    prompt="""
    This is a Leantime ticket management service that allows you to retrieve information about tickets in the Leantime project management system.

    You can:
    - Retrieve a list of tickets assigned to a specific user by their user ID
    - View detailed ticket information including headlines, descriptions, due dates, statuses, and time estimates
    - Check ticket relationships with projects

    Each ticket contains rich metadata including creation dates, deadlines, priorities, planned hours, and current status.

    Use the available tools to query the Leantime system for the information you need about user assignments and ticket details.
    """
)

@mcp.tool()
async def get_tickets_assigned_to_user(user_id: int) -> dict:
    """
    Get tickets assigned to a specific user by their Leantime user ID.

    Args:
        user_id (int): The Leantime ID of the user to get assigned tickets for.

    Returns:
        list: List of ticket objects with properties including:
            - id: Ticket identifier
            - headline: Ticket title
            - description: Detailed ticket content
            - date: Creation date (YYYY-MM-DD HH:MM:SS)
            - dateToFinish: Due date (YYYY-MM-DD HH:MM:SS)
            - projectId: Associated project ID
            - projectName: Name of the project
            - type: Ticket type (e.g., "task")
            - status: Status code
            - statusLabel: Human-readable status (e.g., "Open")
            - planHours: Planned hours for the task
            - hourRemaining: Remaining hours for the task
            - and other ticket metadata

    Raises:
        HTTPException: If user_id is missing or if fetching tickets fails
    """
    if not user_id:
        raise HTTPException(status_code=400, detail="Username is required.")

    try:
        user_tickets = client.get_all_open_user_tickets(user_id=user_id)
        return user_tickets
    except Exception as e:
        logger.error(f"Failed to get tickets for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch tickets: {str(e)}")


@mcp.tool()
async def get_all_users() -> dict:
    """
    Get all users registered in the Leantime system.

    Returns:
        dict: Dictionary of user objects with properties including:
            - id: User identifier
            - username: User's login name
            - firstname: User's first name
            - lastname: User's last name
            - email: User's email address
            - role: User role in the system
            - status: Account status
            - profileId: Profile identifier
            - and other user metadata

    Raises:
        HTTPException: If fetching users fails for any reason
    """
    try:
        users = client.get_users()
        return users
    except Exception as e:
        logger.error(f"Failed to get tickets for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch tickets: {str(e)}")

@mcp.tool()
async def get_all_users_by_mail(mail: str) -> dict:
    """
    Get a user by their email address from the Leantime system.

    Args:
        mail (str): The email address to search for.

    Returns:
        dict: Dictionary containing the user with the specified email address, with properties including:
            - id: User identifier
            - username: User's login name
            - firstname: User's first name
            - lastname: User's last name
            - email: User's email address
            - role: User role in the system
            - status: Account status
            - profileId: Profile identifier
            - and other user metadata
        If no user is found with the given email, returns an empty dictionary.

    Raises:
        HTTPException: If fetching users fails for any reason
    """
    if not mail:
        raise HTTPException(status_code=400, detail="Email address is required.")

    try:
        users = client.get_users()
        for user_data in users.items():
            if user_data.get('email', '').lower() == mail.lower():
                return user_data

        # If no matching user found
        return {}
    except Exception as e:
        logger.error(f"Failed to get users: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch users: {str(e)}")

# Run the MCP server
if __name__ == "__main__":
    # This starts a Server-Sent Events (SSE) endpoint on port 8000
    mcp.run(transport="sse", host="0.0.0.0", port=9000)