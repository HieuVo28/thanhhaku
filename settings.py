import tkinter, json

#make a settings editor window
#to configure the settings.cfg file

#create window
settings_window = tkinter.Tk()
settings_window.title("Settings")
settings_window.geometry("400x400")

#read settings.cfg
#create a list of settings
#create a list of settings labels
#create a list of settings entries
#create a button to save
#create a button to cancel
#use grid to place the widgets
with open("settings.cfg", "r") as settings_file:
    settings_list = json.load(settings_file)
    settings_file.close()

settings_labels = []
settings_entries = []
for setting in settings_list:
    settings_labels.append(tkinter.Label(settings_window, text=setting))
    settings_entries.append(tkinter.Entry(settings_window))
    settings_labels[-1].grid(row=len(settings_labels), column=0)
    settings_entries[-1].grid(row=len(settings_labels), column=1)
    settings_entries[-1].insert(0, settings_list[setting])

#buttons
save_button = tkinter.Button(settings_window, text="Save", command=lambda: save_settings(settings_entries))
save_button.grid(row=len(settings_labels)+1, column=0)
#cancel
cancel_button = tkinter.Button(settings_window, text="Cancel", command=lambda: settings_window.destroy())
cancel_button.grid(row=len(settings_labels)+1, column=1)

def save_settings(settings_entries):
    settings_list = {}
    for entry in settings_entries:
        settings_list[entry.get()] = entry.get()
    with open("settings.cfg", "w") as settings_file:
        json.dump(settings_list, settings_file)
        settings_file.close()
    settings_window.destroy()

settings_window.mainloop()
