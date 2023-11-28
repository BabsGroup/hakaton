from gigachat import GigaChat as GigaChatImpl

class GigaChat:
    def __init__(self):
        pass

    def createText(self, text, context):
        key = "NWM5ODNiMGYtYTE2MC00MmY3LWEwY2MtNTBmODg5ODYwNzhhOjdjY2IzOGE2LWVmMTgtNDEzMC1hZWVmLTlmYTRiZjJiM2U2Zg=="
        with GigaChatImpl(credentials=key, scope="GIGACHAT_API_PERS", verify_ssl_certs=False) as giga:
            response = giga.chat(f"""
Действуй как гид-экскурсовод. Я задам тебе вопрос про какой-то реальный объект и дам немного контекста про этот объект, а ты дашь краткий и интересный ответ. Не используй оценочные суждения.
Мой вопрос: {text} 
Контекст: {context}
            """)

            return response.choices[0].message.content
