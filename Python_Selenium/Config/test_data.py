class TestData:
    url = "https://www.alza.cz/"

    user_name = "wedey95103@haizail.com"
    password = "PasHes12"
    incorrect_user_name = "aa@haizail.com"
    incorrect_password = "aaHes12"
    signin_button_incorrect_user_name_password_text = "Neplatné uživatelské jméno nebo heslo"
    blank_email_text = "Zadejte e-mailovou adresu"
    blank_password_text = "Zadejte prosím heslo"
    user_signed_in_text = user_name

    number_of_items_in_basket = 1
    text_once_all_items_removed_from_basket = "Jsem tak prázdný..."

    search_value_via_search_button = "jízdní kola"
    search_result_header_via_search_button = "Jízdní kola"

    search_value_via_suggestion = "recenze"
    search_result_word_in_title_via_suggestion = "recenze"

    watchdog_price_limit = "10"
    text_once_all_items_removed_from_watchdog_list = "Momentálně pro vás nehlídáme žádné produkty"

    delivery_address_1 = {"name surname": "Jarda Starý",
                        "street and number": "Ulice 4",
                        "zip": "10000",
                        "city": "Praha"}
    delivery_address_2 = {"name surname": "Petr Nový",
                        "street and number": "Jarní 20",
                        "zip": "11000",
                        "city": "Ostrava"}
    delivery_addresses = [delivery_address_1, delivery_address_2]