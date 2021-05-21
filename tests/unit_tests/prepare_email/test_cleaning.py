import pytest
import numpy as np
from melusine.prepare_email.cleaning import (
    remove_multiple_spaces_and_strip_text,
    remove_accents,
    flag_items,
    remove_transfer_answer_header,
)


@pytest.mark.parametrize(
    "input_str, expected_str",
    [
        ("hello   world", "hello world"),
        ("\n   hello world    ", "hello world"),
        ("----- hello\tworld *****", "hello world"),
        ("hello-world", "hello-world"),
        ("hello - world", "hello world"),
    ],
)
def test_remove_multiple_spaces_and_strip_text(input_str, expected_str):
    result = remove_multiple_spaces_and_strip_text(input_str)
    np.testing.assert_string_equal(result, expected_str)


def test_remove_accents():
    input_str = "éèëêàù"
    expected_str = "eeeeau"

    result = remove_accents(input_str)
    np.testing.assert_string_equal(result, expected_str)


@pytest.mark.parametrize(
    "input_str, expected_str",
    [
        ("RE: hello world", " hello world"),
        ("re :", ""),
        ("TR: hello", " hello"),
        ("hello ", "hello "),
        ("Fwd:hello", "hello"),
    ],
)
def test_remove_transfer_answer_header(input_str, expected_str):
    result = remove_transfer_answer_header(input_str)
    np.testing.assert_string_equal(result, expected_str)


@pytest.mark.parametrize(
    "input_str, expected_str1, expected_str2, expected_str3",
    [
        (
            "Bonjour, mon email : prenom.nom@hotmail.fr",
            "Bonjour, mon email :  flag_mail_ ",
            "Bonjour, mon email : prenom.nom@hotmail.fr",
            "Bonjour, mon email :  flag_mail_ ",
        ),
        (
            "Mon numéro : 01.23.45.67.89", 
            "Mon numéro :  flag_phone_ ",
            "Mon numéro :  flag_phone_ ",
            "Mon numéro : 01.23.45.67.89",
        ),
        (
            "01 23 45 67 89 et 01.23.45.67.89", 
            " flag_phone_  et  flag_phone_ ",
            " flag_phone_  et  flag_phone_ ",
            "01 23 45 67 89 et 01.23.45.67.89",
        ),
        (
            "mon numéro01 23 45 67 89", 
            "mon numéro flag_phone_ ",
            "mon numéro flag_phone_ ",
            "mon numéro01 23 45 67 89",
        ),
        (
            "le montant du contrat est du 18000$, soit 17000euros",
            "le montant du contrat est du  flag_amount_ , soit  flag_amount_ ",
            "le montant du contrat est du  flag_amount_ , soit  flag_amount_ ",
            "le montant du contrat est du 18000$, soit 17000euros",
        ),
        (
            "J'habite au 1 rue de la paix, Paris 75002",
            "J'habite au 1 rue de la paix, Paris  flag_cp_ ",
            "J'habite au 1 rue de la paix, Paris 75002",
            "J'habite au 1 rue de la paix, Paris  flag_cp_ ",
        ),
        (
            "Rendez-vous le 18 décembre 2019 ou le 19/12/19 ou le 20.12.19 à 14h30",
            "Rendez-vous le  flag_date_  ou le  flag_date_  ou le  flag_date_  à  flag_time_ ",
            "Rendez-vous le  flag_date_  ou le  flag_date_  ou le  flag_date_  à 14h30",
            "Rendez-vous le 18 décembre 2019 ou le 19/12/19 ou le 20.12.19 à  flag_time_ ",
        ),
        (
            "le 14/12 tu me devras 20.05 dollars",
            "le  flag_date_  tu me devras  flag_amount_ ",
            "le  flag_date_  tu me devras  flag_amount_ ",
            "le 14/12 tu me devras 20.05 dollars",
        ),
        (
            "@Fabien On se voit tout à l'heure alors #apéro",
            " flag_mention_  On se voit tout à l'heure alors flag_hashtag_ ",
            " flag_mention_  On se voit tout à l'heure alors #apéro",
            "@Fabien On se voit tout à l'heure alors flag_hashtag_ ",
        ),
        (
            "On se revoit le 19 Juillet alors 😊. J'ai hâte 😁",
            "On se revoit le  flag_date_ alors 😊. J'ai hâte 😁",
            "On se revoit le  flag_date_ alors 😊. J'ai hâte 😁",
            "On se revoit le 19 Juillet alors  flag_emoji_ . J'ai hâte  flag_emoji_ ",
        ),
    ],
)
def test_flag_items(input_str, expected_str1,expected_str2,expected_str3):
    result1 = flag_items(input_str)
    result2 = flag_items(input_str, flagging_items=True, flag_list=[" flag_phone_ ", " flag_amount_ "," flag_date_ ", " flag_mention_ "], flagging_emojis=False)
    result3 = flag_items(input_str, flagging_items=False, flag_list=[" flag_phone_ ", " flag_amount_ "," flag_date_ ", " flag_mention_ "], flagging_emojis=True)
    np.testing.assert_string_equal(result1, expected_str1)
    np.testing.assert_string_equal(result2, expected_str2)
    np.testing.assert_string_equal(result3, expected_str3)
