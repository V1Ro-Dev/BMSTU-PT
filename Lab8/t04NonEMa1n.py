import random
from uzhas import vivod
pool = ["!", "*"]


def main():
    zal = {
        "forma": [['*'] * 10 for _ in range(10)],
        "tsena": 1
    }
    for i in range(10):
        zal["forma"][i] = [random.choice(pool) for _ in range(10)]

        
    kinoteatr_1 = {
        "nazvanie": "amogus",
        "maks_vmestimost": 1000,
        "informatsia": zal,
        "adres": "ulk bmstu",
        "formati": ["2D", "1488D"]
    }
    kinoteatr_2 = {
        "nazvanie": "lame",
        "maks_vmestimost": 1200,
        "informatsia": zal,
        "adres": "ulitsa_pushkina_dom_kalatushkina",
        "formati": ["3D", "1488D"]
    }
    film_1 = {
        "nazvanie": "bebra",
        "god": 2024,
        "zhanr": "boevik",
        "prodolzhitelnsot": 180,
        "format": "2D"
    }
    film_2 = {
        "nazvanie": "zzzsvo",
        "god": 2022,
        "zhanr": "boevik",
        "prodolzhitelnsot": 525600,
        "format": "1488D"
    }
    film_3 = {
        "nazvanie": "mikrodimid",
        "god": 2021,
        "zhanr": "melodramma",
        "prodolzhitelnsot": 120,
        "format": "3D"
    }
    seans_1 = {
        "kinoteatr": "amogus",
        "nazvanie_filma": "bebra",
        "vremya": "16:00"
    }
    seans_5 = {
        "kinoteatr": "lame",
        "nazvanie_filma": "bebra",
        "vremya": "10:00"
    }
    seans_2 = {
        "kinoteatr": "lame",
        "nazvanie_filma": "microdimid",
        "vremya": "17:30"
    }
    seans_3 = {
        "kinoteatr": "lame",
        "nazvanie_filma": "microdimid",
        "vremya": "21:30"
    }
    seans_4 = {
        "kinoteatr": "lame",
        "nazvanie_filma": "zzzsvo",
        "vremya": "00:00"
    }
    seans_6 = {
        "kinoteatr": "lame",
        "nazvanie_filma": "zzzsvo",
        "vremya": "09:00"
    }
    seans_7 = {
        "kinoteatr": "amogus",
        "nazvanie_filma": "zzzsvo",
        "vremya": "17:00"
    }

    client = {
        "fio": "MMD",
        "nomer_telephona": "89776655185",
        "po4ta": "",
        "budzhet": 1

    }
    spisok_clientov = []
    spisok_seansov = []
    spisok_filmov = []
    spisok_kinoteatrov = []
    spisok_zalov = []
    spisok_clientov.append(client)
    spisok_seansov.append(seans_1)
    spisok_seansov.append(seans_2)
    spisok_seansov.append(seans_3)
    spisok_seansov.append(seans_4)
    spisok_seansov.append(seans_5)
    spisok_seansov.append(seans_6)
    spisok_seansov.append(seans_7)
    spisok_filmov.append(film_1)
    spisok_filmov.append(film_2)
    spisok_filmov.append(film_3)
    spisok_kinoteatrov.append(kinoteatr_1)
    spisok_kinoteatrov.append(kinoteatr_2)
    spisok_zalov.append(zal)

    kriteriy = input("Vvedite kriteriy seansa: (время/название фильма: ").lower()
    if kriteriy == "время":
        vivod("Spisok vremeni po seansam: ")
        for seans in spisok_seansov:
            vivod(seans["vremya"])
        vremya = input("Vvedite vremya seansa f formate: (hh:mm)")
        vremena = []
        for seans in spisok_seansov:
            if vremya in seans.values():
                vremena.append(seans)
        if len(vremena) != 0:
            seans = vremena[0]
            nazvanie = seans["nazvanie_filma"]
            kinoteatr = seans["kinoteatr"]
            mesto = []
            for kinoteatr_ in spisok_kinoteatrov:
                if kinoteatr_["nazvanie"] == kinoteatr:
                    zall = kinoteatr_["informatsia"]
                    zalll = zall["forma"]
                    for i in range(10):
                        for j in range(10):
                            if zalll[i][j] != "!":
                                mesto = [i, j]
                                break
            print(f"Vi zabronirovali mesto v {seans["kinoteatr"]} na film {nazvanie} v {vremya}, vashe mesto: {mesto[0], mesto[1]}")
        else:
             vivod("takogo vremeni net")
    elif kriteriy == "название фильма":
        vivod("Spisok filmov po nazvaniyam: ")
        for film in spisok_filmov:
            vivod(film["nazvanie"])
        name = input("Vvedite nazvanie filma: ")
        names = []
        for seans in spisok_seansov:
            if name in seans.values():
                names.append(seans)
        if len(names) != 0:
            seans = names[0]
            nazvanie = seans["nazvanie_filma"]
            kinoteatr = seans["kinoteatr"]
            mesto = []
            for kinoteatr_ in spisok_kinoteatrov:
                if kinoteatr_["nazvanie"] == kinoteatr:
                    zall = kinoteatr_["informatsia"]
                    zalll = zall["forma"]
                    for i in range(10):
                        for j in range(10):
                            if zalll[i][j] != "!":
                                mesto = [i, j]
                                break
            print(
                f"Vi zabronirovali mesto v {seans["kinoteatr"]} na film {nazvanie} v {name}, vashe mesto: {mesto[0], mesto[1]}")
        else:
            vivod("Takogo filma net")




main()