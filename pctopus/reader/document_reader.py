import os
from pathlib import Path

## This function is used to read from text files
def read_txt_file(file_path: str) -> str:
    """Read content from a text file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except UnicodeDecodeError:
        # Fallback encodings if UTF-8 fails
        for encoding in ['latin-1', 'ascii', 'utf-16']:
            try:
                with open(file_path, 'r', encoding=encoding) as file:
                    return file.read()
            except UnicodeDecodeError:
                continue
        raise

## This function is used to read the text content from PDF files
def read_pdf_file(file_path: str) -> str:
    """Read content from a PDF file"""
    try:
        from PyPDF2 import PdfReader
        reader = PdfReader(file_path)
        return '\n'.join(page.extract_text() for page in reader.pages)
    except ImportError:
        raise ImportError("PyPDF2 is required to read PDF files. Install it using: pip install PyPDF2")

## This function is used to read the text content from Word document (.doc, .docx)
def read_word_file(file_path: str) -> str:
    """Read content from a Word document"""
    try:
        from docx import Document
        doc = Document(file_path)
        return '\n'.join(paragraph.text for paragraph in doc.paragraphs)
    except ImportError:
        raise ImportError("python-docx is required to read Word files. Install it using: pip install python-docx")

## A common class that we can use to extract text content from text files, PDFs and Word document
class DocumentReader:
    def __init__(self):
        # Register file formats and their corresponding reader functions
        self.readers: Dict[str, Callable] = {
            '.txt': read_txt_file,
            '.pdf': read_pdf_file,
            '.doc': read_word_file,
            '.docx': read_word_file,
        }

    def supported_formats(self) -> list[str]:
        """Return list of supported file formats"""
        return list(self.readers.keys())

    def read(self, file_path: str) -> str:
        """
        Read content from a document file based on its extension
        
        Args:
            file_path (str): Path to the document file
            
        Returns:
            str: Text content of the document
            
        Raises:
            ValueError: If the file format is not supported
            FileNotFoundError: If the file doesn't exist
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        file_extension = Path(file_path).suffix.lower()
        
        reader = self.readers.get(file_extension)
        if reader is None:
            supported = ', '.join(self.supported_formats())
            raise ValueError(f"Unsupported file format: {file_extension}. Supported formats are: {supported}")
            
        return reader(file_path)
