from pokebase import move, ability
from tkinter import *
from tkinter import messagebox, ttk
import requests
import os
from PIL import Image, ImageTk
from tkinter.simpledialog import askstring

# basic Pokemon Move Finder Program
# Created by: Travis Huynh
# Using Python GUI for interactive user experience! 

def show_pokemon_list(learned_by_pokemon):
    list_window = Toplevel(root)
    list_window.title("Pokémon that can acquire this move")
    
    list_text = Text(list_window, wrap=WORD, width=40, height=10, font=("Arial", 12))
    list_text.pack(padx=10, pady=10)

    list_text.insert(END, "\n".join(learned_by_pokemon))

def fetch_all_pokemon_move(name):
    try:
        poke = move(name)
        learned_by_pokemon = [pokemon.name for pokemon in poke.learned_by_pokemon]
        
        user_response = messagebox.askyesno("Show Pokemon?", f"Do you want to see the list of {len(learned_by_pokemon)} Pokémon that can acquire this move?")
        
        if user_response:
            show_pokemon_list(learned_by_pokemon)
            return "The list of Pokémon has been displayed in a separate window.\n"
        else:
            return "You chose not to see the list of Pokémon.\n"
    except Exception as e:
        return f"Error fetching information: {e}"


def fetch_pokemon_id(name):
    poke = move(name)
    result = "Summary:\n"
    result += "-------------------------------------------------------------------------------------------\n"
    result += f"The {poke.type} type move {name} is a {poke.damage_class} type move that has an id of: {poke.id}\n"
    result += f"This move was first introduced in {poke.generation}\n\n"
    return result

def fetch_pokemon_power(name):
    poke = move(name)
    result = "Combat:\n"
    result += "-------------------------------------------------------------------------------------------\n"
    if poke.power < 100: 
        result += f"{name} has {poke.power} power and has {poke.pp} pp\n"
        result += "The power on this move is less than 100, wow so shit haha!\n"
        result += f"Additionally, this move has an accuracy of {poke.accuracy}\n\n"
        compare_eq = (poke.power / 100) * 100
        result += f"{name} is {compare_eq}% of Earthquake(ID: 84) in comparison to its power (because earthquake is op)\n"
    elif poke.power == 100: 
        result += f"{name} has {poke.power} power and has {poke.pp} pp\n"
        result += "WOW! I have much respect for this move! It has power that has the same power as earthquake OMG!!!\n"
        result += f"Additionally, this move has an accuracy of {poke.accuracy}\n\n"
        compare_eq = (poke.power / 100) * 100
        result += f"{name} is {compare_eq}% of Earthquake(ID: 84) in comparison to its power (because earthquake is op)\n"
    else: 
        result += f"{name} has {poke.power} power and has {poke.pp} pp\n"
        result += "Bruh, ain't no way its better than stab eq, how does it have more power :(\n"
        result += f"Additionally, this move has an accuracy of {poke.accuracy}\n\n"
        compare_eq = (poke.power / 100) * 100
        result += f"{name} is {compare_eq}% of Earthquake(ID: 84) in comparison to its power (because earthquake is op)\n"
    result += "-------------------------------------------------------------------------------------------\n\n"
    return result

def fetch_ability_info(name):
    try:
        ability_data = ability(name)
        result = f"Ability Name: {ability_data.name}\n"
        result += f"Effect: {ability_data.effect}\n"
        result += f"Short Effect: {ability_data.short_effect}\n"
        return result
    except Exception as e:
        return f"Error fetching information: {e}"
    
def fetch_type_effectiveness(move_name, target_type):
    try:
        move_data = move(move_name)
        effectiveness = 1.0
        for target in move_data.type.damage_relations.double_damage_to:
            if target.name == target_type:
                effectiveness *= 2.0
        for target in move_data.type.damage_relations.half_damage_to:
            if target.name == target_type:
                effectiveness *= 0.5
        for target in move_data.type.damage_relations.no_damage_to:
            if target.name == target_type:
                effectiveness = 0.0
        return f"The effectiveness of {move_name} against {target_type} type is {effectiveness}.\n"
    except Exception as e:
        return f"Error fetching information: {e}"

def fetch_move_info_gui(name):
    output_text.delete(1.0, END) 

    try:
        poke = move(name)
    except Exception as e:
        output_text.insert(END, f"Error: {e}")
        return

    output_text.insert(END, "Fetching " + name + ".......\n\n")
    output_text.insert(END, fetch_all_pokemon_move(name))
    output_text.insert(END, fetch_pokemon_id(name))
    output_text.insert(END, fetch_pokemon_power(name))

def clear_output():
    output_text.delete(1.0, END)

def main_gui():
    global root
    root = Tk()
    root.title("Pokemon Move Finder")
    root.configure(bg="#FC9C85")  

    label = Label(root, text="Welcome to Pokemon Move Finder!\n Created By: Travis Huynh", font=("Calibri", 16), bg="#FCBBAB")
    label.pack(pady=10)

    entry = Entry(root, font=("Calibri", 12), width=30)
    entry.pack(pady=10)

    def search_move():
        name = entry.get()
        if name:
            fetch_move_info_gui(name)

    button = Button(root, text="Search Move", command=search_move, font=("Calibri", 12), bg="#ffffff")
    button.pack(pady=10)

    clear_button = Button(root, text="Clear Output", command=clear_output, font=("Calibri", 12), bg="#ffffff")
    clear_button.pack(pady=10)
    
    ability_button = Button(root, text="Search Ability (does not work lol)", command=search_ability, font=("Calibri", 12), bg="#ffffff")
    ability_button.pack(pady=10)

    type_effectiveness_button = Button(root, text="Type Effectiveness Checker", command=lambda: type_effectiveness_check(entry), font=("Calibri", 12), bg="#ffffff")
    type_effectiveness_button.pack(pady=10)

    global output_text
    output_text = Text(root, wrap=WORD, width=50, height=20, font=("Calibri", 12))
    output_text.pack(pady=10)

    custom_font = ("Helvetica", 14)
    label.configure(font=custom_font)
    entry.configure(font=custom_font)
    button.configure(font=custom_font)
    clear_button.configure(font=custom_font)
    type_effectiveness_button.configure(font=custom_font)
    ability_button.configure(font=custom_font)
    output_text.configure(font=custom_font)

    root.mainloop()

def search_ability():
    ability_name = askstring("Search Ability", "Enter ability name:")
    if ability_name:
        output_text.delete(1.0, END)
        output_text.insert(END, fetch_ability_info(ability_name))

def type_effectiveness_check(entry):
    move_name = entry.get()
    target_type = askstring("Type Effectiveness Checker", "Enter target Pokémon type:")
    if move_name and target_type:
        output_text.delete(1.0, END)
        output_text.insert(END, fetch_type_effectiveness(move_name, target_type))

if __name__ == '__main__':
    main_gui()