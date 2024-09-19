from database import News, NewsCreate, NewsPatch
from depends import NewsCRUDService, get_news_service
from fastapi import Depends, FastAPI, status
from fastapi.responses import JSONResponse

app = FastAPI(docs_url="/api/docs")


@app.get("/api/news/", response_model=list[News])
async def get_all_news(news_service: NewsCRUDService = Depends(get_news_service)):
    news = await news_service.list_all()
    return news


@app.post("/api/news", response_model=News, status_code=status.HTTP_201_CREATED)
async def create_news(
    new_news: NewsCreate, news_service: NewsCRUDService = Depends(get_news_service)
):
    news = await news_service.create(new_news)
    return news


@app.get("/api/news/{news_id}", response_model=News)
async def get_news(
    news_id: str, news_service: NewsCRUDService = Depends(get_news_service)
):
    news = await news_service.get_news(news_id)
    return news


@app.delete("/api/news/{news_id}")
async def delete_news(
    news_id: str, news_service: NewsCRUDService = Depends(get_news_service)
):
    await news_service.delete(news_id)
    return JSONResponse({"status": "ok"})


@app.patch("/api/news/{news_id}", response_model=News)
async def update_news(
    news_id: str,
    news_body: NewsPatch,
    news_service: NewsCRUDService = Depends(get_news_service),
):
    updated_news = await news_service.patch(news_id, news_body)
    return updated_news
