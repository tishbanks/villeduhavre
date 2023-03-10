import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import matplotlib.pyplot as plt
import math

APP_TITLE = "Bilan 'Mon Rendez-Vous Numérique'"

#LISTES:

NOMBRE_PERSONNE_GENRE = []
NOMBRE_PERSONNE_TYPE = []
NOMBRE_PERSONNE_QUARTIER = []
NOMBRE_PERSONNE_GENRE_QUARTIER = [[]]
NOMBRE_PERSONNE_TYPE_QUARTIER = [[]]
NOMBRE_PERSONNE_GENRE_TYPE = [[]]
NOMBRE_PERSONNE_TYPE_GENRE = [[]]
NOMBRE_PERSONNE_QUARTIER_TYPE = [[]]
NOMBRE_PERSONNE_QUARTIER_GENRE = [[]]
NOMBRE_PERSONNE_QUARTIER_GENRE_TYPE = [[[]]]
NOMBRE_PERSONNE_GENRE_TYPE_QUARTIER = [[[]]]
NOMBRE_PERSONNE_TYPE_QUARTIER_GENRE = [[[]]]
NOMBRE_PERSONNE = 0

QUARTIER_LIST = ["Aplemont", "Bléville", "Bois de Bléville", "Caucriauville", "Danton", "Dollemard", "Graville",
                 "Hêtraie", "L'Eure", "Les Acacias", "Les Gobelins", "Les Ormeaux", "Mare au Clerc", "Mare Rouge",
                 "Mont-Gaillard", "Rouelles", "Saint-François", "Saint-Vincent", "Sanvic", "Soquence", "Tourneville"]

GENRE_LIST = ["Mr", "Mme"]

TYPE_LIST = ["A domicile", "En résidence autonomie"]


def display_pivot(df):
    table = pd.pivot_table(df, values="Nombre", index="Quartier",
                           columns=["Type", "Genre"], aggfunc="count", dropna=True, fill_value=0, margins=True)
    st.table(table)

def comparaison(df, q1, q2):

    if q1 != "Tous":
        df1 = df[df.Quartier == q1]
        index1 = QUARTIER_LIST.index(q1)
        x_1 = NOMBRE_PERSONNE_QUARTIER_GENRE[index1]
        y_1 = NOMBRE_PERSONNE_QUARTIER_TYPE[index1]
    else:
        df1 = df
        x_1 = NOMBRE_PERSONNE_GENRE
        y_1 = NOMBRE_PERSONNE_TYPE
    if q2 != "Tous":
        df2 = df[df.Quartier == q2]
        index2 = QUARTIER_LIST.index(q2)
        x_2 = NOMBRE_PERSONNE_QUARTIER_GENRE[index2]
        y_2 = NOMBRE_PERSONNE_QUARTIER_TYPE[index2]
    else:
        df2 = df
        x_2 = NOMBRE_PERSONNE_GENRE
        y_2 = NOMBRE_PERSONNE_TYPE
    compte1 = df1["Genre"].count()
    rdv1 = round(df1["Nombre"].sum(), 0)
    compte2 = df2["Genre"].count()
    rdv2 = round(df2["Nombre"].sum(), 0)
    age1 = round(df1["Age"].mean(), 0)
    age2 = round(df2["Age"].mean(), 0)
    a, b = st.columns(2)
    with a:
        st.write(q1)
        st.metric("# de personnes", compte1)
        st.metric("Age moyen", age1)
        st.metric("# rdvs", rdv1)
        st.metric("# rdvs/personne", round(rdv1 / compte1, 1))
    with b:
        st.write(q2)
        st.metric("# de personnes", compte2)
        st.metric("Age moyen", age2)
        st.metric("# rdvs", rdv2)
        st.metric("# rdvs/personne", round(rdv2 / compte2, 1))

    fig1, ax1 = plt.subplots()
    fig1.patch.set_facecolor('black')
    fig1.patch.set_alpha(0.1)
    fig2, ax2 = plt.subplots()
    fig2.patch.set_facecolor('black')
    fig2.patch.set_alpha(0.1)
    colors = ("#1cc0fc", "#eb4034")
    ax1.pie(x_1, labels=GENRE_LIST, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=90, textprops={'color': "w"})
    ax2.pie(x_2, labels=GENRE_LIST, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=90, textprops={'color': "w"})
    with a:
        st.pyplot(fig1)
    with b:
        st.pyplot(fig2)
    fig3, ax3 = plt.subplots()
    fig3.patch.set_facecolor('black')
    fig3.patch.set_alpha(0.1)
    fig4, ax4 = plt.subplots()
    fig4.patch.set_facecolor('black')
    fig4.patch.set_alpha(0.1)
    colors = ("#1cc0fc", "#eb4034")
    ax3.pie(y_1, labels={"Dom", "Rda"}, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=90, textprops={'color': "w"})
    ax4.pie(y_2, labels={"Dom", "Rda"}, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=90, textprops={'color': "w"})
    with a:
        st.pyplot(fig3)
    with b:
        st.pyplot(fig4)

