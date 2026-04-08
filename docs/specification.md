# Specifikace

## Název

Reachability in Discrete All-Pay Bidding Games

## Popis problému

### Bidding games

Bidding games představují třídu her dvou hráčů s nulovým součtem hraných na orientovaných grafech.
Hra probíhá tak, že je na počáteční uzel grafu umístěn žeton a hráči se jej snaží přesouvat.
Na začátku hry je oběma hráčům přiřazen omezený rozpočet.
V každém kole oba hráči současně podají nabídku a hráč s vyšší nabídkou pohne žetonem.

V tomto projektu při stejných nabídkách hýbe žetonem Hráč 1.

V rachability games Hráč 1 vyhrává právě tehdy když se žeton dostane do předem určeného cílového vrcholu.

### Varianty bidding games

Dále se bidding games dělí podle tří hlavních pravidel:

#### Kdo platí

- **first-price**: platí pouze vítěz
- **all-pay**: platí oba hráči

#### Komu se platí

- **Richman**: platí se druhému hráči
- **Poorman**: platí se do banky

#### Typ nabídek

- **diskrétní**: nabídky musí být celočíselné
- **spojité**: nabídky nemusí být celočíselné

Tento projekt se zaměřuje primárně na diskrétní all-pay bidding games.

### Prahové rozpočty

- **Výherní práh** v daném vrcholu grafu představuje minimální počáteční rozpočet, který Hráč 1 nezbytně potřebuje k tomu, aby si garantoval vítězství proti konkrétnímu počátečnímu rozpočtu Hráče 2.

### Reference

- Avni, Ibsen-Jensen, Tkadlec (2020). All-Pay Bidding Games on Graphs. Proc. 34th AAAI, 1798--1805.
- Avni, Meggendorfer, Sadhukhan, Tkadlec, Žikelić (2023). Reachability Poorman Discrete-Bidding Games. ECAI 2023.

## Cíle projektu

### Hlavní cíl

Implementace C++ solveru pro výpočet výherních prahů pro diskrétní all-pay Poorman bidding games pomocí dynamického programování.

### Možná rozšíření

- Výpočet pravděpodoností výsledku při optimálních strategiích obou hráčů v nerozhodnutých konfiguracích
- Richman
- Python API: pybind

## Technologie

### Jazyk

- C++23

### Knihovny

- [HiGHS](https://github.com/ERGO-Code/HiGHS)

### Build system

- CMake

### Operační systém

- Windows, MacOS, Linux

## Rozhraní

### Uživatelské rozhraní

- Konzolová aplikace

### Vstup/Výstup

- **Vstup**: bidding game, vrchol, rozpočet Hráče 2
- **Výstup**: výherní práh

### Generování her

Součástí programu bude generátor základních typů her (např. Race, Tug-of-War).
