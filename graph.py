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

# Fonction pour créer le graphe interactif avec possibilité de zoom et pan
def plot_interactive_graph(data, x_values, y_values):
    fig, ax = plt.subplots()
    ax.plot(x_values, y_values)
    ax.set(xlabel="Index", ylabel="Random Values", title="Graphique")
    ax.grid(True)

    # Activer l'interactivité mplcursors (afficher les valeurs au survol)
    mplcursors.cursor(hover=True)

    # Fonction pour gérer le zoom sur le graphe en utilisant la molette de la souris
    def on_scroll(event):
        x_min, x_max = ax.get_xlim()
        y_min, y_max = ax.get_ylim()

        x_range = x_max - x_min
        y_range = y_max - y_min

        zoom_factor = 0.1  # Ajustez ce facteur pour contrôler le niveau de zoom

        if event.button == "up":
            ax.set_xlim(x_min + x_range * zoom_factor, x_max - x_range * zoom_factor)
            ax.set_ylim(y_min + y_range * zoom_factor, y_max - y_range * zoom_factor)
        elif event.button == "down":
            ax.set_xlim(x_min - x_range * zoom_factor, x_max + x_range * zoom_factor)
            ax.set_ylim(y_min - y_range * zoom_factor, y_max + y_range * zoom_factor)

        fig.canvas.draw()

    fig.canvas.mpl_connect("scroll_event", on_scroll)
    st.pyplot(fig)

# Fonction principale de l'application Streamlit
def main():
    st.title("Graphe interactif avec Streamlit")

    # Génération des données aléatoires
    num_points = 50
    data = generate_random_data(num_points)

    # Affichage des données
    st.subheader("Tableau de valeurs")
    st.write(data)

    # Création des listes de valeurs pour les axes x et y du graphe
    x_values = data["index"]
    y_values = data["random_values"]

    # Tracé du graphe initial interactif
    st.subheader("Graphe")
    plot_interactive_graph(data, x_values, y_values)

if __name__ == "__main__":
    main()


