# Fakultatív feladat: többszintű ütemező megvalósítása

A globálisan preemptív, statikus prioritásos ütemező az alábbi ütemezési algoritmusokat futtatja az egyes szinteken az előadáson ismertetett módon:

1. magas prioritású szint (prioritás = 1) RR ütemező, időszelet: 2
2. alacsony prioritású szint (prioritás = 0) SRTF ütemező

## Bemenet (standard input, stdin)

Soronként egy (max. 10) taszk adatai. Egy sor felépítése (vesszővel elválasztva):

- a taszk betűjele (A, B, C...)
- a taszk prioritása (0 vagy 1)
- a taszk indítási ideje (egész szám >= 0), a következő időszeletben már futhat (0: az ütemező indításakor már létezik), azonos ütemben beérkező új taszkok esetén az ABC-sorrend dönt
- a taszk CPU-löketideje (egész szám >= 1)

### Példa:

A,0,0,6<br>
B,0,1,5<br>
C,1,5,2<br>
D,1,10,1

A bemenet végét EOF jelzi (előtte soremelés biztosan van, és üres sor is előfordulhat).

## Kimenet (standard output, stdout)

A kimenet első sorában a taszkok futási sorrendje betűjeleikkel (csak betűk, szóközök nélkül).
A második sorban a teljes várakozási idő taszkonként, érkezésük (nem feltétlenül abc-) sorrendjében, az alábbi formában (vesszővel elválasztva, szóközök nélkül):

<p>1. taszk betűjel:várakozási idő,2. betűjel:várakozási idő, ...

### Példa (a fenti bemenetre adott válasz):

ACABDB<br>
A:2,B:8,C:0,D:0

## Értékelés

Összesen 3 pont jár, ha minden teszten átmegy a megoldásuk. Arányosan kevesebb pont jár, ha nem minden esetben működik helyesen a programjuk.

## Tesztadatok

Az első beküldés előtt érdemes az alábbi egyszerű tesztekkel megpróbálkozni.

A,1,2,7<br>
B,1,2,3

ABABA<br>
A:3,B:4

Q,0,5,8<br>
P,1,7,2

QPQ<br>
Q:2,P:0

A,0,0,5<br>
B,0,0,4<br>
C,0,1,3<br>
D,0,2,1

BDBCA<br>
A:8,B:1,C:4,D:0

A,0,0,3<br>
B,1,0,2<br>
C,0,3,3<br>
D,1,4,1<br>

BADAC<br>
A:3,B:0,C:3,D:0

### Egy ráadás, kicsit fogósabb:

A,0,0,5<br>
B,0,1,3<br>
C,1,1,1<br>
D,0,4,1<br>
E,1,3,2

ACBEDBA<br>
A:7,B:4,C:0,E:0,D:1

### Végül egy vitatható eset:

A,1,3,5<br>
D,1,6,1

ADA<br>
A:1,D:1

Vitatható, hogy ha A időszelete lejár, akkor egy teljesen újat kezdhet (és emiatt D-nek várnia kell egy ütemet), vagy folytathatja a futást, de ha közben jön egy másik taszk (D), akkor azonnal átütemezés van. A megoldásban járjunk el úgy, hogy új időszeletet kezdhet, azaz 4 időegységig fut, majd jön D egy időegysége, és végül A maradék egy lépése!