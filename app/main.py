from dash_app import app
from layout import layout
import callbacks

app.layout = layout

if __name__ == "__main__":
    app.run(debug=False)
