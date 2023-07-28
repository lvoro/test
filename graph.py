import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import mplcursors

# Fonction pour créer un tableau de valeurs avec des données aléatoires
def generate_random_data(num_points):
    data = {
        "index": np.arange(1, num_points + 1),
        "random_values": np.random.randint(1, 101, num_points)
    }
    return pd.DataFrame(data)

# Fonction pour créer le graphe interactif avec la possibilité de zoomer
def plot_interactive_graph(data):
    fig, ax = plt.subplots()
    ax.plot(data["index"], data["random_values"])
    ax.set(xlabel="Index", ylabel="Random Values", title="Graphique")
    ax.grid(True)

    # Activer l'interactivité mplcursors (afficher les valeurs au survol)
    mplcursors.cursor(hover=True)

    # Fonction pour gérer le zoom sur le graphe en cliquant
    def onclick(event):
        x_min, x_max = ax.get_xlim()
        y_min, y_max = ax.get_ylim()
        x_range = x_max - x_min
        y_range = y_max - y_min

        zoom_factor = 0.1  # Ajustez ce facteur pour contrôler le niveau de zoom

        if event.button == 1:  # Clic gauche pour zoomer avant
            ax.set_xlim(event.xdata - x_range * zoom_factor, event.xdata + x_range * zoom_factor)
            ax.set_ylim(event.ydata - y_range * zoom_factor, event.ydata + y_range * zoom_factor)
        elif event.button == 3:  # Clic droit pour réinitialiser le zoom
            ax.set_xlim(x_min, x_max)
            ax.set_ylim(y_min, y_max)

        fig.canvas.draw()

    fig.canvas.mpl_connect("button_press_event", onclick)
    st.pyplot(fig)

# Fonction principale de l'application Streamlit
def main():
    st.title("Graphe interactif avec zoom sur clic")

    # Génération des données aléatoires
    num_points = 50
    data = generate_random_data(num_points)

    # Affichage des données
    st.subheader("Tableau de valeurs")
    st.write(data)

    # Tracé du graphe initial interactif
    st.subheader("Graphe")
    plot_interactive_graph(data)

if __name__ == "__main__":
    main()

