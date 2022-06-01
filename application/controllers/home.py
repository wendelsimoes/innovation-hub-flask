# Página inicial
@app.route("/")
def index():
    formDeRegistro = FormDeRegistro()
    return render_template("index.html", 
    formDeRegistro=formDeRegistro, 
    formDeLogin=FormDeLogin(), 
    abrirModalDeRegistro=False, 
    abrirModalDeLogin=False
    )