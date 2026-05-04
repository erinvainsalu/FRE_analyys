import sys
import os

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Leia peakaust
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

# Impordi tabelite ja graafikute joonistamiseks vajalikud funktsioonid
from Python.visuaalide_abilised import maara_raporti_stiil
from Python.visuaalide_abilised import sagedustabel, mitmikvastuse_sagedustabel, loo_risttabel
from Python.visuaalide_abilised import loo_tulpdiagramm, loo_hor_tulpdiagramm, loo_stacked_tulpdiagramm, loo_hor_stacked_tulpdiagramm

# Määra graafikute stiil
style = maara_raporti_stiil()

# Impordi andmed puhastamise käigus loodud CVS-st
data = pd.read_csv('../Data/cleaned_data.csv')

# Impordi vastuste koodid
koodid = pd.read_csv('../Data/vastuste_koodid.csv')

# Kasuta laia paigutust
#st.set_page_config(layout='wide')

# Asenda väheste vastajate arvuga maakonnad valikuga muu
data_puhastatud = data.copy()
data_puhastatud['K5_elukoht'] = data['K5_elukoht'].replace([2, 3, 5, 6, 7, 8, 10, 11, 13, 15], 16)

st.title('Tarbijate teadlikkus')

st.write('Teadlikkus annab ülevaate tarbijate teadmistest, hoiakutest ja käitumisest, mis on seotud nende ostuotsuste ja tarbimisviiside mõjuga keskkonnale ning ühiskonnale. ' \
'See hõlmab arusaamist toodete elutsüklist, nende tootmise ja tarbimise tagajärgedest ning valikuid, mis aitavad vähendada jäätmeid ja soodustada ringmajandust. ' \
'Tekstiilide ja rõivaste kontekstis väljendub tarbijateadlikkus eelkõige valmisolekus teha teadlikke otsuseid rõivaste ostmisel, kasutamisel ja nende eluea lõpus vastutustundlikult käitlemises.')

st.write('## Teadlikkus 2025. aastal Eestis kehtima hakanud seadusest')

tab1, tab2 = st.tabs(['Graafik', 'Tabel (% vastanutest)'])
# Leia vastajate arv teadlikkuse alusel
teadlikkus = sagedustabel(data_puhastatud, koodid, 'K11_teadlikkus')

# Kuva tulpdiagramm
fig, ax = loo_hor_tulpdiagramm(
    teadlikkus,
    'Teadlikkus tekstiilijäätmete liigiti kogumise nõude osas',
    style,
    sort=True
)
tab1.pyplot(fig)
tab2.dataframe(teadlikkus,
    column_order=('vastus_lyhike', 'vastuste_arv', 'protsent_str'),
    column_config={
        'vastus_lyhike': st.column_config.TextColumn('Vastus'),
        'vastuste_arv': st.column_config.NumberColumn('Vastuste arv', width=20),
        'protsent_str': st.column_config.TextColumn('Protsent', alignment='right', width=20)
    },
    hide_index=True)

st.write('### Teadlikkus demograafiliste gruppide lõikes')

st.write('' \
'Joonis näitab tekstiilijäätmete liigiti kogumise seaduse teadlikkust vanusegruppide kaupa. ' \
'Tulemused näitavad, et nooremad vastajad on seadusest oluliselt vähem teadlikud.')

tab1, tab2 = st.tabs(['Graafik', 'Vastuste jaotus (%) tabelina'])

# Teadlikkus vanusegruppide alusel
teadlikkus_vanus = loo_risttabel(data_puhastatud, koodid, 'K3_vanus', 'K11_teadlikkus', normalize=True)

# Kuva tulpdiagramm
fig, ax = loo_stacked_tulpdiagramm(
    teadlikkus_vanus,
    'Teadlikkus seadusest vanuse alusel',
    style
)
tab1.pyplot(fig)
tab2.dataframe(teadlikkus_vanus)

st.write('Joonis näitab tekstiilijäätmete liigiti kogumise seaduse teadlikkust maakondade kaupa.')

tab1, tab2 = st.tabs(['Graafik', 'Vastuste jaotus (%) tabelina'])

# Teadlikkus elukoha alusel
teadlikkus_elukoht = loo_risttabel(data_puhastatud, koodid, 'K5_elukoht', 'K11_teadlikkus', normalize=True)

# Kuva tulpdiagramm
fig, ax = loo_stacked_tulpdiagramm(
    teadlikkus_elukoht,
    'Teadlikkus seadusest maakonniti',
    style
)

tab1.pyplot(fig)
tab2.dataframe(teadlikkus_elukoht)

st.write('### Teadlikkus vs hinnang enda teadmistele')

st.write('#### Tarbijate üldine hinnang enda teadmistele')
st.write('Tarbijatelt küsiti kuidas nad hindavad enda teadmisi jätkusuutlike valikute tegemisel rõivaste ja tekstiilide valdkonnas üleüldiselt.')

teadmiste_hinnang = sagedustabel(data_puhastatud, koodid, 'K8_teadmiste_hinnang')

fig, ax = loo_tulpdiagramm(
    teadmiste_hinnang,
    'Teadmiste hinnang',
    style
)
st.pyplot(fig)

# Teadmiste hinnang vanuse alusel
teadmised_vanus = loo_risttabel(data_puhastatud, koodid, 'K3_vanus', 'K8_teadmiste_hinnang')

fig, ax = loo_stacked_tulpdiagramm(
    teadmised_vanus,
    'Teadmiste hinnang vanuse alusel',
    style
)
st.pyplot(fig)

