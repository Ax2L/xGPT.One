from components.assistant.set_context import set_context

# Username
user_name = 'User'
gpt_name = 'ChatGPT'
# Avatar (in SVG format) from https://www.dicebear.com/playground?style=identicon
user_svg = """
<svg></g></svg>
"""
gpt_svg = """
<svg></path></svg>
"""
# Content background
user_background_color = ''
gpt_background_color = 'rgba(225, 230, 235, 0.5)'
# Initial model settings
initial_content_all = {
    "history": [],
    "paras": {
        "temperature": 1.0,
        "top_p": 1.0,
        "presence_penalty": 0.0,
        "frequency_penalty": 0.0,
    },
    "contexts": {
        'context_select': 'not set',
        'context_input': '',
        'context_level': 4
    }
}
# Context
set_context_all = {"not set": ""}
set_context_all.update(set_context)

# Custom CSS and JS
css_code = """
    <style>
    </style>
"""

js_code = """
<script>
</script>
"""
