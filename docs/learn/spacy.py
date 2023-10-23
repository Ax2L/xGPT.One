import os
import pipreqs

# streamlit_app.py
import spacy_streamlit

models = ["en_core_web_sm", "en_core_web_md"]
default_text = "Sundar Pichai is the CEO of Google."
spacy_streamlit.visualize(models, default_text)
#? ! ||--------------------------------------------------------------------------------||
#? ! ||                        autonom requirements.txt updater                        ||
#? ! ||--------------------------------------------------------------------------------||

try:
    # Create requirements.txt via pipreqs
    current_directory = os.getcwd()
    command = pipreqs +str(current_directory+"/helper/ --force")
    stream = os.popen(command)
    output = stream.read()
    output
except Exception as e:
    print(e)



