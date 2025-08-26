from src.ai.ai_service import AIService


async def test_ai():

    ai_service = AIService()

    res = await ai_service.test_model("who are the best basketball players?")

    print(res)

    print("Done")


if __name__ == "__main__":
    import asyncio

    asyncio.run(test_ai())
