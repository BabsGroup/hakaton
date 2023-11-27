import speech_recognition as sr
#from pydub import AudioSegment

class voise_processing():
    #def convert_mp3_to_wav(self , mp3_file, wav_file):
        #проблемы с ffpeg
        #audio = AudioSegment.from_mp3(mp3_file)
        #audio.export(wav_file, format='wav')


    def voice (self, way): 
        # Создаем объект распознавателя речи
        recognizer = sr.Recognizer()
        
        # Загружаем аудио файл
        audio_file = sr.AudioFile(way)
        
        # Распознаем речь из аудио файла
        with audio_file as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data ,  language="ru-RU")
        
        # Выводим текст
        return text
    

#convert_mp3_to_wav("./test_voice/alo.mp3", "./test_voice/res.wav")
#print(voise_processing.voice("./test_voice/phone.wav"))
