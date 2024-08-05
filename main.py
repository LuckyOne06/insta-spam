from browser import driver, wait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.support import expected_conditions as EC
import time

usernames = []
usernames_for_spam = []


def _setting_script():

    need_to_parse = input("[-] Парсить никнеймы? (Да/Нет): ")
    spam_message = input("[-] Сообщение для спама: ")
    if need_to_parse == "Нет":
        spam_limit = int(input("[-] Кол-во сообщений: "))
        usernames_file = input("[-] Имя файла с никнеймами: ")

        print("[-] Начали...")
        return [0, spam_limit, usernames_file, spam_message]

    else:
        account_count = int(input("[-] сколько парсить?: "))
        if account_count > 0:
            account_count += 1
        parse_profile = input("[-] Откуда парсить (username): ")
        extract_file = input("[-] Куда экспортировать?: ")  #
        spam_limit = int(input("[-] Кол-во сообщений: "))

        print("[-] Начали...")
        return [1, account_count, parse_profile, extract_file, spam_limit, spam_message]


def _parse_usernames(account_count, parse_profile):

    i = 1
    driver.get(f"https://www.instagram.com/{parse_profile}/")
    followers_button = (By.CSS_SELECTOR, f'a[href="/{parse_profile}/followers/"]')
    wait.until(EC.presence_of_element_located(followers_button)
               and EC.element_to_be_clickable(followers_button)).click()

    user_tuple = (By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]'
                            f'/section/main/div[2]/div[1]/div/div[{i}]/div/div/div/div[2]'
                            '/div/div/div/a/div/div/span')

    wait.until(EC.presence_of_element_located(user_tuple))

    while True:

        if i % 10 == 0:
            print(f"[-] Спарсили: {i} юзернеймов...")
        if i == account_count:
            print("[-] Закончили парсинг...")
            break

        user_tuple = (By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]'
                                f'/section/main/div[2]/div[1]/div/div[{i}]/div/div/div/div[2]'
                                '/div/div/div/a/div/div/span')

        try:
            username = driver.find_element(user_tuple[0], user_tuple[1])
            usernames.append(username.text)
            i += 1

        except NoSuchElementException:
            driver.execute_script("window.scrollBy(0, 500)", "")
            time.sleep(3)


def _extract_usernames(file_name):

    with open(f"{file_name}", "a") as f:
        for nickname in usernames:
            f.write(nickname + "\n")
    print("[-] Экспортированы все никнеймы...")


def _delete_repeat_profiles(file_name):

    with open(file_name, 'r') as f:
        lines = f.readlines()

    with open(file_name, 'w') as f:
        f.writelines(lines[len(usernames_for_spam):])
    print("[-] Почистили никнеймы в файле...")


def _send_msg(file_name, spam_limit, spam_message):

    if spam_limit == 0:
        return 0

    with open(file_name, "r") as f:
        for line in f.readlines():
            if len(usernames_for_spam) == spam_limit:
                break
            usernames_for_spam.append(line.strip())

    _delete_repeat_profiles(file_name=file_name)
    driver.get(f"https://www.instagram.com/direct/inbox/")

    for username in usernames_for_spam:
        new_msg_btn = (By.CSS_SELECTOR, 'svg[aria-label="Новое сообщение"]')
        user_direct_btn = (By.XPATH, f"//*[contains(text(), '{username}')]")
        chat_btn = (By.XPATH, "//*[contains(text(), 'Далее')]")
        msg_form = (By.CSS_SELECTOR, 'div[contenteditable="true"][role="textbox"]')
        submit_btn = (By.XPATH, "//*[contains(text(), 'Отправить')]")
        return_btn = (By.CSS_SELECTOR, 'svg[aria-label="Назад"]')

        try:
            wait.until(EC.presence_of_element_located(new_msg_btn) and EC.element_to_be_clickable(new_msg_btn)).click()

        except ElementClickInterceptedException:
            print("[-] ElementClickInterceptedException... pass")
            continue

        try:
            wait.until(EC.presence_of_element_located((By.NAME, "queryBox"))).send_keys(username)
            wait.until(EC.presence_of_element_located(user_direct_btn)
                       and EC.element_to_be_clickable(user_direct_btn)).click()
            wait.until(EC.presence_of_element_located(chat_btn) and EC.element_to_be_clickable(chat_btn)).click()

        except Exception:
            continue

        try:
            wait.until(EC.presence_of_element_located(msg_form)).send_keys(f"{spam_message}")
            wait.until(EC.presence_of_element_located(submit_btn) and EC.element_to_be_clickable(submit_btn)).click()

        except NoSuchElementException:
            wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Список людей, которые могут"
                                                                 " отправлять сообщения владельцу этого аккаунта, "
                                                                 "ограничен.')]")))
        finally:
            wait.until(EC.presence_of_element_located(return_btn) and EC.element_to_be_clickable(return_btn)).click()
    print("[-] Спам окончен...")


def main():

    settings = _setting_script()
    if settings[0] == 0:
        _send_msg(file_name=settings[2], spam_limit=settings[1], spam_message=settings[3])
        print("[-] Завершение...")

    else:
        _parse_usernames(account_count=settings[1], parse_profile=settings[2])
        _extract_usernames(file_name=settings[3])
        _send_msg(file_name=settings[3], spam_limit=settings[4], spam_message=settings[5])
        print("[-] Завершение...")


if __name__ == '__main__':
    main()


