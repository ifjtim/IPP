Dokumentace úlohy CHA: C Header Analysis v Python3 do IPP 2014/2015
Jméno a příjmení: Tomasz Konderla
Login: xkonde03

Zpracování parametrů:
Pro zpracovaní parametru cyklus, který mi prochází postupně zadané vstupní a parametry a vyhodnocuje je .
Cyklus zároveň prověřuje bezchybnost zadaných vstupu .

Načtení vstupních dat:
Skript prvně ověří jestli byla zadaná cesta, nebo konkretní soubor, zároveň se ověřuje jejích existence. Pokud
byla zadaná cesta skript pomoci funkce projit najde všechny hlavičkové soubory a vrátí cesty k ním v poli a
pokud byl zadán konkretní soubor do pole je nahraná pouze cesta k tomu konkretnímu souboru. Pak se dané
soubory analyzuji. Prvně se cely obsah souboru nahraje do proměnné obsah, pak se nahradí všechny konce
řádku za unixové konce řádku. Za druhé pomocí konečného automatu, který vidíte níže, se odstraní všechny
makra, řetězce, komentáře. Za třetí se zavolá funkce rosekej ta pomocí regulárních výrazu se najde všechny
funkce ty se rozdělí na jméno funkce, návratový typ funkce a parametry. U parametru spočítá kolik jích daná
funkce má a pomocí dalších regulárních výrazu najde jejích návratový typ. Pak tyto výsledky upraví podle
parametru ,které byly zadané (např odstraní inline funkce, odstraní duplikace...) a vypíše je do zadaného
výstupního souboru nebo na standardní vystup. V skriptu jsem použil pouze jednu globální proměnou a to
pole z názvy funkci, toto opatření jsem zvolil, protože jsem pozdě zapomněl na parametr odstranění
duplikací a toto bylo nejednoduší řešení tohoto problému.
