import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
import numpy as np

#custom_params = {"axes.spines.right": False, "axes.spines.top": False}
#sns.set_theme(style = 'whitegrid', rc = custom_params)

def maara_raporti_stiil():

    sns.set_theme(style='whitegrid')

    plt.rcParams.update({
        # font
        #"font.family": "sans-serif",
        'font.size': 10,
        'axes.titlesize': 13,
        'axes.labelsize': 10,

        # telgede stiil
        'axes.spines.top': False,
        'axes.spines.right': False,
        'axes.spines.left': False,

        # grid
        #"axes.grid": True,
        'grid.linestyle': '--',
        'grid.alpha': 0.4,

        # legend
        'legend.frameon': False,

        # figure
        #"figure.dpi": 120
    })
    
    return {
        # Defineeri värvipalett
    #PALETTE = ["#3B5BA5", "#55A868", "#C44E52", "#8172B3", "#CCB974"]
    # PALETTE = ["#1B1F3B", "#00429D", "#006D5B", "#2E7D32", "#8E24AA", '#B71C1C', '#C05600', '#37474F'] # dark palette

        'PALETTE': [
            '#3B5BA5',  # blue (original)
            '#2A9D8F',  # teal (clearly different from blue)
            '#55A868',  # green (original)
            '#C44E52',  # red (original anchor)
            '#F4A261',  # muted orange
            '#8172B3',  # purple (original)
            '#8D6E63',  # muted brown
            '#7F7F7F'   # neutral grey
        ],
        'PRIMARY_COLOR': '#3B5BA5'
    }

def leia_sildi_mapping(df_koodid, tunnus):
     return (
        df_koodid[df_koodid['kysimus'] == tunnus]
        .set_index('kood')['vastus_lyhike']
        .to_dict()
    )

# Loo ühe tunnuse osas andmetabel vastuste absoluut- ja suhtarvudega
def sagedustabel(df_data, df_koodid, tunnus, use_full_codebook=True):
    
    # --- counts from data ---
    counts = df_data[tunnus].value_counts()

    if use_full_codebook:
        # use full list of possible answers
        df_map = df_koodid[df_koodid['kysimus'] == tunnus].copy()

        # ensure all codes appear
        df_map['vastuste_arv'] = df_map['kood'].map(counts).fillna(0).astype(int)

    else:
        # use only observed values (partial mode)
        df_map = counts.reset_index()
        df_map.columns = ['kood', 'vastuste_arv']

        # optionally merge labels if available
        labels = df_koodid[df_koodid['kysimus'] == tunnus][['kood', 'vastus_lyhike']]
        df_map = df_map.merge(labels, on='kood', how='left')

    # --- percentages ---
    total = df_map['vastuste_arv'].sum()
    df_map['protsent'] = (df_map['vastuste_arv'] / total * 100).round(0).astype(int) if total > 0 else 0
    df_map['protsent_str'] = df_map['protsent'].map(lambda x: f'{x:.0f}%')

    return df_map[['kood', 'vastus_lyhike', 'vastuste_arv', 'protsent', 'protsent_str']]

# Loo mitmikvastusega tunnuse osas andmetabel vastuste absoluut- ja suhtarvudega
def mitmikvastuse_sagedustabel(df_data, df_koodid, tunnus):
    # Leia võimalike vastusevariantide arv
    ridade_arv = len(df_koodid[df_koodid['kysimus'] == tunnus])
    
    # Leia vastajate arv (kes valis vähemalt ühe vastuse)
    cols = [f'{tunnus}_{i}' for i in range(1, ridade_arv+1)]
    vastajate_arv = (df_data[cols].sum(axis=1) > 0).sum()
    
    # Filtreeri koodid
    df_tunnus = df_koodid[df_koodid['kysimus'] == tunnus].copy()
    
    # Loo tulemustabel
    tulemus = pd.DataFrame({
        'kood': range(1, ridade_arv+1),
        'vastus_lyhike': df_tunnus['vastus_lyhike'].values,
        'vastuste_arv': [df_data[f'{tunnus}_{i}'].sum() for i in range(1, ridade_arv+1)]
    })
    
    tulemus['protsent'] = (tulemus['vastuste_arv'] / vastajate_arv * 100).round(0).astype(int) if vastajate_arv > 0 else 0
    tulemus['protsent_str'] = tulemus['protsent'].astype(int).astype(str) + '%'
    
    return tulemus

