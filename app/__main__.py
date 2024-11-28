import asyncio
import logging
from fastapi import BackgroundTasks
import uvicorn

from app.settings import SETTINGS


async def main():

    uvicorn.run(
        app="app.api.server:app",
        host=SETTINGS.API_HOST,
        port=SETTINGS.API_PORT,
        log_level=SETTINGS.LOGGING_LEVEL.lower(),
        reload=True,
        reload_includes=["app"],
    )


if __name__ == "__main__":
    logging.warning("Starting bot")
    loop = asyncio.new_event_loop()
    loop.create_task(main())
    loop.run_forever()
    logging.warning("Bot stopped")