def display_graphique(**filter):
    global NOMBRE_PERSONNE_GENRE
    global NOMBRE_PERSONNE_TYPE
    global NOMBRE_PERSONNE_QUARTIER

    explode1 = [0] * 2
    explode2 = [0] * 2
    explode3 = [0] * 21

    if "Genre" in filter.keys():
        if filter["Genre"] != "Tous":
            index = GENRE_LIST.index(filter["Genre"])
            explode1[index] = 0.2
    if "Type" in filter.keys():
        if filter["Type"] != "Tous":
            index = TYPE_LIST.index(filter["Type"])
            explode2[index] = 0.2
    if "Quartier" in filter.keys():
        if filter["Quartier"] != "Tous":
            index = QUARTIER_LIST.index(filter["Quartier"])
            explode3[index] = 0.2

    colors = ("#1cc0fc", "#eb4034")
    if not (filter["Genre"] != "Tous" and filter["Type"] != "Tous" and filter["Quartier"] != "Tous"):
        fig1, ax1 = plt.subplots()
        fig1.patch.set_facecolor('black')
        fig1.patch.set_alpha(0.1)
        if filter["Type"] == "Tous" and filter["Quartier"] == "Tous":
            write = "Part Homme/Femme globale"
            ax1.pie(NOMBRE_PERSONNE_GENRE, labels=GENRE_LIST, explode=explode1, colors=colors, autopct='%1.1f%%',
                    shadow=True, startangle=90, textprops={'color': "w"})
        if filter["Type"] == "Tous" and filter["Quartier"] != "Tous":
            index = QUARTIER_LIST.index(filter["Quartier"])
            write = "Part Homme/Femme dans le quartier de {}".format(filter["Quartier"])
            ax1.pie(NOMBRE_PERSONNE_QUARTIER_GENRE[index], labels=GENRE_LIST, explode=explode1, colors=colors,
                    autopct='%1.1f%%', shadow=True, startangle=90, textprops={'color': "w"})
        if filter["Type"] != "Tous" and filter["Quartier"] == "Tous":
            index = TYPE_LIST.index(filter["Type"])
            write = "Part Homme/Femme ayant bénéficié d'un rdv numérique {}".format(filter["Type"])
            ax1.pie(NOMBRE_PERSONNE_TYPE_GENRE[index], labels=GENRE_LIST, explode=explode1, colors=colors,
                    autopct='%1.1f%%', shadow=True, startangle=90, textprops={'color': "w"})
        if filter["Type"] != "Tous" and filter["Quartier"] != "Tous":
            index1 = TYPE_LIST.index(filter["Type"])
            index2 = QUARTIER_LIST.index(filter["Quartier"])
            write = "Part Homme/Femme ayant bénéficié d'un rdv numérique {} dans le quartier de {}".format(filter["Type"], filter["Quartier"])
            ax1.pie(NOMBRE_PERSONNE_TYPE_QUARTIER_GENRE[index1][index2], labels=GENRE_LIST, explode=explode1, colors=colors,
                    autopct='%1.1f%%', shadow=True, startangle=90, textprops={'color': "w"})
        fig2, ax2 = plt.subplots()
        fig2.patch.set_facecolor('black')
        fig2.patch.set_alpha(0.1)
        if filter["Genre"] == "Tous" and filter["Quartier"] == "Tous":
            write2 = "Part Domicile/RDA globale"
            ax2.pie(NOMBRE_PERSONNE_TYPE, labels=("Dom", "Rda"), explode=explode2, colors=colors,
                    autopct='%1.1f%%', shadow=True, startangle=90, textprops={'color': "w"})
        if filter["Genre"] != "Tous" and filter["Quartier"] == "Tous":
            write2 = "Part Domicile/RDA chez les {}".format(filter["Genre"])
            index = GENRE_LIST.index(filter["Genre"])
            ax2.pie(NOMBRE_PERSONNE_GENRE_TYPE[index], labels=("Dom", "Rda"), explode=explode2, colors=colors,
                    autopct='%1.1f%%', shadow=True, startangle=90, textprops={'color': "w"})
        if filter["Genre"] == "Tous" and filter["Quartier"] != "Tous":
            write2 = "Part Domicile/RDA dans le quartier de {}".format(filter["Quartier"])
            index = QUARTIER_LIST.index(filter["Quartier"])
            ax2.pie(NOMBRE_PERSONNE_QUARTIER_TYPE[index], labels=("Dom", "Rda"), explode=explode2, colors=colors,
                    autopct='%1.1f%%', shadow=True, startangle=90, textprops={'color': "w"})
        if filter["Genre"] != "Tous" and filter["Quartier"] != "Tous":
            index1 = GENRE_LIST.index(filter["Genre"])
            index2 = QUARTIER_LIST.index(filter["Quartier"])
            write2 = "Part Domicile/RDA ches les {} dans les quartier de {}.".format(filter["Genre"], filter["Quartier"])
            ax2.pie(NOMBRE_PERSONNE_QUARTIER_GENRE_TYPE[index2][index1], labels=("Dom", "Rda"), explode=explode2, colors=colors,
                    autopct='%1.1f%%', shadow=True, startangle=90, textprops={'color': "w"})
        fig3, ax3 = plt.subplots()
        fig3.patch.set_facecolor('black')
        fig3.patch.set_alpha(0.1)
        if filter["Genre"] == "Tous" and filter["Type"] == "Tous":
            write3 = "Répartition globale par quartier"
            ax3.pie(NOMBRE_PERSONNE_QUARTIER, labels=QUARTIER_LIST, explode=explode3,
                    startangle=90, autopct='%1.1f%%', textprops={'color': "w", 'fontsize': 1})
        if filter["Genre"] != "Tous" and filter["Type"] == "Tous":
            write3 = "Répartition par quartier chez les {}".format(filter["Genre"])
            index = GENRE_LIST.index(filter["Genre"])
            ax3.pie(NOMBRE_PERSONNE_GENRE_QUARTIER[index], labels=QUARTIER_LIST, explode=explode3,
                    startangle=90, autopct='%1.1f%%', textprops={'color': "w", 'fontsize': 1})
        if filter["Genre"] == "Tous" and filter["Type"] != "Tous":
            write3 = "Répartition part quartier des rdv {}".format(filter["Type"])
            index = TYPE_LIST.index(filter["Type"])
            ax3.pie(NOMBRE_PERSONNE_TYPE_QUARTIER[index], labels=QUARTIER_LIST, explode=explode3,
                    startangle=90, autopct='%1.1f%%', textprops={'color': "w", 'fontsize': 1})
        if filter["Genre"] != "Tous" and filter["Type"] != "Tous":
            write3 = "Répartition par quartier chez les {} ayant bénéficié d'un rdv numérique {}.".format(filter["Genre"],filter["Quartier"])
            index1 = GENRE_LIST.index(filter["Genre"])
            index2 = TYPE_LIST.index(filter["Type"])
            ax3.pie(NOMBRE_PERSONNE_GENRE_TYPE_QUARTIER[index1][index2],labels=QUARTIER_LIST, explode=explode3,
                    startangle=90, autopct='%1.1f%%', textprops={'color': "w", 'fontsize': 1})
        a, b, c = st.columns(3)
        with a:
            st.pyplot(fig2)
            st.write(write2)
        with b:
            st.pyplot(fig3)
            st.write(write3)
        with c:
            st.pyplot(fig1)
            st.write(write)