# Loo kahe tunnuse risttabel
def loo_risttabel(df, df_koodid, tunnus_rida, tunnus_veerg, normalize=False):
    if normalize:
        risttabel = pd.crosstab(
            index=df[tunnus_rida],
            columns=df[tunnus_veerg],
            normalize='index'
        ) * 100
        risttabel = risttabel.round(0)
    else:
        risttabel = pd.crosstab(
            index=df[tunnus_rida],
            columns=df[tunnus_veerg]
        )
    
    # Leia koodide tabelist koodidele vastavad nimetused ridade/veergude pealkirjadeks
    row_map = leia_sildi_mapping(df_koodid, tunnus_rida)
    col_map = leia_sildi_mapping(df_koodid, tunnus_veerg)

    # Asenda koodid neile vastavate nimetustega
    risttabel.index = risttabel.index.map(lambda x: row_map.get(x, x))
    risttabel.columns = risttabel.columns.map(lambda x: col_map.get(x, x))

    return risttabel

# Loo kahe tunnuse risttabel, kus üks tunnustest on mitmikvalikuga

# Loo vertikaalne tulpdiagramm
def loo_tulpdiagramm(df, title, style_config, percent=True, sort=False):
    
    # Vajadusel sorteeri andmestik
    if sort:
        df = df.sort_values("protsent", ascending=False)
    
    #print('Vastuste jaotus:')
    #print(df.to_string(index=False))
    
    fig, ax = plt.subplots(figsize=(7, 5))

    # Loo diagramm
    sns.barplot(
        data=df,
        x='vastus_lyhike',
        y='protsent' if percent else 'vastuste_arv', # kasutaja kas suhtarve või absoluutseid väärtuseid
        color=style_config['PRIMARY_COLOR'],
        ax=ax
    )
    
    # Lisa pealkiri
    ax.set_title(title, weight='bold', loc='left', pad=15)
    
    # Eemalda telgede nimed
    ax.set(xlabel=None, ylabel=None)

    # Kui diagrammil kuvatud suhtarvud, siis muuda y-telg protsentideks
    if percent:
        ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
        # Seadista graafiku max
        ax.set_ylim(0, df['protsent'].max() * 1.15)
        #ax.set_ylim(0, max(100, df["protsent"].max() * 1.15))
    
    # Kuva minimalistlik grid
    ax.grid(axis="x", visible=False)
 
    # Lisa diagrammile tekstilised annotatsioonid
    for idx, row in enumerate(df.itertuples()):
        label = f'{row.protsent:.0f}% ({row.vastuste_arv})'
        
        ax.text(
            idx,
            row.protsent + 1,
            label,
            horizontalalignment='center',
            verticalalignment='bottom',
            fontsize=10
        )
    
    plt.tight_layout()
    
    return fig, ax

# Loo horisontaalne tulpdiagramm
def loo_hor_tulpdiagramm(df, title, style_config, percent=True, sort=False):
    
    # Vajadusel sorteeri andmestik
    if sort:
        df = df.sort_values("protsent", ascending=False)
    
    #print('Vastuste jaotus:')
    #print(df.to_string(index=False))
    
    fig, ax = plt.subplots(figsize=(7, 5))

    # Loo diagramm
    sns.barplot(
        data=df,
        x='protsent' if percent else 'vastuste_arv', # kasutaja kas suhtarve või absoluutseid väärtuseid
        y='vastus_lyhike',
        color=style_config['PRIMARY_COLOR'],
        ax=ax
    )
    
    # Lisa pealkiri
    ax.set_title(title, weight='bold', loc='left', pad=15)
    
    # Eemalda telgede nimed
    ax.set(xlabel=None, ylabel=None)

    # Kui diagrammil kuvatud suhtarvud, siis muuda x-telg protsentideks
    if percent:
        ax.xaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
        # Seadista graafiku max
        ax.set_xlim(0, df['protsent'].max() * 1.15)
    
    # Kuva minimalistlik grid
    ax.grid(axis='y', visible=False)
 
    # Lisa diagrammile tekstilised annotatsioonid
    for idx, row in enumerate(df.itertuples()):
        label = f'{row.protsent:.0f}% ({row.vastuste_arv})'
        
        ax.text(
            row.protsent + 0.5,
            idx,
            label,
            horizontalalignment='left',
            verticalalignment='center',
            fontsize=10
        )
    
    plt.tight_layout()
    
    return fig, ax

