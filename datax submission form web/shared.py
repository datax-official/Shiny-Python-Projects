from shiny import ui

INPUTS = {
    "name": ui.input_text("name", "Name"),
    "email": ui.input_text("email", "Email"),
    "whatsapp": ui.input_text("whatsapp", "WhatsApp Number"),
    "city": ui.input_text("city", "City"),
    "country": ui.input_select(
        "country",
        "Country",
        choices=["", "Pakistan","India","Bangladesh","Sri Lanka", "USA", "Canada", "UK", "Australia", "Other"],
    ),
    "experience": ui.input_text_area("experience", "Experience"),
    "internship": ui.input_radio_buttons(
        "internship",
        "For which internship you want to apply?",
        choices=[
            "Data Analyst",
            "Web Developer",
            "Machine Learning",
            "Android App Development"
        ],
        inline=False,
    ),
    "skills": ui.input_text_area("skills", "Top Skills (3 to 5)"),
    "cv": ui.input_file("cv", "Attach CV", multiple=False),
}
