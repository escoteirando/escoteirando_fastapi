from src import app

app.noauth_route("/api/hc")


@app.get("/api/hc", status_code=200, summary="Health Check validation")
def get_healthcheck():
    return "OK"
