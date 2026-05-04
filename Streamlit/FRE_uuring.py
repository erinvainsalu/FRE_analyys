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