from docx import Document


class WrodFileReader:
    @staticmethod
    def read_file(file_path: str) -> list[str]:
        doc = Document(file_path)

        content = []
        for paragraph in doc.paragraphs:
            content.append(paragraph.text)
        return content

    @staticmethod
    def write_file(file_path: str, new_text: list[str]) -> None:
        doc = Document(file_path)
        text_i = 0

        for paragraph in doc.paragraphs:
            for run in paragraph.runs:
                if text_i < len(new_text):
                    is_bold = run.bold
                    is_italic = run.italic
                    font_size = run.font.size
                    aligment = paragraph.alignment

                    run.clear()
                    run.text = new_text[text_i]

                    run.bold = is_bold
                    run.italic = is_italic
                    run.font.size = font_size
                    paragraph.alignment = aligment

                    text_i += 1

                else:
                    break

        doc.save(file_path)
