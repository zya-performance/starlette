from starlette.applications import Starlette
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import JSONResponse
from starlette.testclient import TestClient

app = Starlette()
app.add_middleware(SessionMiddleware, secret_key="example")


@app.route("/view_session")
def view_session(request):
    return JSONResponse({"session": request.session})


@app.route("/update_session", methods=["POST"])
async def update_session(request):
    data = await request.json()
    request.session.update(data)
    return JSONResponse({"session": request.session})


@app.route("/clear_session", methods=["POST"])
async def clear_session(request):
    request.session.clear()
    return JSONResponse({"session": request.session})


def test_session():
    client = TestClient(app)

    response = client.get("/view_session")
    assert response.json() == {"session": {}}

    response = client.post("/update_session", json={"some": "data"})
    assert response.json() == {"session": {"some": "data"}}

    response = client.get("/view_session")
    assert response.json() == {"session": {"some": "data"}}

    response = client.post("/clear_session")
    assert response.json() == {"session": {}}

    response = client.get("/view_session")
    assert response.json() == {"session": {}}
