from fastapi import status
from fastapi.responses import RedirectResponse

from src.controllers import import_controllers
if not import_controllers():
    print("ERROR WHEN LOADING CONTROLLERS")
    exit()

import uvicorn
from src import app


@app.get("/")
def read_root():
    """ Static Root """
    return RedirectResponse(
        "/f",
        status_code=status.HTTP_301_MOVED_PERMANENTLY)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
