
class text_processing():
    len_trash = 2
    object_key = ["памятник", "здание", "лес", "парк", "парка", "дом", "здание"]
    direction_key = [ "слева" , "спереди" , "впереди" , "сзади" , "справа" , "cпереди" , "справау" , "передо" ]
    question_key = ["сколько","когда","году", "год"]

    standart_key = ["лес" , "дом" , "памятник" , "парк" , "слева" , "справа" , "спереди" , "сзади", "сколько","когда","год" , "здание" , "передо" ] # хорошо бы разбить на несколько массивов для ускорения проверки

    def __init__(self):
        pass

    def text_input(self, text_in ): # разбиваем текст на массив по пробелам
        text_in = text_in.split()
        
        return text_in

    def text_filt (self, text_trash): # убираем предлоги и переводим всё к нижнему регистру
        text_ntrash = []

        for i in range(len(text_trash)):         
            if (len(text_trash[i])> self.len_trash):
                text_ntrash.append(text_trash[i].lower()) 

        return text_ntrash

    def key_word ( self, text_ntrash ): # первичный поиск ключей с учётом всех возможных ошибочных варинтов
        # вероятно хорошо бы убрать эту функцию и доделать standartization  что бы каждое слово изначально проверялось под  стандарт 
        

        text_key=[[],[],[]] # размерность соотвествует количесву типов ключей
        obj_key = []
        dir_key = []
        quest_key = []
        for i in range(len(text_ntrash)):
            
            if ( self.object_key.count(text_ntrash[i])):
                obj_key.append(text_ntrash[i])
                
            elif ( self.direction_key.count(text_ntrash[i])):
                dir_key.append(text_ntrash[i])

            elif ( self.question_key.count(text_ntrash[i])): 
                quest_key.append(text_ntrash[i])                     

        text_key[0],text_key[1],text_key[2] = obj_key , dir_key , quest_key
        print("Trash key: ",text_key)
        return text_key
    
    def standardization(self, trash_key): # подгон всех полученных ранее ключей под стандартную форму и разделение на группы  
        standart_word_key =[]
        for i in trash_key:
            for j in self.standart_key:

                sum = 0
                small =  lambda a,b : len(a) if len(a)<len(b) else len(b) # наименьшее из двух слов 
                for k in range(small(i,j)):
                    if i[k] == j[k]: #сравниваем на соотвествие 
                        sum+=1
                    if (sum < k-2): #что бы не полностью проверять совсем разные слова
                        break    

                if (sum >= len(j)*0.8):
                    standart_word_key.append(j)
                    break

        return standart_word_key

    def start (self, in_text): # старт с указанеи первичного текста
        out_key = []
        out_key = self.text_input(in_text)
        out_key = self.text_filt(out_key)
        out_key = self.key_word(out_key)

        for i in range (len(out_key)): 
            out_key[i] = self.standardization(out_key[i])

        return out_key    


    


#text_start = input()
#text_start = "Я хочу узнать что за зданиеу справау от меня , может это лес , какой год"

#text = []

# textf = text_processing() 
# text = textf.text_input(text_start)
# text = textf.text_filt(text)
# text = textf.key_word(text)
# text = textf.standardization(text)

#textf = text_processing() 
#text = textf.start(text_start) 
#print(text)