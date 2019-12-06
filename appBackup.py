from budayaKB_model import BudayaItem, BudayaCollection
from flask import Flask, request, render_template, redirect, flash, url_for
from wtforms import Form, validators, TextField

app = Flask(__name__)
app.secret_key ="tp4"

#inisialisasi objek budayaData
databasefilename = ""
budayaData = BudayaCollection()

#merender tampilan default(index.html)
@app.route('/')
def index():
	return render_template("index.html", current_menu = None)



@app.route('/impor', methods=['GET', 'POST'])
def impor():
	if request.method == "GET":
		return render_template("impor.html", current_menu = 'import')

	elif request.method == "POST":
                f = request.files['file']
                global databasefilename
                databasefilename=f.filename
                result_impor=budayaData.importFromCSV(f.filename)
                budayaData.exportToCSV(databasefilename) #setiap perubahan data langsung disimpan ke file
                return render_template("impor.html", result=result_impor, fname=f.filename, current_menu = 'import')


@app.route('/add', methods=['GET', 'POST'])
def add():
	if request.method == "GET":
		return render_template("add.html", current_menu = 'edit')

	elif request.method == "POST":
                if databasefilename != '':
                        nama = request.form['name']
                        tipe = request.form['tipe']
                        prov = request.form['prov']
                        url = request.form['url']
                        same = False

                        for i in budayaData.koleksi.values():
                                if i.nama == nama:
                                        same = True
                        if same == False:
                                budayaData.tambah(nama, tipe, prov, url)
                                budayaData.exportToCSV(databasefilename) #setiap perubahan data langsung disimpan ke file
                                return render_template("add.html", name = nama, current_menu = 'edit')
                        else:
                                return render_template("add.html", nama = nama, current_menu = 'edit')
                else:
                        return render_template("add.html", imported = False, current_menu = 'edit')


@app.route('/update', methods=['GET', 'POST'])
def update():
	if request.method == "GET":
		return render_template("update.html", current_menu = 'edit')

	elif request.method == "POST":
                if databasefilename != '':
                        nama = request.form['name']
                        tipe = request.form['tipe']
                        prov = request.form['prov']
                        url = request.form['url']
                        same = False

                        for i in budayaData.koleksi.values():
                                if i.nama == nama:
                                        same = True
                        if same == True:
                                budayaData.ubah(nama, tipe, prov, url)
                                budayaData.exportToCSV(databasefilename) #setiap perubahan data langsung disimpan ke file
                                return render_template("update.html", name = nama, current_menu = 'edit' )
                        else:
                                return render_template("update.html", nama = nama, current_menu = 'edit' )
                else:
                        return render_template("update.html", imported = False, current_menu = 'edit')


@app.route('/remove', methods=['GET', 'POST'])
def remove():
	if request.method == "GET":
		return render_template("remove.html", current_menu = 'edit')

	elif request.method == "POST":
                if databasefilename != '':
                        nama = request.form['name']
                        same = False

                        for i in budayaData.koleksi.values():
                                if i.nama == nama:
                                        same = True
                        if same == True:
                                budayaData.hapus(nama)
                                budayaData.exportToCSV(databasefilename) #setiap perubahan data langsung disimpan ke file
                                return render_template("remove.html", name = nama, current_menu = 'edit' )
                        else:
                                return render_template("remove.html", nama = nama, current_menu = 'edit' )
                else:
                        return render_template("remove.html", imported = False, current_menu = 'edit')


@app.route('/search', methods=['GET', 'POST'])
def search():
	if request.method == "GET":
		return render_template("search.html", current_menu = 'search')

	elif request.method == "POST":
                if databasefilename != '':
                        mode = request.form['mode']
                        keyword = request.form['keyword']
                        if mode == 'name':
                                result = budayaData.cariByNama(keyword)
                        elif mode == 'tipe':
                                result = budayaData.cariByTipe(keyword)
                        elif mode == 'prov':
                                result = budayaData.cariByProv(keyword)
                        if result != []:
                                return render_template('search.html', result = result, current_menu = 'search')
                        else:
                                return render_template("search.html", keyword = keyword, current_menu = 'search')
                else:
                        return render_template("search.html", imported = False, current_menu = 'search')


@app.route('/stats', methods=['GET', 'POST'])
def stats():
	if request.method == "GET":
		return render_template("stats.html", current_menu = 'stats')

	elif request.method == "POST":
                if databasefilename != '':
                        mode = request.form['mode']
                        if mode == 'name':
                                result1 = budayaData.stat()
                                items = budayaData.showAll()
                                return render_template('stats.html', result1 = result1, all = items, current_menu = 'stats')
                        elif mode == 'tipe':
                                result2 = budayaData.statByTipe()
                                return render_template('stats.html', result2 = result2, current_menu = 'stats')
                        elif mode == 'prov':
                                result3 = budayaData.statByProv()
                                return render_template('stats.html', result3 = result3, current_menu = 'stats')
                else:
                        return render_template("search.html", imported = False, current_menu = 'stats')




if __name__ == "__main__":
    app.run(debug=True)


