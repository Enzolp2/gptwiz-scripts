import PyPDF2
import pdfplumber

# Using PyPDF2
def extract_text_from_pdf2(pdf_path):
    """
    Extrai o texto de um arquivo PDF e retorna como uma única string.

    Args:
        pdf_path (str): O caminho para o arquivo PDF a ser processado.

    Returns:
        str: Uma string contendo o texto extraído do PDF.

    Raises:
        Exception: Se ocorrer um erro ao tentar abrir ou processar o arquivo PDF.

    Exemplo de uso:
        texto_extraido = extract_text_from_pdf('exemplo.pdf')
    """
    text = ""
    try:
        with open(pdf_path, "rb") as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            num_pages = len(pdf_reader.pages)
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
    except Exception as e:
        print(f"Erro ao extrair texto do PDF: {str(e)}")
    
    return text

# Using pdfplumber
def extract_text_from_pdfplumber(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Exporta para um arquivo .txt
def export_to_text_file(text, path_to_export):
    try:
        with open(path_to_export, 'w', encoding='utf-8') as file:
            file.write(text)
    except Exception as e:
        print(f"Erro ao exportar o texto para o arquivo: {str(e)}")
    
# Exemplo de uso:
# pdf_path_installation = "C:\\adeptmec\\dev\\pdf-extract\\pdf\\acm-installation.pdf"
# pdf_path_operating = "C:\\adeptmec\\dev\\pdf-extract\\pdf\\acm-operating.pdf"
# pdf_path_tdm = "C:\\adeptmec\\dev\\pdf-extract\\pdf\\tdm.pdf"
# pdf_path_tdm_gl = "C:\\adeptmec\\dev\\pdf-extract\\pdf\\tdm-gl.pdf"
# pdf_path_tx750 = "C:\\adeptmec\\dev\\pdf-extract\\pdf\\TX750.pdf"
# pdf_path_vs500 = "C:\\adeptmec\\dev\\pdf-extract\\pdf\\VX500.pdf"
# pdf_tdm_hlp = "C:\\adeptmec\\dev\\pdf-extract\\pdf\\tdm-hlp\\"

if __name__ == "__main__":
    import os
    from dotenv import load_dotenv

    # Carregar variáveis do arquivo .env
    load_dotenv()

    directory = os.getenv("DIRECTORY")
    export_path = os.getenv("EXPORT_PATH")
    pdf2 = os.getenv('PYPDF2')
    plumber = os.getenv('PDFPLUMBER')

    if pdf2 == "TRUE" and plumber == "TRUE":
        print("[ERROR] PDF2 e PLUMBER não podem ser usados simultaneamente\n\n.env\n\nPYPDF2=TRUE\nPDFPLUMBER=TRUE")
        quit()
    
    if pdf2 == "FALSE" and plumber == "FALSE":
        print("[ERROR] PDF2 ou PLUMBER precisa ser selecionado\n\n.env\n\nPYPDF2=FALSE\nPDFPLUMBER=FALSE")
        quit()
    

    """ Extrair todos os pdfs desse diretorio """

    if os.path.isdir(directory):
        files = os.listdir(directory)

    else:
        print("[ERROR] Caminho inválido", directory)
        quit()

    for file in files:
        if os.path.isfile(os.path.join(directory, file)):
            if file.endswith(".pdf"):
                
                if pdf2 == "TRUE":
                    text = extract_text_from_pdf2(os.path.join(directory, file))

                if plumber == "TRUE":
                    text = extract_text_from_pdfplumber(os.path.join(directory, file))

                if text != '':
                    export_to_text_file(text, os.path.join(export_path, file[:-4] + ".txt"))
                
                print(f'[OK] Arquivo {file} exportado com sucesso')
                
            else:
                print(f'[WARNING] Only pdf file is allowed - {file}')

