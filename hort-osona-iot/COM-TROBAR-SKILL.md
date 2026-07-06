# Com trobar la skill "Hort Osona" a l'app Alexa

La skill "Hort Osona" està en **mode desenvolupament** (Development), per això
no surt a la botiga normal de Skills & Games. T'he de guiar al lloc correcte.

## Pas 1: Activar la skill com a developer

1. Obre l'app **Alexa** al teu iPhone
2. Toca **"More"** (el botó amb 3 línies horitzontals, a baix a la dreta)
3. Toca **"Skills & Games"**
4. A la pàgina de Skills, busca la **lupa 🔍** (a dalt a la dreta)
5. Escriu: **"Hort Osona"** o simplement **"Hort"**

⚠️ Si no surt res, és perquè la skill encara no s'ha publicat al teu compte.

## Pas 2: Forçar la vinculació (la clau!)

Això és el que la majoria de gent no sap. Has de fer login a Alexa amb el
**mateix compte Amazon** que vas usar per crear la skill a Developer Console.

1. A l'app Alexa, toca **"More"**
2. Toca **"Settings"**
3. Toca **"Your Account"**
4. Comprova que el **compte d'Amazon** que hi ha és el **mateix** que vas
   usar a https://developer.amazon.com/alexa/console/ask
5. Si NO és el mateix, **canvia'l** tocant "Sign out" i tornant a entrar
   amb el compte correcte

⚠️ Aquest és el **90% dels casos** de "no trobo la skill": la skill és al
compte developer però l'app Alexa està en un compte diferent.

## Pas 3: Veure les teves pròpies skills (developer skills)

Un cop tens el compte correcte:

1. **"More"** → **"Skills & Games"**
2. Toca la **lupa 🔍**
3. Cerca **"Hort Osona"**

Si encara no surt, fes-ho manualment:

1. **"More"** → **"Settings"**
2. **"Your Skills"** (o "Skills" en algunes versions)
3. Hauries de veure una secció **"Dev Skills"** o **"Your Custom Skills"**
4. Busca **"Hort Osona"** allà
5. Clica-la i toca **"Enable"**

## Pas 4: Si tot falla, fer un "Alexa, open hort osona" directe

L'app Alexa és molt lenta a indexar. A vegades el que funciona és:

1. Assegura't que el **Echo** (el teu "Eco") està en línia
2. Digues directament: **"Alexa, open hort osona"**
3. Si Alexa et contesta, ja està activada (no cal buscar-la a l'app)

## Pas 5: Si segueix sense aparèixer

Vés a **https://alexa.amazon.com** (la versió web) i:

1. Fes login amb el **mateix compte Amazon**
2. A dalt, busca **"Skills"** al menú
3. Clica **"Your Skills"** (al submenú)
4. Hauries de veure **"Hort Osona"** a la llista
5. Clica **"Enable"**

## Solució ràpida: demana a Alexa directament

Si tens el teu Amazon Eco a prop, simplement digues:

```
Alexa, open hort osona
```

Si Alexa diu alguna cosa com "Welcome to Hort Osona" o similar, la skill ja
està activada al teu compte. Si diu "I can't find that skill", aleshores
hem de fer el pas 2 (comprovar el compte).

## Resum ràpid

| On | Què |
|---|---|
| App Alexa → More → Skills & Games | Skills públiques (NO la teva) |
| App Alexa → More → Settings → Your Skills | Les teves skills developer |
| https://alexa.amazon.com → Your Skills | Versió web (sol funcionar millor) |
| Directament amb veu: "Alexa, open hort osona" | Mètode més ràpid |

Si cap d'aquests passos funciona, comparteix-me:
- L'**email** del compte que tens a l'app Alexa
- L'**email** del compte que vas usar a developer.amazon.com
- Si són **diferents**, és clarament un problema de compte
