import logging
from docx import Document

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PdfToCocConverter:
    """
    Класс для конвертации pdf файла в файл с расширением doc
    """

    def __init__(self, pdf_file):
        """
        Инициализация экземпляра с указанием пути к pdf-файлу
        """
        self.pdf_file = pdf_file
        self.document = Document()

    def convert_to_doc(self, text):
        """
        Добавляет текст в файл с расширение .doc
        :param text: текст который необходимо добавить
        """
        self.document.add_paragraph(text)
        self.document.add_page_break()

    def save_to_doc(self):
        """
        Сохраняет конвертированный pdf в файл с расширение .doc
        """
        convert_filename = f'{self.pdf_file.split(".")[0]}.doc'
        try:
            self.document.save(convert_filename)
            logger.info(f'Конвертированный pdf успешно сохранен в {convert_filename}')
        except Exception as exc:
            logger.error(f'Произошла ошибка при сохранении конвертированного pdf: {exc}')
