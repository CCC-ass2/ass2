from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import JSONResponse

from backup_page3.covid_analysis import get_df as p3get_df
from backup_page2.emoji_find import get_df as p2get_df
from backup_page1.unemployment_rate_4_greaterCity import get_df as p1get_df


app = FastAPI()

@app.get("/page1data")
def get_page1data():
    return p1get_df()


@app.get("/page2data")
def get_page2data():
    return p2get_df()


@app.get("/page3data")
def get_page3data():
    return p3get_df()


class ServiceNotFound(Exception):
    def __init__(self, name: str = "未找到服务项目"):
        self.name = name


@app.exception_handler(ServiceNotFound)
async def service_not_found_handler(request: Request, exc: ServiceNotFound):
    return JSONResponse(status_code=404, content={"message": exc.name})


def run():
    import uvicorn
    uvicorn.run('main:app', host='0.0.0.0', port=8000)


if __name__ == '__main__':
    run()
