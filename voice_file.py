import pyttsx3


class TextToSpeechConvertor:
    """
    Класс для конвертации текста в голос
    """

    def __init__(self, rate=190, volume=0.8, num_voice=0):
        """
        :param rate: скорость голоса
        :param volume: громкость голоса
        :param num_voice: номер голоса (id-голоса) из доступных голосов в ОС
        """
        self.rate = rate
        self.volume = volume
        self.num_voice = num_voice
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', self.rate)
        self.engine.setProperty('volume', self.volume)
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', self.voices[self.num_voice].id)

    def text_to_speech(self, text):
        """
        Произносит текст в слух
        :param text: текст который необходимо озвучить
        """
        self.engine.say(text)
        self.engine.runAndWait()
