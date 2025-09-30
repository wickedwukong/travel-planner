"""A simple hello world module."""


def hello_world() -> str:
    """Return a greeting message.

    Returns:
        str: The greeting "Hello, World!"
    """
    return "Hello, World!"


if __name__ == "__main__":
    print(hello_world())  # noqa: T201
