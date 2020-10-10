from flask import Flask, render_template, send_from_directory,redirect,url_for
import os
from PIL import Image
import glob
from pathlib import Path

app = Flask(__name__, static_url_path='')

image_list = []#-----WordCloud_Pic
for filename in glob.glob('output/Wordcloud/*.png'):
    im = Image.open(filename)
    image_list.append(im)
print("img === ",len(image_list))


txt_folder = Path('output/Top10').rglob('*.csv')
files = [x for x in txt_folder]
for name in files:
    f = open(name, 'r')
    content = f.readlines()
    print(content) #File_Top10
    f.close()


@app.route("/<name>")
def user(name):
    return f"hello {name}!"

@app.route("/home")
def home():
    return render_template("info.html",Top10 = content)

@app.route("/Pic")
def wc():
    return render_template("info.html",wcloud = image_list)


@app.route("/admin")
def admin():
    return redirect(url_for("user",name = "Admin!"))



@app.route('/static/<path:path>')
def send_js(path):

    return os.path.abspath(os.path.join( 'output', 'Wordcloud' ))
    # return send_from_directory('output\Wordcloud', path)


if __name__ =="__main__":
    app.run(debug=True)