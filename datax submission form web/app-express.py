from pathlib import Path
import pandas as pd
from shared import INPUTS
from shiny import reactive
from shiny.express import input, ui
from shiny_validate import InputValidator, check

app_dir = Path(__file__).parent
ui.include_css(app_dir / "styles.css")

ui.page_opts(title="Internship Application Form")

# Use HTML for the navigation bar
ui.HTML('''
<nav class="navbar navbar-expand-lg navbar-light bg-light">
    <a class="navbar-brand" href="#" style="font-weight: bold; font-size: 1.5rem;">Data X</a>
    <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ml-auto">
            <li class="nav-item">
                <a class="nav-link" href="https://www.youtube.com/@datax_official" target="_blank">YouTube</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="https://www.linkedin.com/company/datax-official/" target="_blank">LinkedIn</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="https://wa.me/923408226347" target="_blank">WhatsApp</a>
            </li>
        </ul>
    </div>
</nav>
''')

with ui.card():
    ui.card_header("Company Details")
    ui.p("Data X is a pioneering startup Data Science services and online education company dedicated to transforming businesses and individuals through cutting-edge data science and artificial intelligence solutions. We offer a comprehensive range of services, from advanced analytics and AI-driven insights to innovative educational programs designed to equip learners with the skills needed to thrive in the digital age. At Data X, we believe in the power of data to drive innovation and success, empowering our clients and students to reach their full potential.")
    ui.p("Empowering businesses and individuals with data-driven solutions.")
    ui.p("Join us for a rewarding internship experience!")

with ui.card():
    ui.card_header("Internship Details")
    ui.p("Apply for an internship in one of the following domains:")

with ui.card():
    ui.card_header("Personal Information")
    INPUTS["name"]
    INPUTS["email"]
    INPUTS["whatsapp"]
    INPUTS["city"]
    INPUTS["country"]
    INPUTS["experience"]

with ui.card():
    ui.card_header("Internship Application")
    INPUTS["internship"]

with ui.card():
    ui.card_header("Top Skills")
    INPUTS["skills"]

with ui.card():
    ui.card_header("Attach CV")
    INPUTS["cv"]

ui.div(
    ui.input_action_button("submit", "Submit", class_="btn btn-primary"),
    class_="d-flex justify-content-end",
)

input_validator = None

@reactive.Effect
def _():
    global input_validator
    input_validator = InputValidator()
    input_validator.add_rule("name", check.required())
    input_validator.add_rule("email", check.required())
    input_validator.add_rule("whatsapp", check.required())
    input_validator.add_rule("city", check.required())
    input_validator.add_rule("country", check.required())
    input_validator.add_rule("experience", check.required())
    input_validator.add_rule("internship", check.required())
    input_validator.add_rule("skills", check.required())

@reactive.Effect
@reactive.Event(input.submit)
def save_to_csv():
    input_validator.enable()
    if not input_validator.is_valid():
        return

    df = pd.DataFrame([{k: input[k]() for k in INPUTS.keys() if k != "cv"}])

    responses = app_dir / "responses.csv"
    if not responses.exists():
        df.to_csv(responses, mode="a", header=True)
    else:
        df.to_csv(responses, mode="a", header=False)

    ui.modal_show(ui.modal("Thank you for applying at Data X!"))
