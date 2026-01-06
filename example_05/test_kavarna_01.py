import builtins
import pytest

from kavarna import Osoba, Kavarna


def test_osoba_attributes():
    o = Osoba("Alena", "čaj", False)
    assert o.jmeno == "Alena"
    assert o.oblibeny_napoj == "čaj"
    assert o.nalada is False


def test_print_info_outputs(capsys):
    o = Osoba("Boris", "káva", True)
    o.print_info()
    out = capsys.readouterr().out
    assert "Jméno: Boris" in out
    assert "Oblíbený nápoj: káva" in out


def test_kavarna_nabidka_contents():
    k = Kavarna("X", "Y")
    assert isinstance(k.nabidka, dict)
    assert "káva" in k.nabidka
    assert isinstance(k.nabidka["káva"], int)
    assert k.nabidka["káva"] > 0


def test_pridat_zakaznika_appends():
    k = Kavarna("T", "U")
    o = Osoba("Cyril", "čaj", False)
    assert len(k.zakaznici) == 0
    k.pridat_zakaznika(o)
    assert k.zakaznici[-1] is o


def test_print_zakaznici_shows_names(capsys):
    k = Kavarna("T", "U")
    o1 = Osoba("Dana", "káva", True)
    o2 = Osoba("Erik", "espresso", False)
    k.pridat_zakaznika(o1)
    k.pridat_zakaznika(o2)
    k.print_zakaznici()
    out = capsys.readouterr().out
    assert "Dana" in out and "Erik" in out


def test_objednej_napoj_available_does_print_and_not_change_attr(capsys):
    k = Kavarna("C", "A")
    o = Osoba("Marta", "čaj", False)
    k.objednej_napoj(o, "čaj")
    out = capsys.readouterr().out
    assert "Marta si objednal(a) čaj za" in out
    assert "Nálada zákazníka Marta je nyní šťastná." in out
    # implementation prints nalada text but does not modify attribute
    assert o.nalada is False


def test_objednej_napoj_unavailable_shows_apology(capsys):
    k = Kavarna("C", "A")
    o = Osoba("Luděk", "káva", True)
    k.objednej_napoj(o, "pivo")
    out = capsys.readouterr().out
    assert "Promiňte, pivo není v nabídce." in out


def test_objednej_napoj_od_uzivatele_valid(monkeypatch, capsys):
    k = Kavarna("C", "A")
    o = Osoba("Zuzka", "espresso", False)
    monkeypatch.setattr(builtins, 'input', lambda prompt='': 'káva')
    res = k.objednej_napoj_od_uzivatele(o)
    out = capsys.readouterr().out
    assert res is True
    assert o.nalada is True
    assert "si objednal(a) káva za" in out


def test_objednej_napoj_od_uzivatele_invalid(monkeypatch, capsys):
    k = Kavarna("C", "A")
    o = Osoba("Honza", "čaj", False)
    monkeypatch.setattr(builtins, 'input', lambda prompt='': 'pivo')
    res = k.objednej_napoj_od_uzivatele(o)
    out = capsys.readouterr().out
    assert res is False
    assert o.nalada is False
    assert "není v nabídce" in out


def test_objednej_napoj_od_uzivatele_input_normalization(monkeypatch, capsys):
    k = Kavarna("C", "A")
    o = Osoba("Klara", "káva", False)
    # input with extra spaces and uppercase accented letters should be handled
    monkeypatch.setattr(builtins, 'input', lambda prompt='': '  KÁva  ')
    res = k.objednej_napoj_od_uzivatele(o)
    out = capsys.readouterr().out
    assert res is True
    assert o.nalada is True
    assert "si objednal(a) káva za" in out
