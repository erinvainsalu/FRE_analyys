import sys
import os

import streamlit as st
import pandas as pd

# Leie peakaust
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

# Impordi tabelite ja graafikute joonistamiseks vajalikud funktsioonid
from Python.visuaalide_abilised import leia_sildi_mapping
from Python.visuaalide_abilised import sagedustabel

st.title('Tarbijate hoiakud tekstiilide liigiti kogumisel rõivastest ja kodutekstiilidest loobumisel')

st.write('Uuring "Tarbijate hoiakud tekstiilide liigiti kogumisel rõivastest ja kodutekstiilidest loobumisel" kutsuti ellu Jääk OÜ ehk Auli Uiboupini algatusel. ' \
'Uuringu peamiseks läbiviijaks oli Fashion Revolution Estonia MTÜ, nõuandvas rollis osales Kerli Kant Hvass (Revaluate OÜ).')

st.write('Fashion Revolution Estonia on osa ülemaailmselt liikumisest Fashion Revolution. ' \
'[Fashion Revolution](https://www.fashionrevolution.org/) on rahvusvaheline moeaktivismile suunatud organisatsioon, mis ühendab inimesi, kes panevad moetööstuse toimima. ' \
'Organisatsioon sündis pärast 2013. aastal Bangladeshis aset leidnud tootmishoone Rana Plaza varingut, mille käigus hukkus tuhandeid inimesi. ' \
'Tol hetkel sai selgeks, et moetööstus peab hakkama kasumi kõrvalt rohkem väärtustama inimesi ja planeeti. ')

st.write('[Fashion Revolution Estonia MTÜ](https://www.fashionrevolution.org/europe/estonia/) seisab tugevalt puhtama, turvalisema, eetilisema, läbipaistvama ja jätkusuutlikuma moetööstuse eest. ' \
'Fashion Revolution Estonia põhiline eesmärk on tuua tarbijateni suuremat teadlikkust jätkusuutliku moe tarbimisest, mis aitab igapäevaelus teha läbimõeldud otsuseid.')

st.write('Uuringu eesmärk oli mõista, millised on tarbijate käitumismustrid, nende vajadused ja väljakutsed kasutatud tekstiilidest loobumisel ning nende valmisolek tekstiile sorteerida enne nendest loobumist. ' \
'Soov oli kasutada kogutud tagasisidet üldisemalt tekstiilide kogumise ja ringlusse saatmise paremaks korraldamiseks Eestis. ' \
'Uuringu loomise põhjuseks on EL tekstiili strateegiast tulenev regulatsioon, mis muuhulgas näeb ette tekstiilijäätmete olmeprügist eraldi kogumise kohustuse. ' \
'Sellega seoses on alates 1. jaanuarist 2025 igal inimesel kohustus koguda tekstiilijäätmed muudest jäätmetest eraldi ning kohalik omavalitsus peab tagama võimaluse tekstiilijäätmeid omavalitsuse piires ära anda. ' \
'Samas on ka probleemiks tekstiilijäätmete suurenev keskkonnamõju ning vajadus arendada ringmajanduse põhimõtteid Eestis (seda nii üleriigiliselt kui väiksemate piirkondade pilootprojektide eesmärgil).')

st.write('Eestis ei ole varasemalt läbi viidud sarnast ulatuslikku uuringut, mis ühendaks tarbijate valmisoleku, kogumissüsteemide sobivuse ja keskkonnateadlikkuse. ' \
'Uuringu käigus koguti andmeid Google Forms vahendusel 2025. aastal perioodil 10. märts kuni 30. aprill ja uuringus osales kokku 668 vastanut. ' \
'Küsimustikule vastamine võttis aega 5 - 10 minutit. Kuna sotsiaalmeedia kanalid (nagu nt LinkedIn, Instagram, Facebook), kus uuringut enim jagati, on seotud kestliku rõivatarbimise info levitamisega, ' \
'siis võib eeldada, et sellest tulenevalt võib vaadelda käesoleva uuringu andmeid ja üldistusi teadliku tarbija seisukohast.')