# 응답에 필요한 기능들 정의해서 routers에서 사용할 수 있도록 구현하는 파일
# OpenAI API 호출과 관련된 기능을 정의하여 라우터에서 사용할 수 있도록 하는 역할
import os

# import openai
from openai import OpenAI

from dotenv import load_dotenv

# # 환경 변수 로드
load_dotenv()

# OpenAI API 키 설정
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))



# 벡터 스토어에서 기존 Assistant 불러오기
def retrieve_assistant():
    try:
        # 벡터 스토어에서 기존 Assistant 불러오기
        vector_store = client.beta.vector_stores.retrieve("vs_wZWpgYaxPipa8tByxs2DSDNk")

        # 기존 assistant를 업데이트 하는 코드
        assistant = client.beta.assistants.retrieve("asst_JR7zBXnLYraebcyRmKXrKU1o")
        return vector_store, assistant

    except Exception as e:
        return f"Error retrieving assistant: {str(e)}"

def start_conversation_with_assistant(assistant):
    try:
        # 새로운 대화 스레드 생성
        thread = client.beta.threads.create(
            messages=[
                {
                    "role": "user",
                    "content": "'무엇을 도와드릴까요?' 라고만 말해",
                }
            ]
        )

        # assistant와 대화 실행
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id
        )

        # 대화가 완료될 때까지 상태 확인
        while run.status != "completed":
            run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            print(run.status)
            print(run.completed_at)

            # 대화 완료 후 챗봇 메시지를 출력
            message = client.beta.threads.messages.list(thread_id=thread.id)

        # "무엇을 도와드릴까요" 반환
        return message.data[0].content[0].text.value, thread.id

    except Exception as e:
        raise Exception(f"Error during conversation: {str(e)}")

def create_conversation_with_assistant(message: str, thread_id):
    try:
        # 메세지를 스레드에 추가
        message = client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=message
        )

        # assistant와 대화 실행
        run = client.beta.threads.runs.create(
            thread_id=thread_id
        )

        # 대화가 완료될 때까지 상태 확인
        while run.status != "completed":
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
            print(run.status)
            print(run.completed_at)

            # 대화 완료 후 챗봇 메시지를 출력
            message = client.beta.threads.messages.list(thread_id=thread_id)

        # "무엇을 도와드릴까요" 반환
        return message.data[0].content[0].text.value, thread_id

    except Exception as e:
        raise Exception(f"Error during conversation: {str(e)}")