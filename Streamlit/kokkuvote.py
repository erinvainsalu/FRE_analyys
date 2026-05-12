import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Impordi tabelite ja graafikute joonistamiseks vajalikud funktsioonid
from Python.visuaalide_abilised import maara_raporti_stiil, leia_sildi_mapping
from Python.visuaalide_abilised import sagedustabel, mitmikvastuse_sagedustabel, loo_risttabel, loo_mitmikvastuse_risttabel
from Python.visuaalide_abilised import loo_tulpdiagramm, loo_hor_tulpdiagramm, loo_stacked_tulpdiagramm, loo_hor_stacked_tulpdiagramm, loo_heatmap

# Määra graafikute stiil
style = maara_raporti_stiil()

# Impordi andmed puhastamise käigus loodud CVS-st
data = pd.read_csv('data/cleaned_data.csv')

# Impordi vastuste koodid
koodid = pd.read_csv('data/vastuste_koodid.csv')

# Asenda väheste vastajate arvuga maakonnad valikuga muu
data_puhastatud = data.copy()
data_puhastatud['K5_elukoht'] = data['K5_elukoht'].replace([2, 3, 5, 6, 7, 8, 10, 11, 13, 15], 16)

st.title('Kokkuvõte uuringust')

st.write('Uuringus osales kokku 678 vastanut, küsimustikule vastamine võttis aega 5 - 10 minutit. ' \
'Kuna sotsiaalmeedia kanalid (nagu nt LinkedIn, Instagram, Facebook), kus uuringut enim jagati, on seotud kestliku rõivatarbimise info levitamisega, ' \
'siis võib eeldada, et sellest tulenevalt võib vaadelda käesoleva uuringu andmeid ja üldistusi teadliku tarbija seisukohast.')

st.write('3 peamist leidu')

st.write('soovitused teavitustegevusteks:')
st.write('    - piirkond, vanus, sugu?')
st.write('    - mis sisu võiks olla - kas hetkel on puudu teadmised, oskused vms')
st.write('soovitused “poliitika kujundamiseks” - kuidas tarbijate eelistuste alusel luua paremat tekstiilide sorteerimisvõrgustikku:')
st.write('    - miks tarbija hetkel ei sorteeri?')
st.write('    - mis teeks sorteerimise lihtsamaks? millised on eelistused?')

###################################################
# TEADLIKKUS SEADUSEST                            #
###################################################

st.write('## Teadlikkus 2025. aastal Eestis kehtima hakanud seadusest')

st.write('Uuringus osalejatelt küsiti nende teadlikkust 2025. aasta algul jõustunud seadusest. ' \
'Jõustunud seadusest oli teadlik 252 vastajat (39%), kusjuures 1% nendest leidis, et tegemist on valitsuse ja KOV-ide, mitte tarbijate probleemiga. ' \
'Ülejäänud 61% vastanutest jagunesid nendeks, kes ei ole seadusest teadlikud (28%) ning nendeks, kes on küll seadusest kuulnud, aga ei ole teadlikud detailidest (33%). ' \
'Kuigi 72% vastajatest on vähemalt ühel või teisel moel jõustunud seadusest kuulnud, siis siiski on palju teadmatust seoses seaduse ja selle täitmise üksikasjadega. ')

st.write('**Vastajate jaotus teadlikkuse lõikes**')

tab1, tab2 = st.tabs(['Graafik', 'Tabel'])
# Leia vastajate arv teadlikkuse alusel
teadlikkus = sagedustabel(data_puhastatud, koodid, 'K11_teadlikkus').sort_values(by='protsent', ascending=False)

highlight_categories = [
    'Olen kuulnud',
    'Ei ole teadlik'
]

# Kuva tulpdiagramm
fig, ax = loo_hor_tulpdiagramm(
    teadlikkus,
    '',
    style,
    sort=True
)

colors = ['#8B0000' if row['vastus_lyhike'] in highlight_categories else '#808080' 
          for _, row in teadlikkus.iterrows()]

for bar, color in zip(ax.patches, colors):
    bar.set_color(color)

tab1.pyplot(fig)
tab2.dataframe(teadlikkus,
    column_order=('vastus_lyhike', 'vastuste_arv', 'protsent_str'),
    column_config={
        'vastus_lyhike': st.column_config.TextColumn('Vastus'),
        'vastuste_arv': st.column_config.NumberColumn('Vastuste arv', width=20),
        'protsent_str': st.column_config.TextColumn('Protsent', alignment='right', width=20)
    },
    hide_index=True)