def display_metric(data, column, **filter):
    data2 = data
    for key, value in filter.items():
        if value != "Tous":
            data = data[data[key] == value]
    count = data[column].count()
    count2 = data2[column].count()
    age_moyen = round(data["Age"].mean(), 1)
    if math.isnan(age_moyen): age_moyen = 0
    nombre_rdv = round(data["Nombre"].sum())
    nombre_rdv2 = round(data2["Nombre"].sum())
    moy_rdv = round(data["Nombre"].mean(), 1)
    if math.isnan(moy_rdv): moy_rdv = 0
    a, b, c, d = st.columns(4)
    with a:
        st.metric(label="# de personnes", value=count)
    with b:
        st.metric(label='# de rdv total', value=nombre_rdv)
    with c:
        st.metric(label='# de rdv moyen', value=moy_rdv)
    with d:
        st.metric(label='Age moyen', value=age_moyen)
    if count != count2:
        part_personnes = round(count / count2 * 100, 1)
        part_rdvs = round(nombre_rdv / nombre_rdv2 * 100, 1)
        with a:
            st.metric(label="%", value=part_personnes)
        with b:
            st.metric(label="%", value=part_rdvs)

def display_map(data, genre="Tous", type="Tous", quartier="Tous"):

    lat = 49.51
    lon = 0.125
    zoom = 13

    string_genre = "des bénéficiaires"
    string_type = ""
    string_quartier = "sur la ville du Havre"

    if genre != "Tous":
        data = data[data.Genre == genre]
        if genre == "Mr": string_genre = "des hommes"
        if genre == "Mme": string_genre = "des femmes"
    if type != "Tous":
        data = data[data.Type == type]
        if type == "A domicile": string_type = "à domicile"
        if type == "En résidence autonomie": string_type = "en résidence autonomie"
    if quartier != "Tous":
        data = data[data.Quartier == quartier]
        lat = data["Latitude"].mean()
        lon = data["Longitude"].mean()
        zoom = 13
        string_quartier = "sur le quartier de {}".format(quartier)

    string = "Plan " + string_genre + " ayant reçu un accompagnement numérique " + string_type + string_quartier

    if not(math.isnan(lat) and math.isnan(lon)):
        map = folium.Map(location=[lat, lon], tiles="Stamen Toner", zoom_start=zoom,
                         scrollWheelZoom=False, dragging=False)
    else:
        map = folium.Map(location=[49.503, 0.12], tiles="Stamen Toner", zoom_start=13,
                         scrollWheelZoom=False, dragging=False)
        string = "Pas de bénéficaires avec les critères selectionnés"

    for i, row in data.iterrows():

        iframe = folium.IFrame(str(row["Nom"]))

        match row["Genre"]:
            case "Mr":
                color = "blue"
            case "Mme":
                color= "red"
        match row["Type"]:
            case "A domicile":
                icon = 'home'
            case "En résidence autonomie":
                icon = 'hospital-o'

        fk= folium.Marker(location=[row["Latitude"], row["Longitude"]],
                      icon=folium.Icon(color=color, icon=icon, prefix='fa')).add_to(map)

    st.write(string)
    st.map = st_folium(map, width=700, height=450)