st.write('Kuna enda teadmiseid on madalamalt hinnanud eelkõige nooremad kasutajagrupid, siis tuleks teadmiseid tõsta just nendes vanusegruppides.')

st.write('#### Tarbijate üldine hinnang probleemi tõsidusele')

st.write('Tarbijatel paluti hinnata tekstiilijäätmete probleemi tõsidust Eestis ja globaalses mastaabis')

tosidus_vanus = loo_risttabel(data_puhastatud, koodid, 'K3_vanus', 'K9_probleemi_tosidus')

fig, ax = loo_stacked_tulpdiagramm(
    tosidus_vanus,
    'Probleemi tõsiduse hinnang vanuse alusel',
    style
)
st.pyplot(fig)

st.write('Graafikult on näha selge seos enda teadmiste hinnangu ning teadlikkuse vahel. ' \
'Inimestest, kes hindavad oma teadmisi kui **"Pigem hea"**, on 64% teadlikud uuest seadusest. ' \
'Inimeste hulgas, kes hindavad oma teadmisi kui **"Väga madal"**, ei ole 63% uuest seadusest teadlikud ning nende hulgas on 0% seadusest teadlikke.')

st.write('Kõigis enesehinnangu gruppides leidub 25-37% neid, kes on seadusest kuulnud, kuid ei ole täpsemalt kursis selle sisuga.')

st.write('Nende hulgas, kes hindasin oma teadmiseid väga madalaks või pigem madalaks on 53-63% neid, kes ei ole uuest seadusest teadlikud.')

# Teadlikkus × hinnang enda teadmistele
teadlikkus_teadmised = loo_risttabel(data_puhastatud, koodid, 'K8_teadmiste_hinnang', 'K11_teadlikkus')

fig, ax = loo_hor_stacked_tulpdiagramm(
    teadlikkus_teadmised, 
    'Teadlikkus seadusest enesehinnangu alusel',
    style
    #,sort=True
)

st.pyplot(fig)

# Statistiline analüüs: korrelatsioon teadlikkuse ja enesehinnangu vahel

st.write('### Teadlikkus vs probleemi tõsiduse hinnang')

st.write('Graafikult on näha seos enda probleemi tõsiduse hinnangu ning teadlikkuse vahel. ' \
'Inimestest, kes hindavad probleemi kui **"Väga tõsine"**, on 36-46% teadlikud uuest seadusest.')

#st.write('Kõigis enesehinnangu gruppides leidub 25-37% neid, kes on seadusest kuulnud, kuid ei ole täpsemalt kursis selle sisuga.')

#st.write('Nende hulgas, kes hindasin oma teadmiseid väga madalaks või pigem madalaks on 53-63% neid, kes ei ole uuest seadusest teadlikud.')


# Teadlikkus × Probleemi tõsidus
teadlikkus_probleem = loo_risttabel(data, koodid, 'K9_probleemi_tosidus', 'K11_teadlikkus')

fig, ax = loo_hor_stacked_tulpdiagramm(
    teadlikkus_probleem, 
    'Teadlikkus seadusest probleemi tõsiduse hinnangu alusel',
    style
    ,sort=True
)

st.pyplot(fig)

st.write('## KOV kommunikatsiooni selgus')

# Leia vastajate arv kommunikatsiooni selguse alusel
kommunikatsiooni_selgus = sagedustabel(data_puhastatud, koodid, 'K13_kommunikatsiooni_selgus')

# Kommunikatsiooni selguse jaotuse tulpdiagramm
fig, ax = loo_hor_tulpdiagramm(
    kommunikatsiooni_selgus,
    'KOV kommunikatsiooni selgus',
    style,
    sort=True
)

st.pyplot(fig)

# Kommunikatsiooni selgus elukoha alusel risttabel
kommunikatsioon_elukoht = loo_risttabel(data_puhastatud, koodid, 'K5_elukoht', 'K13_kommunikatsiooni_selgus')

fig, ax = loo_stacked_tulpdiagramm(
    kommunikatsioon_elukoht,
    'Kommunikatsiooni selgus maakonna alusel',
    style
)

st.pyplot(fig)

# Kas parem kommunikatsioon näitab kõrgemat teadlikkust seadusest?
selgus_teadlikkus = loo_risttabel(data_puhastatud, koodid, 'K13_kommunikatsiooni_selgus', 'K11_teadlikkus', normalize=True)

fig, ax = loo_hor_stacked_tulpdiagramm(
    selgus_teadlikkus,
    'Teadlikkus kommunikatsiooni selguse alusel',
    style
)

st.pyplot(fig)

# Leia vastuste jaotus - teabe allikate eelistused
teabe_allikad = mitmikvastuse_sagedustabel(data, koodid, 'K32_teabe_allikad')

fig, ax = loo_hor_tulpdiagramm(
    teabe_allikad,
    'Teabeallikad',
    style,
    sort=True   
)

st.pyplot(fig)

vanus_teabeallikas = data[[
    'K3_vanus',
    'K32_teabe_allikad_1',
    'K32_teabe_allikad_2',
    'K32_teabe_allikad_3',
    'K32_teabe_allikad_4',
    'K32_teabe_allikad_5',
    'K32_teabe_allikad_6',
    'K32_teabe_allikad_7',
    'K32_teabe_allikad_8',
    'K32_teabe_allikad_9',
    'K32_teabe_allikad_10']].groupby('K3_vanus').agg('sum')
vanus_teabeallikas

fig, ax = loo_stacked_tulpdiagramm(
    vanus_teabeallikas,
    '',
    style
)
st.pyplot(fig)