plt.savefig('Documentation/teadlikkus_seadusest.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close(fig)

###################################################
# KOMMUNIKATSIOONI SELGUS                         #
###################################################
st.write('## KOV kommunikatsiooni selgus')

st.write('Üle poole vastanutest ehk 436 inimest (65%) pidas KOV-ide kommunikatsiooni seoses 2025. aasta alguses kehtima hakanud tekstiilide liigiti kogumise nõudega puudulikuks. ' \
'116 vastajat (17%) pidas kommunikatsiooni arusaamatuks ning 102 (15%) leidis, et kommunikatsioon on olnud Selge, kuid mittetäielik. ' \
'Kõigest 14 inimest ehk 2% vastajatest peab KOV-ide kommunikatsiooni väga selgeks.')

st.write('**Vastajate jaotus kommunikatsiooni selguse lõikes**')

tab1, tab2 = st.tabs(['Graafik', 'Tabel'])

# Leia vastajate arv kommunikatsiooni selguse alusel
kommunikatsiooni_selgus = sagedustabel(data_puhastatud, koodid, 'K13_kommunikatsiooni_selgus')

highlight_categories = [
    'Puudulik',
    'Arusaamatu'
]

# Kommunikatsiooni selguse jaotuse tulpdiagramm
fig, ax = loo_tulpdiagramm(
    kommunikatsiooni_selgus,
    '',
    style
)

colors = ['#8B0000' if row['vastus_lyhike'] in highlight_categories else '#808080' 
          for _, row in kommunikatsiooni_selgus.iterrows()]

for bar, color in zip(ax.patches, colors):
    bar.set_color(color)

tab1.pyplot(fig)
tab2.dataframe(kommunikatsiooni_selgus,
    column_order=('vastus_lyhike', 'vastuste_arv', 'protsent_str'),
    column_config={
        'vastus_lyhike': st.column_config.TextColumn('Vastus'),
        'vastuste_arv': st.column_config.NumberColumn('Vastuste arv', width=20),
        'protsent_str': st.column_config.TextColumn('Protsent', alignment='right', width=20)
    },
    hide_index=True)

plt.savefig('Documentation/kommunikatsiooni_selgus.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close(fig)

###################################################
# MITTEVAJALIKUD TEKSTIILID                       #
###################################################
st.write('## Toimimine mittevajalike rõivaste ja tekstiilidega')

st.write('Mõistmaks, kuidas tarbija käitub kasutuskõlbulike rõivaste ja kodutekstiilidega, mida ta enam ei vaja, küsiti uuringus osalejatelt valikvastuste ja vabas vormis vastuse esitamise võimalusega mida vastajad selliste tekstiilidega ette võtavad. ' \
'Kõige sagedamini valiti korraga 3-4 põhjust, mis näitab, et korraga esineb mitu moodust kasutuskõlbulikest tekstiilidest loobumisel ja inimesed ei eelista ühte konkreetset viisi.')

st.write('Enamus vastanutest (82%) viib kasutuskõlblikud tekstiilid avalikesse kogumiskastidesse ja 72% annab need edasi perele või tuttavatele. ' \
'Veebis teisel ringil müümine (51%) ja ise tuunimine ning ümber tegemine (32%) on samuti levinud, mis näitab mitmekesiseid loobumisviise ja keskkonnateadlikku lähenemist. ' \
'Viimasele viitab ka see, et kõige sagedamini valiti koos vastusevariante: “müün veebis”, “annan perele/tuttavatele” ja “teen ise ümber”.')

st.write('Samas on 36% vastajatest toonud välja, et nad viskavad kasutuskõlbulikud tekstiilid segaolmejäätmetesse. ' \
'Vabatekstilistest vastustest tuleb välja, et sageli on tegemist katkiste ning määrdunud asjadega ehk tegelikult kasutuskõlbmatute rõivaste ja tekstiilidega. ' \
'Nenditi, et kuigi linnapildis on nähtud ja teatakse kantavate ja korralike riiete ning tekstiilide kogumispunkte, siis ei teata kuhu viia kasutuskõlbmatuid asju. ' \
'Ära visatavate esemetena toodi kõige enam välja just sokke ning aluspesu. Ehk vastustest tuleb välja, et olmeprügisse visatakse esemeid parema lahenduse või info puudumise tõttu. ' \
'Tuntakse muret ning huvi, mida teha just mainitud aluspesu ning sokkidega, mis liigituvad tekstiilijäätmeks, aga ei saa liikuda edasi teisele ringile oma esialgsel kujul. ' \
'See annab tugeva indikatsiooni parandada riigi ja KOV-ide kommunikatsiooni seoses tekstiilijäätmete sorteerimisega.')

st.write('**Käitumine mittevajalikest tekstiilidest loobumisel**')
tab1, tab2 = st.tabs(['Graafik', 'Tabel (% vastanutest)'])

mittevajalikud_tekstiilid = mitmikvastuse_sagedustabel(
    df_data=data_puhastatud, 
    df_koodid=koodid, 
    tunnus='K15_mittevajalikud_tekstiilid'
).sort_values(by='protsent', ascending=False)

highlight_categories = ['Viskan olmejäätmetesse']

fig, ax = loo_hor_tulpdiagramm(
    df=mittevajalikud_tekstiilid,
    title='',
    style_config=style,
    sort=True   
)

colors = ['#8B0000' if row['vastus_lyhike'] in highlight_categories else '#808080' 
          for _, row in mittevajalikud_tekstiilid.iterrows()]

for bar, color in zip(ax.patches, colors):
    bar.set_color(color)

tab1.pyplot(fig)
tab2.dataframe(mittevajalikud_tekstiilid,
    column_order=('vastus_lyhike', 'vastuste_arv', 'protsent_str'),
    column_config={
        'vastus_lyhike': st.column_config.TextColumn('Vastus'),
        'vastuste_arv': st.column_config.NumberColumn('Vastuste arv', width=20),
        'protsent_str': st.column_config.TextColumn('Protsent', alignment='right', width=20)
    },
    hide_index=True)

plt.savefig('Documentation/kasutuskolblikud_tekstiilid.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close(fig)

###################################################
# KASUTUSKÕLBMATUD TEKSTIILID                     #
###################################################
st.write('## Kasutuskõlbmatutest tekstiilidest loobumise viisid')

st.write('Selleks, et mõista kuidas tarbijad hetkel kasutuskõlbmatute tekstiilidega toimivad, küsiti kuhu peamiselt viiakse kasutuskõlbmatud rõivad ja tekstiilid. ' \
'Vastajal oli võimalik valida mitu vastusevarianti ning oma vastuseid vabatekstiväljal täpsustada. Kõige enam valiti korraga vaid 1 sobiv variant.')

st.write('Vastustes joonistub välja, et inimestel ei ole ühte selget viisi, mil moel kasutuskõlbmatute tekstiilidega kõige targemini toimetada. ' \
'Ülekaalukalt kõige sagedamini valiti segaolmejäätmete konteineritesse viimist (57%), mis ei ole nõuetekohane ega ka keskkonnasõbralik lahendus, kuid mis oli lubatud praktika enne 2025. aasta jaanuari. ' \
'Rõivakonteineritesse viimine (36%) on samuti levinud, kuigi neisse konteineritesse oodatakse vaid kasutuskõlbulikke rõivaid ja tekstiile. ' \
'Jäätmejaama viib ainult 14%, mis on õige viis, kuid selgelt alakasutatud. See näitab vajadust parema info järele kasutuskõlbmatute tekstiilide käitlemise kohta.')

st.write('**Vastajate jaotus kasutuskõlbmatutest tekstiilidest loobumise viiside alusel**')
tab1, tab2 = st.tabs(['Graafik', 'Tabel (% vastanutest)'])

kolbmatud = mitmikvastuse_sagedustabel(
    df_data=data_puhastatud, 
    df_koodid=koodid, 
    tunnus='K23_kasutuskolbmatud_tekstiilid'
).sort_values(by='protsent', ascending=False)

highlight_categories = [
    'Segaolmejäätmete konteiner',
    'Rõivakonteiner',
    'Põletamine (kodus)',
    'Matmine'
]

fig, ax = loo_hor_tulpdiagramm(
    df=kolbmatud,
    title='',
    style_config=style,
    sort=True   
)

colors = ['#8B0000' if row['vastus_lyhike'] in highlight_categories else '#808080' 
          for _, row in kolbmatud.iterrows()]

for bar, color in zip(ax.patches, colors):
    bar.set_color(color)

tab1.pyplot(fig)
tab2.dataframe(kolbmatud,
    column_order=('vastus_lyhike', 'vastuste_arv', 'protsent_str'),
    column_config={
        'vastus_lyhike': st.column_config.TextColumn('Vastus'),
        'vastuste_arv': st.column_config.NumberColumn('Vastuste arv', width=20),
        'protsent_str': st.column_config.TextColumn('Protsent', alignment='right', width=20)
    },
    hide_index=True)

plt.savefig('Documentation/kasutuskolbmatud_tekstiilid.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close(fig)