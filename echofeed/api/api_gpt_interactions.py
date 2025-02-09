import json
from datetime import datetime
from openai import OpenAI

from echofeed.common import config_info

client = OpenAI(api_key=config_info.OPENAI_API_KEY)


def categorize_keywords(keywords: list) -> dict:
    prompt = (
        "Împărțiți următoarele cuvinte cheie în categorii relevante. "
        "Fiecare categorie trebuie să fie determinată automat pe baza "
        "cuvintelor cheie furnizate. "
        "Returnează rezultatul într-un format de dicționar JSON unde cheia"
        " este numele categoriei și valoarea este o listă de cuvinte cheie. "
        f"Cuvintele cheie sunt: {', '.join(keywords)}."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "Ești un asistent care ajută la clasificarea"
                               " cuvintelor cheie în categorii relevante."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.5,
        )
        text_response = response.choices[0].message.content.strip()
        text_response = (text_response.replace("```json\n", "")
                         .replace("```", ""))

        categories = json.loads(text_response)

    except Exception as e:
        print(f"Eroare la clasificarea cuvintelor cheie: {e}")
        categories = {}

    return categories


def extract_string_from_response(response):
    """
    Extrage un șir de caractere din răspunsul primit de la modelul GPT.

    Args:
        response (object): Obiectul de răspuns primit de la modelul GPT.

    Returns:
        str: Șirul de caractere extras.
    """
    message_content = ""

    if hasattr(response, 'choices') and len(response.choices) > 0:
        message_content = response.choices[0].message.content

    print(f"Mesajul extras: {message_content}")

    return message_content


def extract_recommandation_queries(keywords: list, language: str) -> str:
    keywords_str = ", ".join(keywords)
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        f"Creează un query de căutare pe Google pentru a găsi"
                        f" articole de știri relevante bazate pe cuvintele"
                        f" cheie furnizate de utilizator. Query-ul"
                        f" trebuie să fie generat în limba {language}."
                        f" Folosește cuvintele cheie primite de la utilizator"
                        f" pentru a construi query-ul. Raspunsul sa fie exact"
                        f" sub forma in care ar putea fi pus intr-un query de"
                        f" cautare pe Google, fara cuvinte si caractere"
                        f" aditionale, intr-un singur string(fara caractere"
                        f" de tipul \" \')."
                    )
                },
                {
                    "role": "user",
                    "content": keywords_str
                }
            ],
            max_tokens=100,
            temperature=0.5,
        )
        query = extract_string_from_response(response).strip('"')
        print(query)

    except Exception as e:
        print(f"Eroare la extragerea cuvintelor cheie: {e}")

    return query


def extract_queries(important_keywords: list, relevant_keywords: list, irrelevant_keywords: list, language: str, min_keywords: int) -> str:
    important_keywords_str = ", ".join(important_keywords)
    relevant_keywords_str = ", ".join(relevant_keywords)
    irrelevant_keywords_str = ", ".join(irrelevant_keywords)

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        f"Creează un query de căutare pe Google pentru a găsi"
                        f" articole de știri relevante bazate pe cuvintele"
                        f" cheie furnizate de utilizator. Numărul minim"
                        f" de cuvinte cheie care"
                        f" trebuie folosite este {min_keywords}, dar nu-l"
                        f" depasi prea mult(maxim foloseste 2 cuvinte cheie in plus). Query-ul"
                        f" trebuie să fie generat în limba {language}. Urmează acești pași"
                        f" pentru a construi query-ul: 1. Cuvintele cheie"
                        f" foarte importante (important_keywords) trebuie să"
                        f" fie folosite în mod obligatoriu. 2. Din cuvintele cheie"
                        f" relevante (relevant_keywords) trebuie să fie"
                        f" folosite doar cele relevante celor importante și"
                        f" nu se suprapun cu"
                        f" cele foarte importante. 3. Cuvintele cheie"
                        f" irelevante (irrelevant_keywords) să fie folosite"
                        f" doar dacă nu există suficiente cuvinte cheie din"
                        f" categoriile anterioare pentru a forma query-ul"
                        f" complet, si in acel caz doar cele relevante cu cele"
                        f" selectate din categoriile precedente. 4. Ai dreptul"
                        f" de a modela query-ul folosind aceste cuvinte cheie"
                        f" si reguli astfel incat acesta sa fie optim pentru"
                        f" cautarea de stiri."
                        f" Raspunsul sa fie exact sub forma in care ar putea"
                        f" fi pus intr-un query de cautare pe Google, fara"
                        f" cuvinte si caractere aditionale, intr-un singur"
                        f" string(fara caractere de tipul \" \')."
                    )
                },
                {
                    "role": "user",
                    "content": f"important_keywords: {important_keywords_str}, relevant_keywords: {relevant_keywords_str}, irrelevant_keywords: {irrelevant_keywords_str}"
                }
            ],
            max_tokens=100,
            temperature=0.5,
        )
        query = extract_string_from_response(response).strip('"')
        print(query)

    except Exception as e:
        print(f"Eroare la extragerea cuvintelor cheie: {e}")

    return query


def generate_keywords(user_input: str, language) -> list:
    """
    Generează cuvinte cheie pentru căutarea pe Google în funcție de
     textul introdus de utilizator.

    Args:
        user_input (str): Textul introdus de utilizator.

    Returns:
        list: Lista de cuvinte cheie generate.
    """
    keywords = []
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": f"Genereaza cuvinte cheie pentru cautare"
                               f" de stiri pe baza textului introdus de"
                               f" utilizator. Nu vei scrie nimic altceva."
                               f" Cuvintele cheie vor fi separate prin"
                               f" virgula. Limba este {language}."
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ],
            max_tokens=100,
            temperature=0.5,
        )
        keywords = extract_string_from_response(response).split(", ")

    except Exception as e:
        print(f"Eroare la extragerea cuvintelor cheie: {e}")
    return keywords


def convert_string_to_date(date_string: str):
    """
    Convertește un șir de caractere într-un obiect de tip dată.

    Args:
        date_string (str): Șirul de caractere ce reprezintă data.

    Returns:
        date: Obiectul de tip dată.
    """
    return datetime.strptime(date_string, "%Y-%m-%d").date()
