#pytest test_kavarna.py pro testování aplikace kavarna.py - obsahuje 5 testů pro třídy Osoba a Kavarna

import builtins
import pytest

from kavarna import Osoba, Kavarna


def test_osoba_attributes_and_print_info(capsys):
    o = Osoba("Alena", "čaj", False)
    assert o.jmeno == "Alena"
    assert o.oblibeny_napoj == "čaj"
    assert o.nalada is False

    o.print_info()
    captured = capsys.readouterr()
    assert "Jméno: Alena" in captured.out
    assert "Oblíbený nápoj: čaj" in captured.out


def test_kavarna_pridat_zakaznika_and_print(capsys):
    k = Kavarna("TestCafe", "Ulice 1")
    o = Osoba("Karel", "káva", True)
    k.pridat_zakaznika(o)
    assert k.zakaznici[-1] is o

    k.print_zakaznici()
    out = capsys.readouterr().out
    assert "Karel" in out


def test_objednej_napoj_available(capsys):
    k = Kavarna("C", "A")
    o = Osoba("Marta", "čaj", False)
    k.objednej_napoj(o, "čaj")
    out = capsys.readouterr().out
    assert "Marta si objednal(a) čaj za" in out
    assert "Nálada zákazníka Marta je nyní šťastná." in out


def test_objednej_napoj_unavailable(capsys):
    k = Kavarna("C", "A")
    o = Osoba("Luděk", "káva", True)
    k.objednej_napoj(o, "pivo")
    out = capsys.readouterr().out
    assert "Promiňte, pivo není v nabídce." in out


def test_objednej_napoj_od_uzivatele_interaction(monkeypatch, capsys):
    k = Kavarna("C", "A")
    o = Osoba("Zuzka", "espresso", False)

    # valid choice -> should return True and set nalada True
    monkeypatch.setattr(builtins, 'input', lambda prompt='': 'káva')
    res = k.objednej_napoj_od_uzivatele(o)
    out = capsys.readouterr().out
    assert res is True
    assert o.nalada is True
    assert "si objednal(a) káva za" in out

    # invalid choice -> should return False and keep nalada False
    o2 = Osoba("Honza", "čaj", False)
    monkeypatch.setattr(builtins, 'input', lambda prompt='': 'pivo')
    res2 = k.objednej_napoj_od_uzivatele(o2)
    out2 = capsys.readouterr().out
    assert res2 is False
    assert o2.nalada is False
    assert "není v nabídce" in out2
