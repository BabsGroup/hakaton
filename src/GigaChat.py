from gigachat import GigaChat as GigaChatImpl
from gigachat.models import Chat, Messages, MessagesRole

class GigaChat:
    def __init__(self):
        pass

    def createText(self, text, context):
        key = "NWM5ODNiMGYtYTE2MC00MmY3LWEwY2MtNTBmODg5ODYwNzhhOjdjY2IzOGE2LWVmMTgtNDEzMC1hZWVmLTlmYTRiZjJiM2U2Zg=="
        with GigaChatImpl(credentials=key, scope="GIGACHAT_API_PERS", verify_ssl_certs=False) as giga:
            try:
                payload = Chat(
                    messages=[
                        Messages(
                            role=MessagesRole.SYSTEM,
                            content=
f"""Ты веселый экскурсовод,который ведет экскурсию у пользователя.Вокруг пользователя скорее всего находятся:{context}.
Надо коротко и интересно ответить на его вопрос.Избегай слов старейший,красивейший и других оценочных прилогательных.Больше шути.
Если ты ответишь интересно, я оставлю тебе большие чаевые!"""
                        ),
                        Messages(
                            role=MessagesRole.USER,
                            content=
                            f"""Мой вопрос:s{text}"""
                        )
                    ],
                    temperature=1.2,
                )

                response = giga.chat(payload)
                print(response)

                return response.choices[0].message.content
            except Exception as e:
                print(e)
