from fastapi import FastAPI
from starlette.responses import RedirectResponse
import uvicorn

app= FastAPI()


job= {'name': 'vaibhav',
      'age': 30,
      'location': 'Hyderabad'}

@app.get("/")
async def root():
    
    return RedirectResponse(url="/docs")



# @app.get("/hello/{name}")
# async def root(name):
    
#     return job.get(name)


if __name__ == '__main__':  #it will run progm on only this page other import will restrict
    
    uvicorn.run(app, host='0.0.0.0', port=8080)