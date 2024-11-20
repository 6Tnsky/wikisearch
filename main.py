from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def get_driver():
    # Убедитесь, что путь к chromedriver указан правильно
    driver = webdriver.Chrome()  # Создаем экземпляр драйвера
    return driver

def search_wikipedia(driver, query):
    driver.get("https://ru.wikipedia.org/wiki/%D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0")
    search_box = driver.find_element(By.ID, "searchInput")
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)  # Подождите загрузки страницы

def list_paragraphs(driver):
    paragraphs = driver.find_elements(By.TAG_NAME, "p")
    for i, paragraph in enumerate(paragraphs):
        print(f"Paragraph {i + 1}: {paragraph.text[:100]}...")  # Печатаем первые 100 символов
        if i % 5 == 4:  # После каждого пятого параграфа предлагаем продолжить
            cont = input("Продолжить просмотр параграфов? (y/n): ")
            if cont.lower() != 'y':
                break

def list_internal_links(driver):
    links = driver.find_elements(By.CSS_SELECTOR, "#bodyContent a")
    internal_links = [link for link in links if
                      link.get_attribute('href') and 'wikipedia.org' in link.get_attribute('href')]

    for i, link in enumerate(internal_links[:10]):  # Показать первые 10 ссылок
        print(f"{i + 1}. {link.text} ({link.get_attribute('href')})")

    choice = int(input("Выберите номер ссылки для перехода или 0 для отмены: "))
    if choice > 0 and choice <= len(internal_links):
        return internal_links[choice - 1].get_attribute('href')
    return None

def main():
    driver = get_driver()

    try:
        query = input("Введите запрос для поиска на Википедии: ")
        search_wikipedia(driver, query)

        while True:
            print("\nВыберите действие:")
            print("1. Листать параграфы текущей статьи")
            print("2. Перейти на одну из связанных страниц")
            print("3. Выйти из программы")

            action = input("Ваш выбор: ")

            if action == '1':
                list_paragraphs(driver)
            elif action == '2':
                new_url = list_internal_links(driver)
                if new_url:
                    driver.get(new_url)
                    time.sleep(2)  # Подождите загрузки страницы
            elif action == '3':
                break
            else:
                print("Неверный выбор. Попробуйте снова.")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()