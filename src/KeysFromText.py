import src.KeysBag as KeysBag
import src.Text.text_init as TextProcess

class KeysFromText:
    def __init__(self):
        pass

    def keys(self, text):
        keyf = TextProcess.text_processing()
        result = keyf.key_init(text)

        k = KeysBag.KeysBag()
        object_key = result.get('object')
        if len(object_key) > 0:
            k.set_type(object_key[0])

        direction_key = result.get('direction')
        if len(direction_key) > 0:
            k.set_direction(direction_key[0])

        return k
