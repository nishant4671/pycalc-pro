from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from calculator import PyCalc

app = FastAPI()
calc = PyCalc()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def web_interface(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "result": None,
            "history": calc.history[-5:]
        }
    )

@app.get("/calculate", response_class=HTMLResponse)
async def calculate(request: Request, expression: str):
    result = calc.calculate(expression)
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "result": result,
            "history": calc.history[-5:]
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)