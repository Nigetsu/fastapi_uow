import uvicorn

if __name__ == '__main__':
    uvicorn.run(app='src.main:app', port=8000, reload=True)
