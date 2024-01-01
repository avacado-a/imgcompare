from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
import Image
import time
import os
import myfreedb

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app = Flask('app')


def allowed_file(filename):
  return '.' in filename and \
         filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def compare(file1, file2):
  img1 = Image.open(file1).convert('RGB').resize(
      (1, 1))  #Change 1 to to 20 for Extensive similarity seach
  img2 = Image.open(file2).convert('RGB').resize(
      (1, 1))  #Change 1 to to 20 for Extensive similarity seach
  #1:Quick Image similarity search
  a = img1.getpixel((0, 0))
  b = img2.getpixel((0, 0))
  c = sum([a[i] - b[i] for i in range(3)])
  c /= 3
  #2:Extensive similarity seach
  #arr1 = list(img1.getdata())
  #arr2 = list(img2.getdata())
  #c=0
  #for i in range(len(arr1)):
  #  for x in range(3):
  #    c+=(arr1[i][x]-arr2[i][x])
  #c/=len(arr1)*3
  return abs(c)


def comp(file1, file2, dbx):
  print("1")
  if file1.replace("static/", "") not in list(dbx):
    img1 = Image.open(file1).convert('RGB').resize((1, 1))
    dbx[file1.replace("static/", "")] = img1.getpixel((0, 0))
  if file2.replace("static/", "") not in list(dbx):
    img2 = Image.open(file2).convert('RGB').resize((1, 1))
    dbx[file2.replace("static/", "")] = img2.getpixel((0, 0))
  a = dbx[file1.replace("static/", "")]
  b = dbx[file2.replace("static/", "")]
  print("4", a, b)
  c = sum([a[i] - b[i] for i in range(3)])
  c /= 3
  #2:Extensive similarity seach
  #arr1 = list(img1.getdata())
  #arr2 = list(img2.getdata())
  #c=0
  #for i in range(len(arr1)):
  #  for x in range(3):
  #    c+=(arr1[i][x]-arr2[i][x])
  #c/=len(arr1)*3
  return abs(c), dbx


def findsim(i):
  dbx = {}
  e = "hello"
  while e != "":
    e = ""
    try:
      print("a")
      dbx = eval(str(myfreedb.get(527)))
      print("b")
    except BaseException as x:
      print(x)
      print("c")
      time.sleep(2)
      e = x
  c = 257
  b = None
  #s = time.perf_counter_ns()
  for x in os.listdir("static"):
    print(x)
    if i != "static/" + x:
      a = comp(i, "static/" + x, dbx)
      a, dbx = a
      print(a)
      if a < c:
        b = "static/" + x
        c = a

  e = "hello"
  while e != "":
    e = ""
    try:
      print("b")
      myfreedb.post(527, str(dbx))
      print("a")
    except BaseException as x:
      print(x)
      time.sleep(2)
      e = x

  return b


  #print((time.perf_counter_ns()-s)/(1000000000*420*1),c,b)
@app.route('/img/<filename>')
def image(filename):
  filename = filename.replace("static", "")
  return f"<h2>Your image</h2><img style='height:45%;' src='/static/{len(os.listdir('static'))-1}.png' /><br><h2>The closest image found in the database</h2><img style='height:45%;' src='/static/{filename}' /><a href='https://imgcompare.sparik7633.repl.co/' ><button>Home</button></a>"


@app.route('/', methods=['GET', 'POST'])
def upload():
  if request.method == 'POST':
    if 'file' not in request.files:
      print('No file part')
      return "Error: No file found"
    file = request.files.getlist("file")[0]
    print(file)
    print(file, file.filename)
    print(allowed_file(file.filename))
    if file.filename == '':
      print(file, "Filename error")
      return 'Error: No selected file'
    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      c = 0
      for i in range(len(os.listdir("static"))):
        c += 1
      file.save("static/" + str(c) + ".png")
      a = findsim("static/" + str(c) + ".png")
      a = a.replace("static/", "")
      return redirect("https://imgcompare.sparik7633.repl.co/img/" + a)
  else:
    return '''
  <!doctype html>
  <html>
  <body>
  <title>Upload new File(s)</title>
  <h1>Upload new File</h1>
  <form method=post enctype=multipart/form-data>
    <input type=file name=file>
    <input type=submit value=Upload>
  </form>
  </body>
  </html>
  '''


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
  if request.method == 'POST':
    if 'file' not in request.files:
      return "No file part"
    files = request.files.getlist("file")
    print(files)
    for file in files:
      print(file, file.filename)
      print(allowed_file(file.filename))
      if file.filename == '':
        print(file, "Filename error")
        return "No selected file"
      if file.filename in os.listdir("static"):
        print("File already exists")
      elif file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
      c = 0
      for i in range(len(os.listdir("static"))):
        c += 1
      file.save("static/" + str(c) + ".png")
    return redirect("https://imgcompare.sparik7633.repl.co/upload/")
  return '''
  <!doctype html>
  <html>
  <head>
  <link href="/static/css/all.css" rel="stylesheet" type="text/css" />
  <link rel="shortcut icon" href="/static/assets/favicon.ico" type="image/x-icon">
  </head>
  <body>
  <title>Upload new File(s)</title>
  <h1>Upload new File</h1>
  <form method=post enctype=multipart/form-data>
    <input type=file name=file multiple>
    <input type=submit value=Upload>
  </form>
  </body>
  </html>
  '''


app.run(host='0.0.0.0', port=8080, debug=True)
