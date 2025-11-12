import gradio as gr

def greet(name):
    """Function to greet the user by name."""
    return f"Hallo, {name}!! 🙂"

gr.Interface(
    fn=greet,
    inputs=gr.Textbox(label="Name eingeben"),
    outputs=gr.Textbox(label="Begrüßung"),
    title="Hello World mit Gradio",
    description="Geben Sie Ihren Namen ein, um eine Begrüßung zu erhalten."
).launch()