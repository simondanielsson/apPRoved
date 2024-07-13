"""Launch the API locally."""

import argparse

import uvicorn

from api.utils.log import read_logging_config


def main() -> None:
    """Trigger main function of the API."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Activate debug mode",
    )
    args = parser.parse_args()

    uvicorn.run(
        "api.api:api",
        host="localhost",
        port=8080,
        reload=args.debug,
        access_log=True,
        log_config=read_logging_config(),
    )


if __name__ == "__main__":
    """Trigger main function."""
    main()
