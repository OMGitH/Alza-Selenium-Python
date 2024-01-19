class TestData:

    # Alza url
    url = "https://www.alza.cz/"

    # test_login_logout
    user_name = "wedey95103@haizail.com"
    password = "PasHes12"
    incorrect_user_name = "aa@haizail.com"
    incorrect_password = "aaHes12"
    signin_button_incorrect_user_name_password_text = "Neplatné uživatelské jméno nebo heslo"
    blank_email_text = "Zadejte e-mailovou adresu"
    blank_password_text = "Zadejte prosím heslo"
    user_signed_in_text = user_name

    # test_basket_add_remove_item
    number_of_items_in_basket = 1
    text_once_all_items_removed_from_basket = "Jsem tak prázdný..."

    # test_search
    search_value_via_search_button = "jízdní kola"
    search_result_header_via_search_button = "Jízdní kola"
    search_value_via_suggestion = "recenze"
    search_result_word_in_title_via_suggestion = "recenze"

    # test_watchdogs_add_remove_item
    watchdog_price_limit = "10"
    text_once_all_items_removed_from_watchdogs_page = "Momentálně pro vás nehlídáme žádné produkty"

    # test_delivery_addresses_add_remove_addresses
    delivery_address_1_original = {"name surname": "Jarda Starý",
                        "street and number": "Ulice 4",
                        "zip": "10000",
                        "city": "Praha",
                        "phone": "777 123 456"}
    delivery_address_2_original = {"name surname": "Petr Nový",
                        "street and number": "Jarní 20",
                        "zip": "11000",
                        "city": "Ostrava",
                        "phone": "777 456 789"}
    delivery_addresses_original = [delivery_address_1_original, delivery_address_2_original]
    delivery_address_1_edited = {"name surname": "Martin Pávek",
                               "street and number": "Nová 17",
                               "zip": "12000",
                               "city": "Liberec",
                               "phone": "604 987 654"}
    delivery_address_2_edited = {"name surname": "Gregor Běžný",
                               "street and number": "Podzimní 45",
                               "zip": "13000",
                               "city": "Brno",
                               "phone": "604 654 321"}
    delivery_addresses_edited = [delivery_address_1_edited, delivery_address_2_edited]
