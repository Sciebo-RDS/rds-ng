def format_database_url(
    host: str, port: int, database: str, user: str, password: str
) -> str:
    """
    Formats a proper database URL, raising runtime errors in case of any errors.

    Args:
        host: The host of the database.
        port: The port of the database; if 0, it will be omitted.
        database: The database name.
        user: The username.
        password: The user password.

    Returns:
        The formatted database URL.
    """
    if user == "" or password == "":
        raise RuntimeError("No user credentials provided")
    if database == "":
        raise RuntimeError("No database name provided")

    url = f"{user}:{password}@{host}"
    if port != 0:
        url += f":{port}"
    url += f"/{database}"
    return url