# Loo vertikaalne "stacked" tulpdiagramm
def loo_stacked_tulpdiagramm(df, title, style_config, normalize=True):
    if normalize:
        # Teisenda absoluutarvud protsentideks
        df_plot = df.div(df.sum(axis=1), axis=0)
    else:
        df_plot = df.copy()
    
    #print(f'\nVastuste arv: {df.sum().sum()}')
    #print(f'Vastuste arv tunnuste kaupa:')
    #print(df.sum(axis=1))

    # Loo stacked tulpdiagramm
    fig, ax = plt.subplots(figsize=(7, 5))
    
    df_plot.plot(
        kind='bar',
        stacked=True,
        color=style_config['PALETTE'],
        ax=ax,
        width=0.8
    )

    ax.set_title(title, weight='bold', loc='left', pad=15)
    ax.set(xlabel=None, ylabel=None)
    #ax.set_xlabel('Vanusegrupp', fontsize=13, fontweight='bold')
    #ax.set_ylabel('Protsent (%)', fontsize=13, fontweight='bold')

    # Kui diagrammil kuvatud suhtarvud, siis muuda y-telg protsentideks
    if normalize:
        ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))
        ax.set_ylim(0, 1)
    
    # x-telg
    ax.set_xticklabels(df.index, rotation=0, ha='center')

    # Lisa segmentidele neile vastavad protsendid sildina
    for container in ax.containers:
        # Kuva silte ainult juhul kui >5
        labels = [f'{v*100:.0f}%' if v*100 > 5 else '' for v in container.datavalues]
        ax.bar_label(
            container,
            labels=labels,
            label_type='center',
            fontsize=9
        )

    # Legendi stiil
    ax.legend(
        bbox_to_anchor=(0.5, -0.1),
        loc="upper center",
        fontsize=9,
        #frameon=False,
        ncol=len(df.columns) # kuva kõik nimetused ühel real
    )

    # Lisa diagrammile x-telje alla vastuste arvudele vastavad sildid
    #for i, (grupp, count) in enumerate(df.sum(axis=1).items()):
    #    ax.text(
    #        i,
    #        -0.12,
    #        f'n={count}',
    #        ha='center',
    #        #va='top', 
    #        fontsize=9,
    #        style='italic',
    #        color='gray'
    #    )

    plt.tight_layout()
    #plt.savefig('/mnt/user-data/outputs/stacked_bar_final.png', dpi=300, bbox_inches='tight', facecolor='white')

    return fig, ax

# Loo horisontaalne "stacked" tulpdiagramm
def loo_hor_stacked_tulpdiagramm(df, title, style_config, normalize=True, sort=True):
    
    if normalize:
        # Teisenda absoluutarvud protsentideks
        df_plot = df.div(df.sum(axis=1), axis=0)
    else:
        df_plot = df.copy()
    
    # Vajadusel sorteeri andmestik
    if sort:
        df = df.loc[df.sum(axis=1).sort_values(ascending=True).index]
    
    #print(f'\nVastuste arv: {df.sum().sum()}')
    #print(f'Vastuste arv tunnuste kaupa:')
    #print(df.sum(axis=1))

    # Loo stacked tulpdiagramm
    fig, ax = plt.subplots(figsize=(7, 6))
    
    df_plot.plot(
        kind="barh",
        stacked=True,
        color=style_config['PALETTE'],
        ax=ax
    )

    #ax.margins(y=0.1)

    ax.set_title(title, weight='bold', loc='left', pad=15)
    ax.set(xlabel=None, ylabel=None)

    # Kui diagrammil kuvatud suhtarvud, siis muuda x-telg protsentideks
    if normalize:
        ax.xaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))
        ax.set_xlim(0, 1)

    # y-telg
    ax.set_yticklabels(df.index)
    if not sort:
        ax.invert_yaxis()

    # Lisa segmentidele neile vastavad protsendid sildina
    for container in ax.containers:
        labels = [
            f'{v*100:.0f}%' if (normalize and v*100 > 5)
            else (f'{int(v)}' if not normalize and v > 0 else '')
            for v in container.datavalues
        ]
        
        ax.bar_label(
            container,
            labels=labels,
            label_type='center',
            fontsize=8
        )

    # Legendi stiil
    ax.legend(
        bbox_to_anchor=(0.5, -0.1),
        loc="upper center",
        fontsize=9,
        #frameon=False,
        ncol=len(df.columns) # kuva kõik nimetused ühel real
    )

    # Lisa absoluutarvude sildid vasakule
    totals = df.sum(axis=1)
    
    # Lisa diagrammile y-telje juurde vastuste arvudele vastavad sildid
    for i, (grupp, count) in enumerate(totals.items()):
        ax.text(
            -0.03,
            i-0.5,
            f'(n={count})',
            transform=ax.get_yaxis_transform(),
            ha='right',
            va='center',
            fontsize=8,
            style='italic',
            color='gray'
        )

    # --- clean grid ---
    #ax.grid(axis='x', linestyle='--', alpha=0.4)
    #ax.grid(axis='y', visible=False)

    plt.tight_layout()

    return fig, ax

