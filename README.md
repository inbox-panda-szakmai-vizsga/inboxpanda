# InboxPanda

Az InboxPanda olyan előfizetéses ügyfélszolgálati rendszer, amellyel egy vállalkozás élő chatet és kapcsolatfelvételi űrlapot építhet a meglévő weboldalába. Mindkét csatornáról a vállalkozás közös jegylistájába érkeznek a kérdések. A munkatársak látják, ki foglalkozik az üggyel, mit válaszoltak már az ügyfélnek, és melyik megkeresés vár még válaszra.

A projekt a **Szoftverfejlesztő és -tesztelő technikus** szakmai vizsgára készülő vizsgaremek. Jelenleg a tervezésnél tartunk. Az alábbiak a tervezett működést írják le.

## Felületek és szerepkörök

| Felület | Ki használja? | Mire szolgál? |
| --- | --- | --- |
| `inboxpanda.site` | Érdeklődő vállalkozástulajdonos | A nyilvános oldal bemutatja, hogyan működik a szolgáltatás a vállalkozás saját honlapján, és az előfizetés megkezdéséhez vezeti az érdeklődőt. |
| `inboxpanda.site/admin` | Az InboxPanda üzemeltetője | Áttekinti az előfizető vállalkozásokat, az előfizetéseket és a szolgáltatás használati statisztikáit. |
| `[vallalkozas].inboxpanda.site` | A vállalkozás ügyfele | Bármikor beléphet e-mailben kapott egyszer használatos kóddal (OTP), és megnézheti az ennél a vállalkozásnál nyitott saját jegyeit. |
| `[vallalkozas].inboxpanda.site/admin` | Az előfizető vállalkozás adminisztrátora és munkatársai | Az adminisztrátor itt állítja be a munkaterületet és hívja meg a kollégákat. A csapat itt kezeli a saját ügyfelei jegyeit. |
| A vállalkozás saját honlapja | A vállalkozás ügyfele | A látogató a beágyazott chatablakban kérdezhet, vagy a kapcsolatfelvételi oldalon küldhet üzenetet. |

## Önkiszolgáló előfizetés a vizsgademón

A vállalkozás tulajdonosa az `inboxpanda.site` oldalon regisztrál, kiválasztja a vállalkozás aldomainjét és a havi vagy éves előfizetést. A vizsgán a Stripe sandbox fizetési oldalán tesztkártyával járja végig a folyamatot, valódi pénzmozgás nélkül. [Stripe tesztfizetések](https://docs.stripe.com/testing)

Amikor a Stripe visszaigazolja az első sikeres fizetést, az InboxPanda automatikusan aktiválja a munkaterületet. A tulajdonos ekkor a választott aldomain `/admin` oldalán kezdheti el a beállítást. Az előfizetés megújítását és lemondását is automatikusan követi a rendszer.

## A beágyazástól a válaszig

1. **Beállítás.** Az előfizető saját munkaterületet kap. Az adminisztrátor megadja a vállalkozás webcímét, beállítja a chat üdvözlőszövegét, és meghívja a munkatársakat. A beállítási útmutató megmutatja, hová kell beilleszteni a chatablak és a kapcsolatfelvételi űrlap kódját.
2. **Megkeresés.** A chat automatikusan köszönti a látogatót, aki e-mail-cím nélkül is elküldheti az első üzenetét. Ezzel jegy nyílik, a munkatárs válasza pedig megjelenik a chatablakban. Ha az első ügyfélüzenettől számított 10 percig egyik munkatárs sem válaszol, a chat felajánlja az e-mailes folytatást. A látogató megadhatja a címét, hogy később ugyanabban az ügyben kapjon választ.

   A kapcsolatfelvételi űrlapon az ügyfél már a kérdés beküldésekor megadja az e-mail-címét. Ebből is jegy nyílik, a válasz e-mailben érkezik, és a levélre küldött viszontválasz ugyanahhoz a jegyhez kerül.
3. **Ügyintézés.** A munkatársak csatorna, állapot és felelős szerint szűrhetik a jegyeket. Egy munkatárs magához veheti az ügyet, válaszolhat az ügyfélnek, belső megjegyzést hagyhat a kollégáinak, majd lezárhatja a jegyet. A telefonra telepíthető munkatársi webalkalmazásból (PWA) ugyanezt a beszélgetést folytathatja.

4. **Jegyek követése.** Az ügyfél közvetlenül megnyithatja a vállalkozás ügyfélportálját, vagy követheti az űrlap beküldését visszaigazoló levélben kapott linket. A portálon megadja az e-mail-címét, majd az oda küldött kóddal belép. A jegylistában az aktuális és korábbi ügyei állapotát is láthatja.

## Lehetséges bővítések

- **Az előfizetők támogatása.** A vállalkozás adminisztrátora magával az InboxPandával kapcsolatban is nyithatna jegyet, például ha elakad a beágyazással. Ezeket a megkereséseket az InboxPanda üzemeltetői kezelnék a központi adminfelületen.

## A projekt felépítése

| Komponens | Technológia | Feladat |
| --- | --- | --- |
| `control-plane` | Laravel REST API | A SaaS üzemeltetői backendje. Nyilvántartja az előfizető vállalkozásokat, kezeli az előfizetéseket és a számlázást, feldolgozza a Stripe fizetési eseményeit, valamint adatokat szolgáltat az üzemeltetői statisztikákhoz. |
| `tenant-plane` | Laravel REST API | Az előfizető vállalkozások backendje. Kezeli a munkaterület beállításait, a munkatársak jogosultságait és a chatből vagy űrlapról érkező ügyfélszolgálati jegyeket. |
| `control-site` | Nuxt | Az `inboxpanda.site` nyilvános landing oldalát szerveroldalon rendereli (SSR). Ugyanez az alkalmazás adja az `inboxpanda.site/admin` üzemeltetői felületet, amely a `control-plane` API-t használja. |
| `tenant-site` | Nuxt | A vállalkozás aldomainjén az OTP-s ügyfélportált, az `/admin` útvonalon a munkatársi felületet adja. Mindkettő a `tenant-plane` API-t használja. |

A beágyazható elemek és a munkatársi PWA Vue-ra épülnek. Az üzenetek és a vállalkozások adatai PostgreSQL-be kerülnek.

## Projektdokumentáció

| Mappa | Tartalom |
| --- | --- |
| [docs/openapi](docs/openapi/) | A Laravel API-k OpenAPI-dokumentációjának helye. |
| [docs/design](docs/design/) | Fejlesztési terv és rendszertervezési dokumentumok. |
| [docs/database](docs/database/) | Adatmodell és ER-diagram. |
| [docs/testing](docs/testing/) | Teszttervek és tesztjegyzőkönyvek. |
| [docs/exam](docs/exam/) | Témaválasztás és vizsgához beadandó dokumentumok. |
