from flask import Flask, render_template, url_for, redirect, flash, session
from flask import request
from flask_mysqldb import MySQL


application = Flask(__name__)
application.config['MYSQL_HOST'] = 'localhost'
application.config['MYSQL_USER'] = 'root'
application.config['MYSQL_PASSWORD'] = ''
application.config['MYSQL_DB'] = 'uts_natanael'
mysql = MySQL(application)

@application.route('/')

@application.route('/index')
def index():
    return render_template('index.html')

@application.route('/login', methods=['GET','POST'])
def login():
    cur = mysql.connection.cursor()
    cur.execute("select *from pengguna")
    userlist = cur.fetchall()
    cur.close()
    if request.method == 'GET':
        return render_template('index2.html', userlist=userlist)	
    elif request.method =='POST':
        user = request.form['username']			
        passwd = request.form['password']		
    	
        for kolom in userlist:
            for i in range(len(kolom)):
                if str(user) == kolom[i]:
                    if str(passwd) == kolom[i+1]:
                        return redirect(url_for('tabel1'))
                    else:
                        break
        flash('invalid username/password', 'error')
        return render_template('index2.html')
    return render_template('index2.html')

@application.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('index3.html')	

    elif request.method == 'POST':
        user = request.form['username']			
        password = request.form['password']	
        passwordconfirm = request.form['passwordconfirmation']

        if password == passwordconfirm:
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO pengguna (Nama_pengguna, kata_kunci) values(%s, %s)', (user, password))
            mysql.connection.commit()
            cur.close()
        else:
            flash('Salahhhhhh')
        return render_template('index3.html')

@application.route('/tabel1')
def tabel1():
    cur = mysql.connection.cursor()
    cur.execute("select *from guru")
    guru = cur.fetchall()
    cur.close()
    return render_template('tabel1.html', data=guru)

@application.route('/newdata_guru')
def newdata_guru():
    return render_template('newdata_guru.html')

