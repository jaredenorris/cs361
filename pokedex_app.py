import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
from io import BytesIO

# Function to fetch a list of all Pokémon types from PokeAPI
def get_pokemon_types():
    url = "https://pokeapi.co/api/v2/type/"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return [type_info['name'] for type_info in data['results']]
    return []

# Function to get Pokémon of the selected type
def get_pokemon_by_type():
    selected_type = type_var.get()
    if selected_type:
        url = f"https://pokeapi.co/api/v2/type/{selected_type}/"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            pokemon_list = [pokemon['pokemon']['name'] for pokemon in data['pokemon']]
            # Clear the listbox before adding items
            pokemon_listbox.delete(0, tk.END)
            for name in pokemon_list:
                pokemon_listbox.insert(tk.END, name)
        else:
            pokemon_listbox.delete(0, tk.END)  # Clear the listbox
            pokemon_listbox.insert(tk.END, "No Pokémon found for type " + selected_type)
    else:
        pokemon_listbox.delete(0, tk.END)  # Clear the listbox
        pokemon_listbox.insert(tk.END, "Please select a Pokémon type.")

def get_pokemon_info():
    pokemon_name = name_entry.get()
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}/"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        name_label.config(text=f"Name: {data['name']}")
        height_label.config(text=f"Height: {data['height']}")
        weight_label.config(text=f"Weight: {data['weight']}")

        types = [type_info['type']['name'] for type_info in data['types']]
        types_label.config(text="Types: " + ", ".join(types))

        stats_text.set("Stats:\n")
        for stat in data['stats']:
            stats_text.set(stats_text.get() + f"{stat['stat']['name']}: {stat['base_stat']}\n")

        image_url = data['sprites']['front_default']
        if image_url:
            image_response = requests.get(image_url)
            img = Image.open(BytesIO(image_response.content))
            img.thumbnail((150, 150))
            img = ImageTk.PhotoImage(img)
            image_label.config(image=img)
            image_label.image = img
        else:
            image_label.config(image=None)
    else:
        name_label.config(text=f"Error: {response.status_code}")
        height_label.config(text="")
        weight_label.config(text="")
        types_label.config(text="")
        stats_text.set("")
        image_label.config(image=None)

def get_pokemon_generations():
    url = "https://pokeapi.co/api/v2/generation/"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return [generation['name'] for generation in data['results']]
    return []


def get_pokemon_by_generation():
    selected_generation = generation_var.get()
    if selected_generation:
        url = f"https://pokeapi.co/api/v2/generation/{selected_generation}/"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            game_pokemon = [pokemon['name'] for pokemon in data['pokemon_species']]

            if game_pokemon:
                # Clear the listbox before adding items
                generation_pokemon_listbox.delete(0, tk.END)
                for name in game_pokemon:
                    generation_pokemon_listbox.insert(tk.END, name)
            else:
                generation_pokemon_listbox.delete(0, tk.END)  # Clear the listbox
                generation_pokemon_listbox.insert(tk.END, "No Pokémon found for generation " + selected_generation)
        else:
            generation_pokemon_listbox.delete(0, tk.END)  # Clear the listbox
            generation_pokemon_listbox.insert(tk.END, "No Pokémon found for generation " + selected_generation)
    else:
        generation_pokemon_listbox.delete(0, tk.END)  # Clear the listbox
        generation_pokemon_listbox.insert(tk.END, "Please select a Pokémon generation.")













app = tk.Tk()
app.title("Pokedex")

frame = ttk.Frame(app, padding=10)
frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

name_label = ttk.Label(frame, text="Name:")
name_label.grid(column=0, row=0, sticky=tk.W)

name_entry = ttk.Entry(frame)
name_entry.grid(column=1, row=0)

search_button = ttk.Button(frame, text="Search", command=get_pokemon_info)
search_button.grid(column=2, row=0)

height_label = ttk.Label(frame, text="")
height_label.grid(column=0, row=1, sticky=tk.W)
weight_label = ttk.Label(frame, text="")
weight_label.grid(column=1, row=1, sticky=tk.W)

types_label = ttk.Label(frame, text="")
types_label.grid(column=1, row=3, columnspan=3, sticky=tk.W)

stats_text = tk.StringVar()
stats_label = ttk.Label(frame, textvariable=stats_text)
stats_label.grid(column=0, row=3, columnspan=3, sticky=tk.W)

image_label = ttk.Label(frame, image=None)
image_label.grid(column=0, row=5, columnspan=3, sticky=tk.W)

# "Search by Type" section
select_types_label = ttk.Label(frame, text="Select Pokémon Type:")
select_types_label.grid(column=0, row=6, sticky=tk.W)

type_var = tk.StringVar()
type_combobox = ttk.Combobox(frame, textvariable=type_var, values=get_pokemon_types())
type_combobox.grid(column=1, row=6)
type_combobox.set("")

type_button = ttk.Button(frame, text="Search", command=get_pokemon_by_type)
type_button.grid(column=2, row=6)

# Listbox to display Pokémon of the selected type
pokemon_listbox = tk.Listbox(frame)
pokemon_listbox.grid(row=7, column=0, columnspan=3, sticky=tk.W)

# "Search by Generation" section
generations_label = ttk.Label(frame, text="Select Pokémon Generation:")
generations_label.grid(column=0, row=8, sticky=tk.W)

generation_var = tk.StringVar()
generation_combobox = ttk.Combobox(frame, textvariable=generation_var, values=get_pokemon_generations())
generation_combobox.grid(column=1, row=8)
generation_combobox.set("")

generation_button = ttk.Button(frame, text="Search", command=get_pokemon_by_generation)
generation_button.grid(column=2, row=8)

# Listbox to display Pokémon of the selected generation
generation_pokemon_listbox = tk.Listbox(frame)
generation_pokemon_listbox.grid(row=9, column=0, columnspan=3, sticky=tk.W)



app.mainloop()
