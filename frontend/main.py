import taipy


path = None
markdown = """
# Recipede.tech
          
Flyer: <|{path}|file_selector|label=Upload Flyer|extensions=.png,.jpg|on_action=load_file|>
        
"""

def load_file(state):
    mypath = state.path
    print(mypath)

taipy.Gui(page=markdown).run()