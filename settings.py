import json
import os
from lib import defaults

def ensure():
    """
    create default settings.json if it does not exist
    """
    if not os.path.isfile(defaults.SETTINGS_FILE):
        create()
def create():
    """
    create the settings
    """
    # get the default settings
    settings = defaults.DEFAULT_SETTINGS
    # draw the page
    settings['settings'] = draw_page(settings['settings'])
    # update the settings
    update(settings)
def get():
    """
    get the settings
    """
    with open(defaults.SETTINGS_FILE, 'r') as f:
        return json.load(f)

def update(settings):
    """
    update the settings
    """
    # update the settings
    with open(defaults.SETTINGS_FILE, 'w') as f:
        json.dump(settings, f)
def draw_page(selectables):
    """
    draw the settings page
    """
    print("Settings:")
    for i, selectable in enumerate(selectables):
        print("{}. {}".format(i + 1, selectable))
    while True:
        # get user input
        try:
            input_ = int(input("Select: "))
            #validate input
            if input_ < 0 or input_ > len(selectables):
                print("Invalid input")
                continue
            # return the selected item
            return selectables[input_ - 1]
        except ValueError:
            print("Invalid input")
            continue
if __name__ == "__main__":
    ensure()
    print("Settings Editor")
    
    while True:
        selection = draw_page([
            "Configure",
            "Exit"
        ])

        if selection == "Exit":
            break
        elif selection == "Configure":
            print("Configure")
            config = get()
            def recursive_draw_page(config):
                print(config)
                draw = []
                #get top level keys
                keys = list(config.keys())
                #if key is a dict, add it to the selectables
                for key in keys:
                    if isinstance(config[key], dict):
                        draw.append("> "+key)
                for key in keys:
                    if not isinstance(config[key], dict):
                        draw.append(key)
                #draw the page
                draw_page(draw)
                #get user input
                while True:
                    selection0 = int(input("Select: "))
                    #validate input
                    if selection0 < 0 or selection0 > len(draw):
                        print("Invalid input")
                        continue
                    else:
                        break
                selected = draw[selection0]
                #if selected is a dict, draw the page
                if isinstance(config[selected], dict):
                    print(config)
                    recursive_draw_page(config[selected])
            recursive_draw_page(config)
