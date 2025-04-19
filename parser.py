
import requests
from bs4 import BeautifulSoup

def checkfresh_parser(brand: str, batch_code: str) -> dict:
    """
    Парсит дату выпуска парфюма по сайту checkfresh.com
    """
    url = f"https://www.checkfresh.com/{brand.lower()}.html"
    headers = {
        "User-Agent": "Mozilla/5.0",
    }
    try:
        # Подгружаем HTML страницы бренда
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        # Готовим POST-запрос на определение батча
        form_data = {
            "code": batch_code,
            "Submit": "Check+date+code",
        }
        post_url = f"https://www.checkfresh.com/{brand.lower()}.html?lang=en"
        post_response = requests.post(post_url, headers=headers, data=form_data, timeout=10)
        post_soup = BeautifulSoup(post_response.text, "html.parser")

        result_block = post_soup.find("div", {"id": "content"}).find("div", {"class": "resultbox"})

        if result_block:
            raw = result_block.get_text(separator="\n").strip()
            return {
                "brand": brand,
                "batch": batch_code,
                "result": raw,
                "status": "ok"
            }
        else:
            return {
                "brand": brand,
                "batch": batch_code,
                "result": "Не удалось определить дату. Возможно, неправильный код или неподдерживаемый бренд.",
                "status": "not_found"
            }
    except Exception as e:
        return {
            "brand": brand,
            "batch": batch_code,
            "result": f"Ошибка: {str(e)}",
            "status": "error"
        }
