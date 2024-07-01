import PyPDF2
import logging
from PyPDF2.errors import PdfReadError
from voice_file import TextToSpeechConvertor
from docx_file import PdfToCocConverter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PdfFileOpener(PdfToCocConverter):
    """
    Класс для открытия и обработки pdf файла
    """

    def __init__(self, pdf_file, rate=190, volume=0.8, num_voice=1):
        """
        :param pdf_file: файл в формате pdf
        :param rate: скорость голоса
        :param volume: громкость голоса
        :param num_voice: номер голоса(id-голоса) в ОС
        """
        super().__init__(pdf_file)
        self.pdf_file = pdf_file
        self.rate = rate
        self.volume = volume
        self.num_voice = num_voice
        self.text_to_speech = TextToSpeechConvertor(self.rate, self.volume, self.num_voice)

    def check_file_format(self):
        """
        Проверяет формат файл
        :return: True или False
        """
        return self.pdf_file.lower().endswith('.pdf')

    def select_action(self):
        """
        Выбирает что сделать с файлов
        :return: номер выбранного действия
        """
        convert_to_speech = 'Преобразовать в речь'
        convert_to_doc = 'Преобразовать в doc'
        while True:
            self.text_to_speech.text_to_speech('Выберите необходимое действие')
            try:
                action = int(input(f'1. {convert_to_speech} | 2. {convert_to_doc}:   '))
                if 1 <= action <= 2:
                    self.text_to_speech.text_to_speech(
                        f'Выбрано {convert_to_speech if action == 1 else convert_to_doc}')
                    return action
            except ValueError as exc:
                logger.error(f'Ошибка ввода: {exc}')

    def process_pdf(self, pdf_file, start_page, end_page, action):
        """
        Обрабатывает pdf-файл
        :param pdf_file: открытый pdf-файл
        :param start_page: начальная страница
        :param end_page: конечная страница
        :param action: действие которое выбрал пользователь
        """
        for page in range(start_page, end_page):
            print(f'Текущая страница: {page + 1}')
            page_text = pdf_file.pages[page].extract_text()
            if action == 1 and page_text:
                self.text_to_speech.text_to_speech(page_text)
            elif page_text:
                self.convert_to_doc(page_text)

    def main(self, start_page=1, end_page=None):
        """
        Читает pdf-файл и выполняет необходимые действия
        :param start_page: начальная страница
        :param end_page: конечная страница
        """
        if not self.check_file_format():
            return
        try:
            with open(self.pdf_file, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                number_of_pages = len(pdf_reader.pages)
                set_end_page = end_page if end_page else number_of_pages
                action = self.select_action()
                self.process_pdf(pdf_reader, start_page - 1, set_end_page, action)
            if action != 1:
                self.save_to_doc()
        except FileNotFoundError as exc:
            logger.error(f'Файл не найден: {exc}')
        except PdfReadError as exc:
            logger.error(f'Ошибка чтения файла pdf: {exc}')
        except Exception as exc:
            logger.error(f'Неожиданная ошибка: {exc}')


if __name__ == '__main__':
    test_file = 'Бейдер - Чистый Python.pdf'
    pdf_opener = PdfFileOpener(test_file)
    pdf_opener.main()
