# Dynamic server-generated HTML UI components

HTMX Components are server-generated HTML UI components, that use the [HTMX](https://htmx.org/) library to make them dynamic

Features:

* Works with and without JavaScript enabled
* No need to write any JavaScript

Available Widgets/Components:
* GridView
* Dynamic Form
* TreeView
* more soon!

See them in action: http://htmxcomponents.pythonanywhere.com/

Language Support:
* Python
* more soon!

Framework Support:
* Flask
* Django, FastAPI coming soon!

Example application: https://github.com/neilmcguigan/htmx-components-flask-example

Installation:
```
pip install htmx-components-flask

```

Example Usage (Flask):
```
from flask import Flask, render_template_string, request
from htmx_components_flask import htmx_components_flask
from flask_wtf import FlaskForm
import wtforms

app = Flask(__name__)
app.register_blueprint(htmx_components_flask)
app.config["SECRET_KEY"] = "s3cr3t"


class MyForm(FlaskForm):
    stringfield = wtforms.StringField("String", validators=[wtforms.validator.InputRequired()])
    submitbtn = wtforms.SubmitField("Submit")

# assumes you have a file templates/base.html that includes the htmx script:
@app.get("/", methods=["GET", "POST"])
def index():
    form = MyForm(request.form)
    form.validate_on_submit()

    return render_template_string("""
{% if "HX-Request" not in request.headers %}
    {% extends "base.html" %}
{% endif %}

{% block content %}

{% include "htmx_components_flask/form/horizontal.html" %}

{% endblock %}    
    
    """, form=form)
```



