
class text_processing():
        
    len_trash = 2
    direction_key   = [ "слева" , "спереди" , "впереди" , "сзади" , "справа" , "cпереди"  , "передо", "вокруг" ]
    object_key      = [ "здание" , "зданию",  "здания", "лес" , "леса", "лесу", "парк" ,"парка", "парку", "дом" , "дома", "дому", "дома", "памятник", "памятнику", "памятника", "памятники", "метро" ]
    question_key    = [ "сколько", "когда", "кто" , "какой" , "что" ]
    question_target = [ "архитектор", "лет","год","году", "жил" , "проживал" ]
    # уточения ? по тиу сколько лет , кто архитектор 
# нужны ли множественые формы слов ?
    standart_direction_key = [ "слева" , "справа" , "спереди" , "сзади", "вокруг" ]
    standart_object_key    = [ "лес" , "дом" , "памятник" , "парк" , "здание", "метро" ]
    standart_question      = [ "сколько", "когда", "кто" ,"какой" , "что" ]
    standart_add_key       = [ "архитектор", "лет","год", "жил" ]

    standart_key = [ standart_direction_key , standart_object_key , standart_question , standart_add_key ]
    
    def text_input( self, text_in ): # разбиваем текст на массив по пробелам
        text_in = text_in.split()
        
        return text_in

    def text_filt( self, text_trash ) : # убираем предлоги и переводим всё к нижнему регистру
        text_ntrash = []

        for i in range( len(text_trash) ):         
            if ( len(text_trash[i]) > self.len_trash ):
                text_ntrash.append( text_trash[i].lower() ) 

        return text_ntrash

    def key_word ( self, text_ntrash ): # первичный поиск ключей с учётом всех возможных ошибочных варинтов
        # вероятно хорошо бы убрать эту функцию и доделать standartization  что бы каждое слово изначально проверялось под  стандарт 
        

        text_key=[ [],[],[],[],[] ] # размерность соотвествует количесву типов ключей
        obj_key    = []
        dir_key    = []
        quest_key  = []
        add_key    = []
        string_out = []

        for i in range( len(text_ntrash) ): # распределяем слова по типам ключей 
            
            if ( self.direction_key.count(text_ntrash[i]) ):
                dir_key.append(text_ntrash[i])
                string_out.append(text_ntrash[i]) 

            elif ( self.object_key.count( text_ntrash[i]) ):
                obj_key.append( text_ntrash[i] )
                string_out.append(text_ntrash[i])

            elif ( self.question_key.count(text_ntrash[i]) ): 
                quest_key.append( text_ntrash[i] )
                string_out.append(text_ntrash[i])

            elif (self.question_target.count(text_ntrash[i])):
                add_key.append( text_ntrash[i] )                      
                string_out.append(text_ntrash[i])

        text_key[0],text_key[1],text_key[2],text_key[3], text_key[4] =  dir_key , obj_key , quest_key , add_key , string_out

        return text_key
    
    def standardization( self, trash_key , type ): # подгон всех полученных ранее ключей под стандартную форму и разделение на группы  
        standart_word_key =[]
        for i in trash_key:
            for j in self.standart_key[type]:

                sum = 0 # счетчик количества одинаковых символов
                small =  lambda a,b : len(a) if len(a) < len(b) else len(b) # наименьшее из двух слов 
                for k in range( small(i,j) ):
                    if i[k] == j[k]: #сравниваем на соотвествие 
                        sum+=1
                    if ( sum < k-2 ): #что бы не полностью проверять совсем разные слова
                        break    

                if ( sum >= (len(j) * 0.8) ): # если  длина проверяемого слова совпадает с талоном на 0.8 то  стандарт записывается в вывод
                    standart_word_key.append(j)
                    break

        return standart_word_key

    def key_init ( self, in_text ): # старт с указанеи первичного текста
        out_key = []
        out_key = self.text_input( in_text )
        out_key = self.text_filt( out_key )
        out_key = self.key_word( out_key )

        for i in range ( len(out_key)-1 ): 
            out_key[i] = self.standardization( out_key[i] , i )

        struct = { 'direction' : out_key[0] , 'object' : out_key[1] , 'question' : out_key[2] , 'add' : out_key[3] , 'string' : out_key[4]  } # словарь для более удобного обращения потом

        return struct


    


#text_start = input()
#text_start = "Я хочу узнать что за здание справа от меня , может это лес , какой год , кто архитектор"

#text = []
# text = textf.text_input(text_start)
# text = textf.text_filt(text)
# text = textf.key_word(text)
# text = textf.standardization(text)

#textf = text_processing() 
#text = textf.key_init(text_start) 
#print(text)