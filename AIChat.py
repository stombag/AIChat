from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from openai import OpenAI

app = FastAPI()

@app.get("/")
async def home():
    return HTMLResponse("""
    <html>
        <body>
            <h1>RPG NPC 서버</h1>
            <p>서버 실행 중</p>
        </body>
    </html>
    """)

client = OpenAI(
    base_url="http://127.0.0.1:1234/v1",
    api_key="lm-studio"
)

conversation_memory = {}


@app.post("/chat")
async def chat(data: dict):

    npc_type = data["npc_type"]
    user_message = data["message"]

    # NPC별 메모리 생성
    if npc_type not in conversation_memory:
        conversation_memory[npc_type] = []

    system_prompt = ""

    if npc_type == "Guard":
        system_prompt = (
            "너는 한국 RPG 게임 마을의 경비병 NPC다. "
            "플레이어와 자연스럽게 대화한다. "
            "자신이 경비병이라는 사실을 반복하지 않는다. "
            "질문에 직접 답변한다. "
            "반드시 한국어만 사용한다. "
            "짧고 자연스럽게 말한다."
        )

    elif npc_type == "Merchant":
        system_prompt = (
            "너는 한국 RPG 게임의 상인 NPC다. "
            "물건을 판매한다. "
            "친절하게 대화한다. "
            "자신이 상인이라는 말을 반복하지 않는다. "
            "반드시 한국어만 사용한다."
        )

    elif npc_type == "Blacksmith":
        system_prompt = (
            "너는 한국 RPG 게임의 대장장이 NPC다. "
            "무기와 방어구를 제작한다. "
            "무뚝뚝하지만 친절하다. "
            "자신이 대장장이라는 말을 반복하지 않는다. "
            "반드시 한국어만 사용한다."
        )

    # 사용자 입력 저장
    conversation_memory[npc_type].append(
        {
            "role": "user",
            "content": user_message
        }
    )

    # 최근 대화 10개만 유지
    recent_memory = conversation_memory[npc_type][-10:]

    messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ] + recent_memory

    response = client.chat.completions.create(
        model="qwen2.5-7b-instruct",
        messages=messages,
        temperature=0.8
    )

    reply = response.choices[0].message.content

    # NPC 답변 저장
    conversation_memory[npc_type].append(
        {
            "role": "assistant",
            "content": reply
        }
    )

    return reply
    # AIChat