def main():
    st.set_page_config(APP_TITLE)
    st.title(APP_TITLE)

    # LOAD DATA
    df = pd.read_excel('https://github.com/tishbanks/villeduhavre/blob/64017b3e9aba8eebe4a696acbc5dc6c4860999f2/MRN3.xlsx')
    data = pd.DataFrame().assign(
        Genre=df['Civilité'],
        Nom=df['Nom, Prénom bénéficiaire'],
        Age=df['age'],
        Type=df['Mon rdv numérique'],
        Adresse=df['adresse'],
        Nombre=df['Nombre de rdv faits'],
        Latitude=df['latitude'],
        Longitude=df['longitude'],
        Quartier=df['District'],
        Demande_decouverte=df['Découverte'],
        Demande_apprendre=df['Apprendre'],
        Demande_effectuer=df['Effectuer'],
        Demande_telecharger=df['Télécharger'],
        Demande_organiser=df['Organiser'],
        Demande_achats=df['Achats'],
        Demande_installer=df['Installer']
    )
    #VARIABLE DU DATASET

    global NOMBRE_PERSONNE_GENRE, quartier
    global NOMBRE_PERSONNE_TYPE
    global NOMBRE_PERSONNE_QUARTIER
    global NOMBRE_PERSONNE_GENRE_QUARTIER
    global NOMBRE_PERSONNE_TYPE_QUARTIER
    global NOMBRE_PERSONNE_GENRE_TYPE
    global NOMBRE_PERSONNE_TYPE_GENRE
    global NOMBRE_PERSONNE_QUARTIER_TYPE
    global NOMBRE_PERSONNE_QUARTIER_GENRE
    global NOMBRE_PERSONNE

    global GENRE_LIST
    global TYPE_LIST
    global QUARTIER_LIST

    i=0
    j=0

    for genre in GENRE_LIST:
        NOMBRE_PERSONNE_GENRE.append(data[data.Genre == genre]["Genre"].count())
        NOMBRE_PERSONNE_GENRE_TYPE.append([])
        NOMBRE_PERSONNE_GENRE_QUARTIER.append([])
        NOMBRE_PERSONNE_GENRE_TYPE_QUARTIER.append([[]])
        for type in TYPE_LIST:
            NOMBRE_PERSONNE_GENRE_TYPE_QUARTIER[i].append([])
            NOMBRE_PERSONNE_GENRE_TYPE[i].append(data[data.Type == type][data.Genre == genre]["Genre"].count())
            for quartier in QUARTIER_LIST:
                NOMBRE_PERSONNE_GENRE_TYPE_QUARTIER[i][j].append(data[data.Quartier == quartier][data.Type == type][data.Genre == genre]["Genre"].count())
            j+=1
        for quartier in QUARTIER_LIST:
            NOMBRE_PERSONNE_GENRE_QUARTIER[i].append(data[data.Quartier == quartier][data.Genre == genre]["Genre"].count())
        j=0
        i+=1
    i=0
    j=0
    for type in TYPE_LIST:
        NOMBRE_PERSONNE_TYPE.append(data[data.Type == type]["Type"].count())
        NOMBRE_PERSONNE_TYPE_GENRE.append([])
        NOMBRE_PERSONNE_TYPE_QUARTIER.append([])
        NOMBRE_PERSONNE_TYPE_QUARTIER_GENRE.append([[]])
        for genre in GENRE_LIST:
            NOMBRE_PERSONNE_TYPE_GENRE[i].append(data[data.Genre == genre][data.Type == type]["Type"].count())
        for quartier in QUARTIER_LIST:
            NOMBRE_PERSONNE_TYPE_QUARTIER_GENRE[i].append([])
            NOMBRE_PERSONNE_TYPE_QUARTIER[i].append(data[data.Quartier == quartier][data.Type == type]["Type"].count())
            for genre in GENRE_LIST:
                NOMBRE_PERSONNE_TYPE_QUARTIER_GENRE[i][j].append(data[data.Quartier == quartier][data.Type == type][data.Genre == genre]["Genre"].count())
            j+=1
        j=0
        i+=1
    i=0
    j=0
    for quartier in QUARTIER_LIST:
        NOMBRE_PERSONNE_QUARTIER.append(data[data.Quartier == quartier]["Quartier"].count())
        NOMBRE_PERSONNE_QUARTIER_GENRE.append([])
        NOMBRE_PERSONNE_QUARTIER_TYPE.append([])
        NOMBRE_PERSONNE_QUARTIER_GENRE_TYPE.append([[]])
        for genre in GENRE_LIST:
            NOMBRE_PERSONNE_QUARTIER_GENRE[i].append(data[data.Genre == genre][data.Quartier == quartier]["Quartier"].count())
        for type in TYPE_LIST:
            NOMBRE_PERSONNE_QUARTIER_GENRE_TYPE[i].append([])
            NOMBRE_PERSONNE_QUARTIER_TYPE[i].append(data[data.Type == type][data.Quartier == quartier]["Quartier"].count())
            for genre in GENRE_LIST:
                NOMBRE_PERSONNE_QUARTIER_GENRE_TYPE[i][j].append(data[data.Quartier == quartier][data.Type == type][data.Genre == genre]["Genre"].count())
            j+=1
        j=0
        i+=1
    i=0

    genre_list = GENRE_LIST.copy()
    genre_list.insert(0, "Tous")
    quartier_list = QUARTIER_LIST.copy()
    quartier_list.insert(0, "Tous")
    type_list = TYPE_LIST.copy()
    type_list.insert(0, "Tous")

    genre = st.sidebar.selectbox("Civilité:", genre_list)
    type = st.sidebar.selectbox("Type:", type_list)
    quartier = st.sidebar.selectbox("Quartier:", quartier_list)
    comparaison_quartier = st.sidebar.checkbox("Comparaison Quartier")

    display_map(data, genre, type, quartier)

    if not comparaison_quartier:
        st.write("Chiffres globaux:")
        display_metric(data, "Genre")

        if (genre, type, quartier) != ("Tous", "Tous", "Tous"):
            st.write("Chiffres filtrés:")
            display_metric(data, "Genre", Genre=genre, Type=type, Quartier=quartier)

        display_graphique(Genre=genre, Type=type, Quartier=quartier)
        pivot = st.sidebar.checkbox("Tableau comparatif")

    if comparaison_quartier:
        quartier1 = st.sidebar.selectbox("Quartier 1:", quartier_list)
        quartier2 = st.sidebar.selectbox("Quartier 2:", quartier_list)
        compare = st.sidebar.button("Compare {} et {}".format(quartier1, quartier2))
        if compare:
            comparaison(data, quartier1, quartier2)

    if pivot:
        display_pivot(data)
main()