@application.route('/simpanform_guru', methods=['POST'])
def simpanform_guru():
    nip=request.form['nip']
    nama=request.form['nama']
    alamat=request.form['alamat']
    tem_lahir=request.form['tem_lahir']
    tang_lahir=request.form['tang_lahir']
    gender=request.form['gender']
    agama=request.form['agama']
    no_tel=request.form['no_tel']
    pendidikan=request.form['pendidikan']
    status=request.form['status']
    cur = mysql.connection.cursor()
    cur.execute('insert into guru(nip, nama, alamat, tmp_lahir, tgl_lahir, gender, agama, telp, pendidikan, status) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (nip, nama, alamat, tem_lahir, tang_lahir, gender, agama, no_tel, pendidikan, status))
    mysql.connection.commit()
    cur.close()
    return redirect('tabel1')

@application.route('/edit/<int:nip>', methods=['GET', 'POST'])
def edit(nip):
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT *FROM guru WHERE nip=%s', (nip, ))
        guru = cursor.fetchone()
        cursor.close()
        return render_template('edit_guru.html', guru=guru)

    else:
        nama=request.form['nama']
        alamat=request.form['alamat']
        tem_lahir=request.form['tem_lahir']
        tang_lahir=request.form['tang_lahir']
        gender=request.form['gender']
        agama=request.form['agama']
        no_tel=request.form['no_tel']
        pendidikan=request.form['pendidikan']
        status=request.form['status']
        cur = mysql.connection.cursor()
        cur.execute('UPDATE guru SET nama = %s, alamat = %s, tmp_lahir = %s, tgl_lahir = %s, gender = %s, agama = %s, telp = %s, pendidikan = %s, status = %s WHERE nip = %s;', (nama, alamat, tem_lahir, tang_lahir, gender, agama, no_tel, pendidikan, status, nip))
        mysql.connection.commit()
        cur.close()
        return redirect(('/tabel1'))

    return render_template('/tabel1.html')     

@application.route('/delete/<int:nip>', methods=['GET'])
def delete(nip):
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM guru WHERE nip=%s', (nip, ))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('tabel1'))

    return render_template('/tabel1.html')

@application.route('/tabel2')
def tabel2():
    cur = mysql.connection.cursor()
    cur.execute("select *from orang_tua")
    ortu = cur.fetchall()
    cur.close()
    return render_template('tabel_ortu.html', data=ortu)

@application.route('/newdata_ortu')
def newdata_ortu():
    return render_template('newdata_ortu.html')

@application.route('/simpanform_ortu', methods=['POST'])
def simpanform_ortu():
    kd=request.form['kd']
    nama=request.form['nama']
    alamat=request.form['alamat']
    telp=request.form['telp']
    pekerjaan=request.form['pekerjaan']
    agama=request.form['agama']
    status=request.form['status']
    cur = mysql.connection.cursor()
    cur.execute('insert into orang_tua(kd_ortu, Nama, Alamat, Telp, Pekerjaan, Agama,Status) values(%s, %s, %s, %s, %s, %s, %s)', (kd, nama, alamat, telp, pekerjaan, agama, status))
    mysql.connection.commit()
    cur.close()
    return redirect('tabel2')

@application.route('/edit_ortu/<int:kd>', methods=['GET', 'POST'])
def edit_ortu(kd):
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT *FROM orang_tua WHERE kd_ortu=%s', (kd, ))
        ortu = cursor.fetchone()
        cursor.close()
        return render_template('edit_ortu.html', ortu=ortu)

    else:
        nama=request.form['nama']
        alamat=request.form['alamat']
        telp=request.form['telp']
        pekerjaan=request.form['pekerjaan']
        agama=request.form['agama']
        status=request.form['status']
        cur = mysql.connection.cursor()
        cur.execute('UPDATE orang_tua SET Nama = %s, Alamat = %s, Telp = %s, Pekerjaan = %s, Agama = %s, Status = %s WHERE kd_ortu = %s;', (nama, alamat, telp, pekerjaan, agama, status, kd))
        mysql.connection.commit()
        cur.close()
        return redirect(('/tabel2'))

    return render_template('/tabel_ortu.html')     

@application.route('/delete_ortu/<int:kd>', methods=['GET'])
def delete_ortu(kd):
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM orang_tua WHERE kd_ortu=%s', (kd, ))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('tabel2'))

    return render_template('/tabel_ortu.html')

@application.route('/tabel3')
def tabel3():
    cur = mysql.connection.cursor()
    cur.execute("select *from siswa")
    siswa = cur.fetchall()
    cur.close()
    return render_template('tabel_siswa.html', data=siswa)

@application.route('/newdata_siswa')
def newdata_siswa():
    return render_template('newdata_siswa.html')

@application.route('/simpanform_siswa', methods=['POST'])
def simpanform_siswa():
    nis=request.form['nis']
    nama=request.form['nama']
    alamat=request.form['alamat']
    tem_lahir=request.form['tem_lahir']
    tang_lahir=request.form['tang_lahir']
    gender=request.form['gender']
    agama=request.form['agama']
    id_kelas=request.form['id_kelas']
    kd_ortu=request.form['kd_ortu']
    tgl_daftar=request.form['tgl_daftar']
    cur = mysql.connection.cursor()
    cur.execute('insert into siswa(Nis, Nama, Alamat, Tmp_lahir, Tgl_lahir, Gender, Agama, Id_kelas, Kd_ortu, Tgl_daftar) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (nis, nama, alamat, tem_lahir, tang_lahir, gender, agama, id_kelas, kd_ortu, tgl_daftar))
    mysql.connection.commit()
    cur.close()
    return redirect('tabel3')

@application.route('/edit_siswa/<int:nis>', methods=['GET', 'POST'])
def edit_siswa(nis):
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT *FROM siswa WHERE Nis=%s', (nis, ))
        siswa = cursor.fetchone()
        cursor.close()
        return render_template('edit_siswa.html', siswa=siswa)

    else:
        nama=request.form['nama']
        alamat=request.form['alamat']
        tem_lahir=request.form['tem_lahir']
        tang_lahir=request.form['tang_lahir']
        gender=request.form['gender']
        agama=request.form['agama']
        id_kelas=request.form['id_kelas']
        kd_ortu=request.form['kd_ortu']
        tgl_daftar=request.form['tgl_daftar']
        cur = mysql.connection.cursor()
        cur.execute('UPDATE siswa SET Nama = %s, Alamat = %s, Tmp_lahir = %s, Tgl_lahir = %s, Gender = %s, Agama = %s, Id_kelas = %s, Kd_ortu = %s, Tgl_daftar = %s WHERE Nis = %s;', (nama, alamat, tem_lahir, tang_lahir, gender, agama, id_kelas, kd_ortu, tgl_daftar, nis))
        mysql.connection.commit()
        cur.close()
        return redirect(('/tabel3'))

    return render_template('/tabel3.html')     

@application.route('/delete_siswa/<int:nis>', methods=['GET'])
def delete_siswa(nis):
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM siswa WHERE Nis=%s', (nis, ))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('tabel3'))

    return render_template('/tabel3.html')

@application.route('/tabel4')
def tabel4():
    cur = mysql.connection.cursor()
    cur.execute("select *from kelas")
    kelas = cur.fetchall()
    cur.close()
    return render_template('tabel_kelas.html', data=kelas)

@application.route('/newdata_kelas')
def newdata_kelas():
    return render_template('newdata_kelas.html')

@application.route('/simpanform_kelas', methods=['POST'])
def simpanform_kelas():
    id_kelas=request.form['id_k']
    kelas=request.form['kelas']
    nip=request.form['nip']
    cur = mysql.connection.cursor()
    cur.execute('insert into kelas(id_kelas, Kelas, Nip) values(%s, %s, %s)', (id_kelas, kelas, nip))
    mysql.connection.commit()
    cur.close()
    return redirect('tabel4')

@application.route('/edit_kelas/<int:id_kelas>', methods=['GET', 'POST'])
def edit_kelas(id_kelas):
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT *FROM kelas WHERE id_kelas=%s', (id_kelas, ))
        kelas = cursor.fetchone()
        cursor.close()
        return render_template('edit_kelas.html', kelas=kelas)

    else:
        kelas=request.form['kelas']
        nip=request.form['nip']
        cur = mysql.connection.cursor()
        cur.execute('UPDATE kelas SET Kelas = %s, Nip = %s WHERE id_kelas = %s; ',(kelas, nip, id_kelas))
        mysql.connection.commit()
        cur.close()
        return redirect(('/tabel4'))

    return render_template('/tabel_kelas.html')     

@application.route('/delete_kelas/<int:id_kelas>', methods=['GET'])
def delete_kelas(id_kelas):
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM kelas WHERE id_kelas=%s', (id_kelas, ))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('tabel4'))

    return render_template('/tabel_kelas.html')

@application.route('/tabel5')
def tabel5():
    cur = mysql.connection.cursor()
    cur.execute("select *from mapel")
    mapel = cur.fetchall()
    cur.close()
    return render_template('tabel_mapel.html', data=mapel)

@application.route('/newdata_mapel')
def newdata_mapel():
    return render_template('newdata_mapel.html')

@application.route('/simpanform_mapel', methods=['POST'])
def simpanform_mapel():
    id_mapel=request.form['id_m']
    mapel=request.form['mapel']
    cur = mysql.connection.cursor()
    cur.execute('insert into mapel(Id_mapel, Mapel) values(%s, %s)', (id_mapel, mapel))
    mysql.connection.commit()
    cur.close()
    return redirect('tabel5')

@application.route('/edit_mapel/<int:id_mapel>', methods=['GET', 'POST'])
def edit_mapel(id_mapel):
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT *FROM mapel WHERE Id_mapel=%s', (id_mapel, ))
        mapel = cursor.fetchone()
        cursor.close()
        return render_template('edit_mapel.html', mapel=mapel)

    else:
        mapel=request.form['mapel']
        cur = mysql.connection.cursor()
        cur.execute('UPDATE mapel SET Mapel = %s WHERE Id_mapel = %s; ',(mapel, id_mapel))
        mysql.connection.commit()
        cur.close()
        return redirect(('/tabel5'))

    return render_template('/tabel_mapel.html')     

@application.route('/delete_mapel/<int:id_mapel>', methods=['GET'])
def delete_mapel(id_mapel):
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM mapel WHERE Id_mapel=%s', (id_mapel, ))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('tabel5'))

    return render_template('/tabel_mapel.html')


if __name__ == '__main__':
    application.run(debug=True)