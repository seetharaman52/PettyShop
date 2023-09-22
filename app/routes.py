import datetime
from flask import *
from app import app
import mysql.connector
mydb = mysql.connector.connect(host="localhost", user="root", password="kit@1234")
my_cursor = mydb.cursor()
my_cursor.execute("use myshop")

@app.route("/logout", methods=["GET", "POST"])
def log_out():
    session["logged_in"] = False
    return redirect(url_for("index"))


@app.route('/', methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    username = None
    password = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        u_query = "select * from users_list where user = %s"
        my_cursor.execute(u_query,(username,))
        res = my_cursor.fetchone()
        if res and res[0] == username and res[0] == password:
            session["logged_in"] = True
            query = "select cash_balance from company where company_name = %s"
            my_cursor.execute(query, ("Stationery Paradise",))
            amount = my_cursor.fetchall()
            return render_template('main.html', items=list_of_items(),
                                   cash_balance=amount[0][0], available_items=list_of_items())
        else:
            return render_template("error.html")


@app.route("/main_page")
def main_page():
    query = "select cash_balance from company where company_name = %s"
    my_cursor.execute(query, ("Stationery Paradise",))
    amount = my_cursor.fetchall()
    return render_template('main.html', items=list_of_items(),
                           cash_balance=amount[0][0], available_items=list_of_items(),
                           his=list_of_items_history())


def list_of_items():
    query = "select * from item where price >= 0"
    my_cursor.execute(query)
    res = my_cursor.fetchall()
    if res:
        return res
    return ""


def list_of_items_history():
    query = "select * from purchase"
    my_cursor.execute(query)
    res = my_cursor.fetchall()
    if res:
        return res
    return ""

@app.route("/adding_items", methods=["GET", "POST"])
def add_items():
    id_ = request.form.get("ItemId")
    item_name = request.form.get("ItemName")
    rate = request.form.get("rate")
    try:
        query = "insert into item(item_id, item_name, price) values(%s, %s, %s)"
        my_cursor.execute(query,(id_, item_name, rate,))
        mydb.commit()
    except:
        return render_template("itemExist.html")
    return redirect(url_for("main_page"))


@app.route("/purchasing_items", methods=["GET", "POST"])
def purchase_items():
    current_datetime = datetime.datetime.now()
    date = current_datetime.strftime("%Y-%m-%d")
    time = current_datetime.strftime("%H:%M:%S")
    item_id = request.form.get("item_id")
    qty = int(request.form.get("qty"))
    rate = int(request.form.get("rate"))
    amount = qty * rate

    my_cursor.execute("select max(purchase_id) from purchase")
    max_id = my_cursor.fetchone()[0]
    max_id = max_id + 1 if max_id else 1

    query = "select * from item where item_id=%s"
    my_cursor.execute(query, (item_id,))
    if my_cursor.fetchone():
        query = "select qty from item_qty where item_id=%s"
        my_cursor.execute(query, (item_id,))
        existing_qty = my_cursor.fetchone()

        if existing_qty:
            new_qty = existing_qty[0] + qty
            query = "update item_qty set qty=%s where item_id=%s"
            my_cursor.execute(query, (new_qty, item_id,))
        else:
            query = "insert into item_qty(item_id, qty) values(%s, %s)"
            my_cursor.execute(query, (item_id, qty,))
        query = ("insert into purchase(purchase_id, purchase_date, purchase_time, item_id, qty, rate, amount) "
                 "values(%s, %s, %s, %s, %s, %s, %s)")
        data = (max_id, date, time, item_id, qty, rate, amount)
        my_cursor.execute(query, data)
        query = "UPDATE company SET cash_balance = cash_balance - %s WHERE company_name = %s"
        my_cursor.execute(query, (amount, "Stationery Paradise"))
        query = "select price from item where item_id=%s"
        my_cursor.execute(query, (item_id,))
        res = my_cursor.fetchall()
        item_price = int(res[0][0])
        if int(rate) != item_price:
            query = "update item set price = %s where item_id = %s"
            my_cursor.execute(query, (rate, item_id,))
        mydb.commit()
        return redirect(url_for("main_page"))


@app.route("/remove_item", methods=["GET","POST"])
def remove_item():
    name = request.form.get("item_id")
    query = "delete from item where item_id=%s"
    my_cursor.execute(query,(name,))
    mydb.commit()
    query = "update item_qty set qty=%s where item_id=%s"
    my_cursor.execute(query,(0, name,))
    mydb.commit()
    return redirect(url_for("main_page"))


@app.route("/add_cash", methods=["GET", "POST"])
def add_cash():
    success = True
    added_amount = request.form.get('credit')
    query = "select cash_balance from company where company_name = %s"
    my_cursor.execute(query, ("Stationery Paradise",))
    amount = my_cursor.fetchone()
    if amount is None:
        success = False
    else:
        amount = amount[0]
        new_amount = int(amount) + int(added_amount)
        update_query = "update company set cash_balance = %s where company_name = %s"
        try:
            my_cursor.execute(update_query, (new_amount, 'Stationery Paradise'))
            mydb.commit()
        except:
            mydb.rollback()
            success = False
    return redirect(url_for("main_page"))


@app.route("/sell_items", methods=["POST", "GET"])
def sell_items():
    current_datetime = datetime.datetime.now()
    date = current_datetime.strftime("%Y-%m-%d")
    time = current_datetime.strftime("%H:%M:%S")
    my_cursor.execute("select max(sales_id) from sales")  # 0
    res = my_cursor.fetchall()
    max_id = res[0][0]
    if not max_id:
        max_id = 1
    elif max_id:
        max_id = max_id + 1
    item_id = request.form.get("ItemId")
    qty = request.form.get("qty")
    rate = request.form.get("rate")
    check = items_available(item_id, qty)
    if check[0]:
        available_qty = check[1]
        rem = int(available_qty) - int(qty)
        if int(available_qty) >= int(qty):
            amount = int(rate)*int(qty)
            query = ("insert into sales(sales_id, sales_date, sales_time, item_id,"
                     "qty, rate, amount) values(%s, %s, %s, %s, %s, %s, %s)")
            my_cursor.execute(query, (max_id, date, time, item_id, qty, rate, amount,))
            mydb.commit()
            query = "select cash_balance from company where company_name = %s"
            my_cursor.execute(query, ("Stationery Paradise",))
            amount_db = my_cursor.fetchall()
            amount_db = amount_db[0][0]
            new_amount = amount_db + amount
            update_query = "update company set cash_balance = %s where company_name = %s"
            my_cursor.execute(update_query, (new_amount, 'Stationery Paradise'))
            mydb.commit()
            query = "update item_qty set qty=%s where item_id=%s"
            my_cursor.execute(query, (rem, item_id,))
            mydb.commit()
            return redirect(url_for("main_page"))
        else:
            return "<h1>Selling item qty is too high!</h1>"
    return redirect(url_for("main_page"))


def items_available(item_id, qty):
    query = "select qty from item_qty where item_id=%s"
    my_cursor.execute(query, (item_id,))
    res = my_cursor.fetchall()
    if res:
        return [True, res[0][0]]
    return [False, res[0][0]]


def get_qty(item_id):
    query = "select qty from item_qty where item_id = %s"
    my_cursor.execute(query, (item_id,))
    res = my_cursor.fetchall()
    try:
        return res[0][0]
    except:
        return 0


@app.route("/add_user")
def add_user():
    user_name = request.form.get('username')
    pass_word = request.form.get('password')
    query = "select user from users_list"
    my_cursor.execute(query)
    res = my_cursor.fetchall()
    if res[0][0] != user_name:
        q = "insert into users_list(user, secretkey) values(%s, %s)"
        my_cursor.execute(q,(user_name, pass_word,))
        mydb.commit()
        return render_template("userAdded.html")
    else:
        return render_template("userExist.html")


@app.route("/check_item_exists_1")
def check_item_exists_1():
    item_id = request.args.get("item_id")
    query = "select item_id from item where item_id = %s"
    my_cursor.execute(query, (item_id,))
    item_exists = bool(my_cursor.fetchone())
    return jsonify({"exists": item_exists})


@app.route("/check_item_exists_2")
def check_item_exists_2():
    item_id = request.args.get("item_id")
    query = "SELECT item_id, qty FROM item_qty WHERE item_id = %s"
    my_cursor.execute(query, (item_id,))
    item = my_cursor.fetchone()
    response = {"exists": bool(item), "available_qty": item[1] if item else 0}
    return jsonify(response)


app.jinja_env.globals.update(get_qty=get_qty)
