import requests
from database import get_verse, insert_dictionary, insert_interlinear, \
    insert_reference, get_book, get_chapter


def extract_references(abbr, chapter, verse):
    """Get references in browser."""
    url = f"https://pesquisa.biblia.com.br/pt-BR/crossref/ACF/{abbr}/{chapter}/{verse}"
    references = requests.get(url, allow_redirects=True)

    book_id = get_book(abbr)[0]
    chapter_id = get_chapter(book_id, chapter)[0]
    reference_id = get_verse(book_id, chapter_id, verse)[0]    

    for r in references.json():
        verse_number = r["versiculo_para"]
        chapter_number = r["capitulo_para"]
        book_abbr = r["padrao"]
        text = f"{r['nomeLivro']} {chapter_number}:{verse_number}"        
        # save in database
        insert_reference(book_abbr, chapter_number, verse_number, reference_id, text)


def extract_interlinear(abbr, chapter, verse):
    """Get interlinear."""    
    url = f"https://pesquisa.biblia.com.br/pt-BR/interlinear/ACF/{abbr}/{chapter}/{verse}"
    interlineares = requests.get(url, allow_redirects=True)
    
    book_id = get_book(abbr)[0]
    chapter_id = get_chapter(book_id, chapter)[0]
    verse_id = get_verse(book_id, chapter_id, verse)[0]
    
    for i in interlineares.json():
        # save in database
        insert_interlinear(verse_id, i)


def extract_dictionary(abbr, chapter, verse):
    """Get dictionary."""
    book_id = get_book(abbr)[0]
    chapter_id = get_chapter(book_id, chapter)[0]

    url = f"https://pesquisa.biblia.com.br/pt-BR/dictionary/ACF/{abbr}/{chapter}/{verse}"
    
    dictionaries = requests.get(url, allow_redirects=True)
    for d in dictionaries.json():
        # save in database
        insert_dictionary(abbr, chapter_id, verse, d)


