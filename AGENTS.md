# InboxPanda – projektkontextus AI-ágenseknek

Az InboxPanda több vállalkozást kiszolgáló, előfizetéses ügyfélszolgálat. A projekt jelenleg tervezési fázisban van. A termék célját és a tervezett ügyfélutat a [README](README.md), a vizsgaremek vállalásait a [tématerv](docs/exam/InboxPanda%20-%20tématerv.docx), a felületek és a háttérfolyamatok kapcsolatait a [rendszerterv](docs/design/spec.excalidraw.svg) írja le.

## Melyik komponenshez tartozik a feladat?

| Terület | Backend | Webes felület |
| --- | --- | --- |
| SaaS-üzemeltetés | `control-plane` (Laravel) – előfizető vállalkozások, előfizetések, számlázás, Stripe-események és üzemeltetői statisztikák. | `control-site` (Nuxt) – az `inboxpanda.site` szerveroldalon renderelt (SSR) landing oldala és az `inboxpanda.site/admin` üzemeltetői felülete. |
| Előfizető vállalkozás és ügyfelei | `tenant-plane` (Laravel) – ügyfélhitelesítés OTP-vel, a vállalkozás beállításai, munkatársai, jogosultságai, jegyei és üzenetei. | `tenant-site` (Nuxt) – a `[vallalkozas].inboxpanda.site` főoldalán az ügyfélportál, az `/admin` útvonalon a munkatársi jegykezelés, a kezdeti beállítás és a beágyazási útmutató. |

Az `/admin` útvonal mindkét webalkalmazásban szerepel. A teljes domain és a felhasználó szerepe alapján válaszd ki az érintett komponenst. Például egy jegyszűrő felülete a `tenant-site`-hoz, a hozzá tartozó lekérdezés és jogosultság-ellenőrzés a `tenant-plane`-hez tartozik.

## Előfizetés és automatikus aktiválás

- A regisztráció a `control-site` felületén indul. A vállalkozás tulajdonosa aldomaint és számlázási időszakot választ. A `control-plane` indítja az előfizetést a Stripe-nál. A vizsgademóhoz a sandbox tesztkulcsait és tesztkártyáit használd. [Stripe tesztfizetések](https://docs.stripe.com/testing)
- A `control-plane` ellenőrzi a Stripe webhook aláírását, majd az első sikeres fizetés visszaigazolása és az aktív előfizetés alapján automatikusan aktiválja a vállalkozás munkaterületét. Az ismételten kézbesített esemény is ugyanahhoz a munkaterülethez tartozik. Megújításkor, sikertelen fizetéskor és lemondáskor a backend az előfizetés aktuális állapota alapján frissíti a nyilvántartást. [Stripe előfizetési események](https://docs.stripe.com/billing/subscriptions/webhooks)

## Szerepkörök és adathatárok

- **Üzemeltető (control plane).** Az `inboxpanda.site/admin` az InboxPandát működtető csapaté. Itt az előfizető vállalkozás és az előfizetés a kezelés tárgya. A nyilvános `inboxpanda.site` célközönsége a leendő előfizető.
- **Előfizető vállalkozás (tenant).** Egy vállalkozáshoz saját aldomain és munkaterület tartozik. A `[vallalkozas].inboxpanda.site/admin` alatt a vállalkozás adminisztrátora konfigurálja a beágyazást és hívja meg a kollégákat. A munkatársak a saját vállalkozásuk jegyeit kezelik weben és a PWA-ban. A jegyek listázásakor, megnyitásakor és módosításakor is érvényesíteni kell ezt a határt.
- **Végügyfél.** A vállalkozás honlapján chatel vagy űrlapot küld be. A beágyazókód határozza meg, melyik vállalkozás fogadja a megkeresést. Az ügyfél bármikor közvetlenül megnyithatja a vállalkozás aldomainjét és e-mailben egyszer használatos kódot kérhet. A visszaigazoló levélben kapott link ugyanerre a portálra vezet. A `tenant-plane` listázáskor és egyedi jegy megnyitásakor is az aktuális vállalkozásra és az OTP-vel igazolt e-mail-címhez tartozó jegyekre korlátozza a hozzáférést. A belső megjegyzések csak a munkatársaknak szólnak.

## Jegyek és üzenetek

- A chat első ügyfélüzenete e-mail-cím nélkül is jegyet nyit. Az űrlap beküldésekor a jegyhez már tartozik e-mail-cím.
- A 10 perces várakozás a jegyet megnyitó ügyfélüzenettől indul. Ha ennyi idő elteltével még nincs az ügyfélnek küldött munkatársi válasz, a chat e-mail-címet kér az e-mailes folytatáshoz. A várakozást csak az első ilyen válasz zárja le. A cím megadása önkéntes, és a meglévő jegyhez kapcsolja az e-mailes folytatást.
- A chatablakban adott válasz, az űrlapos ügyre küldött e-mail és a beérkező viszontválasz a megfelelő jegy előzményeihez tartozik. Egy már folyamatban lévő ügyben az e-mailes válasz megőrzi a beszélgetés folytonosságát.
- A webes és mobilos munkatársi felület ugyanazokat a jegyeket, felelősöket, állapotokat és üzeneteket kezeli.

## Tervezési keretek

- A tématerv a beágyazható elemekhez és a munkatársi PWA-hoz Vue-t, az adatok tárolásához PostgreSQL-t ír elő. A rendszerterv mindkét Laravel backendhez háttérfeldolgozót (queue worker) ábrázol, valamint Redist is jelöl.
- Az üzemeltetői jegykezelés opcionális bővítés. Ezen a felületen az előfizető vállalkozás kérhetne segítséget az InboxPanda csapatától.
