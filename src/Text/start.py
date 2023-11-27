import text_init as ti
import voise_text as vt

voisef = vt.voise_processing()
text_start = voisef.voice("./test_voice/test1.wav")
print(text_start)
#text_start = "Я хочу узнать что за здание справа от меня"
text = []
textf = ti.text_processing() 
text = textf.start(text_start)

print("Sort key: ", text)