def loo_diverging_stacked_tulpdiagramm(
    data, 
    pealkiri, 
    negatiivne_veerud=None,
    neutraalne_veerg=None, 
    positiivne_veerud=None,
    negatiivne_varvid=None,
    neutraalne_varv='#ffe5b4',
    positiivne_varvid=None,
    naita_protsente=True,
    figsize=(12, 8),
    xlabel='Vastajate osakaal (%)'
):
    """
    Loob diverging stacked bar diagrammi ordinaalse Likert-skaala andmete jaoks.
    Neutraalne väärtus on keskele jaotatud (pool paremale, pool vasakule).
    
    Parameetrid:
    -----------
    data : pd.DataFrame
        Andmed kus esimene veerg on kategooriad, ülejäänud veerud on vastuste arvud
    pealkiri : str
        Diagrammi pealkiri
    negatiivne_veerud : list
        Negatiivsete vastuste veergude nimed (väiksemast suuremani)
        Näide: ['Probleem puudub', 'Väike probleem']
    neutraalne_veerg : str
        Neutraalse vastuse veeru nimi
        Näide: 'Keskmine'
    positiivne_veerud : list
        Positiivsete vastuste veergude nimed (väiksemast suuremani)
        Näide: ['Pigem tõsine', 'Väga tõsine']
    negatiivne_varvid : list, optional
        Värvid negatiivsetele vastustele (heledamast tumedamani)
    neutraalne_varv : str, optional
        Värv neutraalsele vastusele (default: beež)
    positiivne_varvid : list, optional
        Värvid positiivsetele vastustele (heledamast tumedamani)
    naita_protsente : bool, optional
        Kas näidata protsentide numbreid (default: True)
    figsize : tuple, optional
        Joonise suurus (default: (12, 8))
    xlabel : str, optional
        X-telje nimetus
        
    Tagastab:
    --------
    fig, ax : matplotlib figure ja axes objektid
    
    Näide:
    ------
    >>> fig, ax = loo_diverging_stacked_tulpdiagramm(
    ...     probleem_vanus,
    ...     'Tekstiilijäätmete probleemi tõsidus vanusegruppide lõikes',
    ...     negatiivne_veerud=['Probleem puudub', 'Väike probleem'],
    ...     neutraalne_veerg='Keskmine',
    ...     positiivne_veerud=['Pigem tõsine', 'Väga tõsine']
    ... )
    """
    
    # Vaikimisi värvid
    if negatiivne_varvid is None:
        # Heledast tumedani: hall/sinine negatiivne pool
        negatiivne_varvid = ['#d1d3d4', '#92a8b8']
    
    if positiivne_varvid is None:
        # Heledast tumedani: oranž/punane positiivne pool
        positiivne_varvid = ['#f4a582', '#ca0020']
    
    # Kontrolli, et on piisavalt värve
    if negatiivne_veerud and len(negatiivne_varvid) < len(negatiivne_veerud):
        raise ValueError(f"Vajab {len(negatiivne_veerud)} negatiivset värvi, anti {len(negatiivne_varvid)}")
    
    if positiivne_veerud and len(positiivne_varvid) < len(positiivne_veerud):
        raise ValueError(f"Vajab {len(positiivne_veerud)} positiivset värvi, anti {len(positiivne_varvid)}")
    
    # Arvuta protsendid
    df_pct = data.copy()
    
    # Esimene veerg on kategooriad, ülejäänud on vastused
    vastuse_veerud = [col for col in data.columns if col != data.columns[0]]
    
    # Arvuta iga rea summa
    df_pct['_summa'] = data[vastuse_veerud].sum(axis=1)
    
    # Arvuta protsendid
    for col in vastuse_veerud:
        df_pct[col] = (data[col] / df_pct['_summa']) * 100
    
    # Loo joonis
    fig, ax = plt.subplots(figsize=figsize)
    
    # Kategooriad (y-telg)
    kategooriad = df_pct[df_pct.columns[0]].values
    y_pos = np.arange(len(kategooriad))
    
    # ===== VASAKPOOLNE KÜLG (NEGATIIVNE) =====
    vasak_kumulatiivne = np.zeros(len(df_pct))
    
    # Lisa negatiivne pool (pööratud järjekorras, et kõige tugevam oleks kõige väljaspool)
    if negatiivne_veerud:
        for i, veerg in enumerate(reversed(negatiivne_veerud)):
            vaartused = -df_pct[veerg].values
            varv_idx = len(negatiivne_veerud) - 1 - i
            ax.barh(y_pos, vaartused, left=vasak_kumulatiivne, 
                    color=negatiivne_varvid[varv_idx], 
                    edgecolor='white', linewidth=0.5,
                    label=veerg)
            vasak_kumulatiivne += vaartused
    
    # Lisa pool neutraalsest vasakule
    if neutraalne_veerg:
        neutraalne_vasak = -df_pct[neutraalne_veerg].values / 2
        ax.barh(y_pos, neutraalne_vasak, left=vasak_kumulatiivne, 
                color=neutraalne_varv, 
                edgecolor='white', linewidth=0.5,
                label=neutraalne_veerg)
        vasak_kumulatiivne += neutraalne_vasak
    
    # ===== PAREMPOOLNE KÜLG (POSITIIVNE) =====
    parem_kumulatiivne = np.zeros(len(df_pct))
    
    # Lisa pool neutraalsest paremale
    if neutraalne_veerg:
        neutraalne_parem = df_pct[neutraalne_veerg].values / 2
        ax.barh(y_pos, neutraalne_parem, left=parem_kumulatiivne, 
                color=neutraalne_varv,
                edgecolor='white', linewidth=0.5)
        parem_kumulatiivne += neutraalne_parem
    
    # Lisa positiivne pool
    if positiivne_veerud:
        for i, veerg in enumerate(positiivne_veerud):
            vaartused = df_pct[veerg].values
            ax.barh(y_pos, vaartused, left=parem_kumulatiivne, 
                    color=positiivne_varvid[i], 
                    edgecolor='white', linewidth=0.5,
                    label=veerg)
            parem_kumulatiivne += vaartused
    
    # ===== VORMINDUS =====
    
    # Y-telg (kategooriad)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(kategooriad, fontsize=11)
    
    # X-telg
    ax.set_xlabel(xlabel, fontsize=12, fontweight='bold')
    
    # Pealkiri
    ax.set_title(pealkiri, fontsize=14, fontweight='bold', pad=20)
    
    # Nulljoon
    ax.axvline(0, color='black', linewidth=1.2, zorder=10)
    
    # Määra sümmeetriline X-telg
    max_vasak = abs(vasak_kumulatiivne.min())
    max_parem = parem_kumulatiivne.max()
    max_abs = max(max_vasak, max_parem)
    
    ax.set_xlim(-max_abs * 1.05, max_abs * 1.05)
    
    # Muuda X-telje sildid positiivseteks (absoluutväärtused)
    xticks = ax.get_xticks()
    ax.set_xticks(xticks)
    ax.set_xticklabels([f'{abs(x):.0f}' for x in xticks], fontsize=10)
    
    # Legend (ülemises osas, väljaspool graafikut)
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels, 
              loc='upper center', 
              bbox_to_anchor=(0.5, -0.05), 
              ncol=min(5, len(handles)), 
              frameon=False,
              fontsize=10)
    
    # Grid
    ax.grid(axis='x', alpha=0.3, linestyle='--', linewidth=0.5)
    ax.set_axisbelow(True)
    
    # ===== LISA PROTSENDID TULPADELE =====
    if naita_protsente:
        for i in range(len(kategooriad)):
            # Vasak pool (negatiivne) kokku
            vasak_summa = 0
            if negatiivne_veerud:
                vasak_summa = sum(df_pct.iloc[i][veerg] for veerg in negatiivne_veerud)
            
            # Parem pool (positiivne) kokku
            parem_summa = 0
            if positiivne_veerud:
                parem_summa = sum(df_pct.iloc[i][veerg] for veerg in positiivne_veerud)
            
            # Neutraalne
            neutraalne_summa = 0
            if neutraalne_veerg:
                neutraalne_summa = df_pct.iloc[i][neutraalne_veerg]
            
            # Näita vasakpoolset summat
            if vasak_summa > 3:  # Näita ainult kui piisavalt suur
                ax.text(-vasak_summa/2 - neutraalne_summa/4, i, 
                       f'{vasak_summa:.0f}%',
                       ha='center', va='center', 
                       fontsize=9, fontweight='bold', 
                       color='#333')
            
            # Näita neutraalset
            if neutraalne_summa > 3:
                ax.text(0, i, f'{neutraalne_summa:.0f}%',
                       ha='center', va='center',
                       fontsize=9, fontweight='bold',
                       color='#333')
            
            # Näita parempoolset summat
            if parem_summa > 3:
                ax.text(parem_summa/2 + neutraalne_summa/4, i, 
                       f'{parem_summa:.0f}%',
                       ha='center', va='center', 
                       fontsize=9, fontweight='bold', 
                       color='white')
    
    plt.tight_layout()
    
    return fig, ax