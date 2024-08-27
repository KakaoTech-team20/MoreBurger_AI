# FastAPI에서는 의존성을 함수로 생성할 수 있으며, 이를 통해 다른 경로 작업에서 재사용할 수 있습니다. 의존성은 일반적으로 데이터베이스 연결, 보안 검증, 구성 설정 등의 공통 작업을 처리하는 데 사용됩니다.

# 예시
from typing import Optional

from fastapi import Depends, FastAPI

app = FastAPI()

def common_parameters(q: Optional[str] = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    response = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}], **commons}
    return response

@app.get("/users/")
async def read_users(commons: dict = Depends(common_parameters)):
    response = {"users": [{"user_id": "Alice"}, {"user_id": "Bob"}], **commons}
    return response

# 의존성을 사용하는 이유
# 의존성을 사용하면 코드를 더 깔끔하게 유지할 수 있고, 중복을 줄이며, 비즈니스 로직과 인증, 데이터베이스 세션 관리 등을 분리할 수 있습니다.
# 이는 유지보수를 쉽게 하고, 오류 가능성을 줄이며, 코드의 가독성을 향상시킵니다.
#
# 위의 예제와 같이 의존성을 설정하면, FastAPI가 요청을 처리할 때마다 필요한 값을 자동으로 계산하고, 결과를 경로 작업 함수의 파라미터로 전달합니다.
# 이 방식은 코드를 더 모듈화하고 테스트하기 쉽게 만들어 줍니다.
#
# FastAPI의 의존성 시스템은 매우 강력하며, 다양한 상황에서 유연하게 사용될 수 있습니다.
