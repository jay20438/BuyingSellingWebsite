import mysql.connector

mydb = mysql.connector.connect(host = "localhost", user = "root", passwd = "123456", database = "endsemeval")

c = mydb.cursor()


def create_table():
	c.execute('CREATE TABLE IF NOT EXISTS taskstable(task TEXT,task_status TEXT,task_due_date DATE)')

def add_buyer_data(bname, bphno, bemail, bstate, bzip, bbudget):
	c.execute('INSERT INTO buyers(name,phone_no,email,state,postal_zip,budget) VALUES (%s,%s,%s,%s,%s,%s)', (bname, bphno, bemail, bstate, bzip, bbudget))
	mydb.commit()

def add_seller_data(sname, sphno, semail, sstate, szip):
	c.execute('INSERT INTO sellers(name,phone_no,email,state,postal_zip,rating) VALUES (%s,%s,%s,%s,%s,%s)', (sname, sphno, semail, sstate, szip, 0))
	mydb.commit()
	c.execute('SELECT id FROM sellers WHERE id=(SELECT MAX(id) FROM sellers)')
	data = c.fetchall()
	return data[0][0]

def add_data(name, type, price, qty, dp, us, sid):
	c.execute('INSERT INTO products(product_name, product_type, price, quantity, date_posted, use_status, seller_id) VALUES (%s,%s,%s,%s,%s,%s,%s)', (name, type, price, qty, dp, us, sid))
	mydb.commit()

def view_all_data():
	c.execute('SELECT product_name, product_type, price, quantity FROM products')
	data = c.fetchall()
	return data

def view_all_transactions():
	c.execute('SELECT * FROM transactions')
	data = c.fetchall()
	return data

def view_all_purbybuyers():
	c.execute('SELECT * FROM buyers_purchases')
	data = c.fetchall()
	return data

def view_all_sellers_rating():
	c.execute('SELECT * FROM sellers_rating')
	data = c.fetchall()
	return data

def view_all_sellers():
	c.execute('SELECT * FROM sellers_data')
	data = c.fetchall()
	return data

def view_se_data():
	c.execute('SELECT product_name, product_type, price, quantity,seller_id FROM products')
	data = c.fetchall()
	return data

def view_buy_data():
	c.execute('SELECT id,product_name, product_type, price, quantity, seller_id FROM products')
	data = c.fetchall()
	return data

def view_seller_specific_data(sid):
	fstr = f"SELECT product_name, product_type, price, quantity, seller_id FROM products WHERE seller_id = '{sid}';"
	c.execute(fstr)
	data = c.fetchall()
	return data

def view_seller_data():
	c.execute('SELECT name,phone_no,email,state,postal_zip FROM sellers')
	data = c.fetchall()
	return data

def view_buyer_data():
	c.execute('SELECT name,phone_no,email,state,postal_zip,budget FROM buyers')
	data = c.fetchall()
	return data

# def filter_category(filter):
# 	fstr = f"SELECT product_name, product_type, price, quantity FROM products WHERE product_type = '{filter}';"
# 	c.execute(fstr)
# 	data = c.fetchall()
# 	return data

def filter_category(filter):
	fstr = f"SELECT product_name, product_type, price, quantity FROM products WHERE product_type = '{filter}';"
	c.execute(fstr)
	data = c.fetchall()
	return data

def filter_price(filter):
	fstr = f"SELECT product_name, product_type, price, quantity FROM products WHERE price <= '{filter}';"
	c.execute(fstr)
	data = c.fetchall()
	return data

def filter_state(filter):
	fstr = f"SELECT product_name, product_type, price, quantity, state FROM endsemeval.products P, endsemeval.sellers S WHERE P.seller_id = S.id AND S.state = '{filter}';"
	c.execute(fstr)
	data = c.fetchall()
	return data

def filter_3category(filterbycategory, filterbyprice, filterbystate):
	fstr = f"SELECT product_name, product_type, price, quantity, state FROM endsemeval.products P, endsemeval.sellers S WHERE P.seller_id = S.id AND S.state = '{filterbystate}' AND price <= '{filterbyprice}' AND product_type = '{filterbycategory}';"
	c.execute(fstr)
	data = c.fetchall()
	return data

def filter_4category(filterbycategory, filterbyprice):
	fstr = f"SELECT product_name, product_type, price, quantity FROM endsemeval.products WHERE price <= '{filterbyprice}' AND product_type = '{filterbycategory}';"
	c.execute(fstr)
	data = c.fetchall()
	return data

def filter_5category(filterbycategory, filterbystate):
	fstr = f"SELECT product_name, product_type, price, quantity, state FROM endsemeval.products P, endsemeval.sellers S WHERE P.seller_id = S.id AND S.state = '{filterbystate}' AND product_type = '{filterbycategory}';"
	c.execute(fstr)
	data = c.fetchall()
	return data

def filter_6category(filterbyprice, filterbystate):
	fstr = f"SELECT product_name, product_type, price, quantity, state FROM endsemeval.products P, endsemeval.sellers S WHERE P.seller_id = S.id AND S.state = '{filterbystate}' AND price <= '{filterbyprice}';"
	c.execute(fstr)
	data = c.fetchall()
	return data

def delete_data(name,sid):
	fstr = f"DELETE FROM products P WHERE P.seller_id = '{sid}' AND P.product_name = '{name}';"
	c.execute(fstr)
	mydb.commit()

def edit_pname(oldname,nname,sid):
	fstr = f"UPDATE products SET product_name = '{nname}' WHERE product_name =  '{oldname}'and seller_id =  '{sid}';"
	c.execute(fstr)
	mydb.commit()
	data = c.fetchall()
	return data

def edit_pprice(oldname,nprice,sid):
	fstr = f"UPDATE products SET price = '{nprice}' WHERE product_name =  '{oldname}'and seller_id =  '{sid}';"
	c.execute(fstr)
	mydb.commit()
	data = c.fetchall()
	return data

def edit_pqty(prodname,nqty,sid):
	fstr = f"UPDATE products SET quantity = '{nqty}' WHERE product_name =  '{prodname}'and seller_id =  '{sid}';"
	c.execute(fstr)
	mydb.commit()
	data = c.fetchall()
	return data

def getbuyerid(bphno):
	fstr2 = f"SELECT id FROM endsemeval.buyers WHERE buyers.phone_no = '{bphno}';"
	c.execute(fstr2)
	data = c.fetchall()
	return data[0][0]

def place_order(pid, sid, bphno, paymode, pamount,datetoday):
	fstr = f"DELETE FROM products P WHERE P.id = '{pid}';"
	c.execute(fstr)
	mydb.commit()

	bid = getbuyerid(bphno)
	c.execute('INSERT INTO payment(mode,amount,date,buyer_id,seller_id,product_id) VALUES (%s,%s,%s,%s,%s,%s)', (paymode, pamount, datetoday, bid, sid, pid))
	
	mydb.commit()

	c.execute('SELECT id FROM payment WHERE id=(SELECT MAX(id) FROM payment)')
	data2 = c.fetchall()
	return data2[0][0]