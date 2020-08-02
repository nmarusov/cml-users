import uvicorn
from fastapi import FastAPI, Path
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from models import UserList

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.get("/all", response_model=UserList)
async def get_all_users():
    """Получить список всех пользователей."""
    return {
        "users": [
            {"name": "Тимофей Иванов", "id": 113},
            {"name": "Andrey Kuznetsov", "id": 112},
            {"name": "Сергей Барашков", "id": 106},
            {"name": "АО ОКБМ АФРИКАНТОВ", "id": 100},
            {"name": "Тимофей Грошев", "id": 107},
            {"name": "Dmytro Miroshnychenko", "id": 105},
            {"name": "Petr Skopin", "id": 104},
            {"name": "tvel1", "id": 110},
            {"name": "Рафаэль Даутов", "id": 103},
            {"name": "Михаил Гусев", "id": 114},
            {"name": "Leonid Laboshin", "id": 108},
            {"name": "tvel2", "id": 111},
        ],
        "count": 12,
    }


@app.get("/substituted/{user_id}", response_model=UserList)
async def get_substituted_users(
    user_id: int = Path(..., description="Идентификатор пользователя", ge=1)
):
    """Получить список пользователей, чьи обязанности исполняет указанный пользователь."""
    return {
        "users": [
            {
                "name": "Leonid Laboshin",
                "date_start": "2020-07-19",
                "date_finish": "2020-08-29",
                "id": 108,
            },
            {
                "name": "Dmytro Miroshnychenko",
                "date_start": "2020-07-19",
                "date_finish": "2020-08-29",
                "id": 105,
            },
        ],
        "count": 2,
    }


@app.get("/deputies/{user_id}", response_model=UserList)
async def get_deputies(
    user_id: int = Path(..., description="Идентификатор пользователя", ge=1)
):
    """Получить список пользователей, выполняющих обязанности указанного пользователя."""
    return {
        "users": [
            {
                "name": "Тимофей Иванов",
                "date_start": "2020-07-19",
                "date_finish": "2020-08-29",
                "id": 113,
            },
            {
                "name": "Petr Skopin",
                "date_start": "2020-07-19",
                "date_finish": "2020-08-29",
                "id": 104,
            },
            {
                "name": "Рафаэль Даутов",
                "date_start": "2020-07-19",
                "date_finish": "2020-08-29",
                "id": 103,
            },
        ],
        "count": 3,
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=1402)
