from flask import Flask, request, jsonify
import sqlite3
import json

app=Flask(__name__)

def db_connection():
    conn = None
    try:
        conn=sqlite3.connect('datas.sqlite')
    except sqlite3.error as e:
        print(e)
    return conn


@app.route('/users', methods=['GET', 'POST'])
def data():
    conn = db_connection()
    cursor = conn.cursor()
    if request.method=='GET':
        cursor = conn.execute('select * from data')
        datas= [
            dict(id=row[0],first_name=row[1],last_name=row[2],company_name=row[3],
            age=row[4],city=row[5],state=row[6],zip=row[7],email=row[8],web=row[9])
            for row in cursor.fetchall()
        ]
        if datas is not None:
            return jsonify(datas)

    if request.method=='POST':
        n_first_name = request.form['first_name']
        n_last_name = request.form['last_name']
        n_company_name = request.form['company_name']
        n_city = request.form['city']
        n_state = request.form['state']
        n_zip = request.form['zip']
        n_email = request.form['email']
        n_web = request.form['web']
        n_age = request.form['age']
        sql= """INSERT INTO data(first_name,last_name,company_name,city,state,zip,email,web,age)
                VALUES (?,?,?,?,?,?,?,?,?)"""
        cursor.execute(sql, (n_first_name,n_last_name,n_company_name,n_city,n_state,n_zip,n_email,n_web,n_age))
        conn.commit()
        return f"Data with the id: {cursor.lastrowid} created successfully", 201

@app.route('/users/<int:id>', methods=['GET','PUT','DELETE'])
def single_data(id):
    conn = db_connection()
    cursor = conn.cursor()
    data=None
    if request.method=='GET':
        cursor.execute('SELECT * FROM data WHERE id=?', (id,))
        rows = cursor.fetchall()
        for r in rows:
            data=r
        if data is not None:
            return jsonify(data), 200
        else:
            return "something wrong", 404

    if request.method=='PUT':
        sql=""" UPDATE data SET
                first_name = ?,
                last_name=?, 
                age=?
                WHERE id=?"""
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        age = request.form['age']

        updated_data={
                    'id':id,
                    'first_name': first_name,
                    'last_name': last_name,
                    'age':age
                }
        conn.execute(sql, (first_name,last_name,age, id))
        conn.commit()
        return jsonify(updated_data)

    if request.method=='DELETE':
        sql="""DELETE FROM data WHERE id=?"""
        conn.execute(sql, (id,))
        conn.commit()
        return "Book with the id: {} has been deleted successfully".format(id), 200


if __name__ == '__main__':
    app.run(debug=True)