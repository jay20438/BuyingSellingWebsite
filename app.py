from asyncio.windows_events import NULL
from unicodedata import name
import streamlit as st
import pandas as pd 
from db_fxns import * 
import streamlit.components.v1 as stc
from datetime import date

import plotly.express as px 

def main():
	menu = ["Home","Register as Buyer","Register as Seller","Sell Product","Update Your Product","View Products","Buy Product","Delete Product","Employee Access","About"]
	choice = st.sidebar.selectbox("Menu",menu)

	if choice == "Home":
		st.title("OSW")
		st.header("Welcome to OSW!!")
		st.text("Have a Happy Buying and Selling Experience")

	elif choice == "Register as Buyer":
		st.subheader("Enter your Details:")
		bname = st.text_input("Name")
		bphno = st.text_input("Phone No")
		bemail = st.text_input("Email")
		bstate = st.text_input("State")
		bzip = st.number_input("Postal Zip", step=1)
		bbudget = st.number_input("Budget", step=1)
		if st.button("Register"):
			add_buyer_data(bname, bphno, bemail, bstate, bzip, bbudget)
			st.warning("Hi '{}'! You are registered as a new Buyer".format(bname))

	elif choice == "Register as Seller":
		st.subheader("Enter your Details:")
		sname = st.text_input("Name")
		sphno = st.text_input("Phone No")
		semail = st.text_input("Email")
		sstate = st.text_input("State")
		szip = st.number_input("Postal Zip", step=1)
		
		if st.button("Register"):
			sid = add_seller_data(sname, sphno, semail, sstate, szip)
			st.warning("Hi '{}'! Your Unique Seller ID is '{}'".format(sname,sid))

	elif choice == "Sell Product":
		st.subheader("List your Product:")
		Name = st.text_input("Product Name")
		Type = st.text_input("Product Type")
		price = st.number_input("Price", step=1)
		qty = st.number_input("Quantity", step=1)
		dp = st.date_input("date posted")
		us = st.number_input("Use Status(in months)", step=1)
		sid = st.number_input("Enter your Seller ID", step=1)
		if st.button("Add Product"):
			add_data(Name, Type, price, qty, dp, us, sid)
			st.warning("Your Product: '{}' has been added".format(Name))

	elif choice == "View Products":
		st.subheader("Products")
		with st.expander("View Data"):
			result = view_all_data()
			clean_df = pd.DataFrame(result,columns=['product_name', 'product_type', 'price', 'quantity'])
			st.dataframe(clean_df)
		
		filterbycategory =  st.text_input("Select Category")
		filterbyprice =  st.number_input("Select Maximum Price", step=1)
		filterbystate =  st.text_input("Select State")

		if(len(filterbycategory)!=0) and (filterbyprice > 0) and (len(filterbystate)!=0):
			result2 = filter_3category(filterbycategory, filterbyprice, filterbystate)
			clean_df = pd.DataFrame(result2,columns=['product_name', 'product_type', 'price', 'quantity','state'])
			st.dataframe(clean_df)

		elif(len(filterbycategory)!=0) and (filterbyprice > 0):
			result2 = filter_4category(filterbycategory, filterbyprice)
			clean_df = pd.DataFrame(result2,columns=['product_name', 'product_type', 'price', 'quantity'])
			st.dataframe(clean_df)

		elif(len(filterbycategory)!=0) and (len(filterbystate) != 0):
			result2 = filter_5category(filterbycategory, filterbystate)
			clean_df = pd.DataFrame(result2,columns=['product_name', 'product_type', 'price', 'quantity','state'])
			st.dataframe(clean_df)

		elif(filterbyprice > 0) and (len(filterbystate) != 0):
			result2 = filter_6category(filterbyprice, filterbystate)
			clean_df = pd.DataFrame(result2,columns=['product_name', 'product_type', 'price', 'quantity','state'])
			st.dataframe(clean_df)
		
		else:
			if(len(filterbycategory)!=0):
				result2 = filter_category(filterbycategory)
				clean_df = pd.DataFrame(result2,columns=['product_name', 'product_type', 'price', 'quantity'])
				st.dataframe(clean_df)
		
			elif(filterbyprice > 0):
				result2 = filter_price(filterbyprice)
				clean_df = pd.DataFrame(result2,columns=['product_name', 'product_type', 'price', 'quantity'])
				st.dataframe(clean_df)
			
			elif(len(filterbystate)!=0):
				result2 = filter_state(filterbystate)
				clean_df = pd.DataFrame(result2,columns=['product_name', 'product_type', 'price', 'quantity','state'])
				st.dataframe(clean_df)        

	elif choice == "Update Your Product":
		sid = st.number_input("Enter your Seller ID:",step=1)
		if(sid > 0):
			with st.expander("Your Products:"):
				result = view_seller_specific_data(sid)
				clean_df = pd.DataFrame(result,columns=['product_name', 'product_type', 'price', 'quantity','seller_id'])
				st.dataframe(clean_df)
			list_of_updates = ['None','Product Name','Price','Quantity']
			selected_update = st.selectbox("Choose attribute you want to update",list_of_updates)
			if(selected_update == 'Product Name'):
				oldname = st.text_input("Enter old name:")
				pnameup = st.text_input("Enter new name:")
				if(len(oldname) > 0 and len(pnameup)>0):
					if st.button("Update Product"):
						edit_pname(oldname,pnameup,sid)
						st.success("Updated Product Name To {}".format(pnameup))
						with st.expander("View Updated Data"):
							result = view_seller_specific_data(sid)
							clean_df = pd.DataFrame(result,columns=['product_name', 'product_type', 'price', 'quantity','seller_id'])
							st.dataframe(clean_df)

			if(selected_update == 'Price'):
				prodname = st.text_input("Enter Product name:")
				nprice = st.number_input("Enter new Price:",step=1)
				if(len(prodname) > 0 and nprice>0):
					if st.button("Update Product"):
						edit_pprice(prodname,nprice,sid)
						st.success("Updated Product Price To {}".format(nprice))
						with st.expander("View Updated Data"):
							result = view_seller_specific_data(sid)
							clean_df = pd.DataFrame(result,columns=['product_name', 'product_type', 'price', 'quantity','seller_id'])
							st.dataframe(clean_df)

			if(selected_update == 'Quantity'):
				produname = st.text_input("Enter Product name:")
				nqty = st.number_input("Enter new Quantity:",step=1)
				if(len(produname) > 0 and nqty>0):
					if st.button("Update Product"):
						edit_pqty(produname,nqty,sid)
						st.success("Updated Product Quantity To {}".format(nqty))
						with st.expander("View Updated Data"):
							result = view_seller_specific_data(sid)
							clean_df = pd.DataFrame(result,columns=['product_name', 'product_type', 'price', 'quantity','seller_id'])
							st.dataframe(clean_df)

	elif choice == "Delete Product":
		st.subheader("Delete your Product")
		with st.expander("View Data"):
			result = view_se_data()
			clean_df = pd.DataFrame(result,columns=['product_name', 'product_type', 'price', 'quantity','seller_id'])
			st.dataframe(clean_df)

		pname =  st.text_input("Enter Product Name:")
		psid =  st.number_input("Enter your Seller ID:",step=1)

		if st.button("Delete"):
			delete_data(pname, psid)
			st.warning("Deleted: '{}'".format(pname))

		with st.expander("Updated Data"):
			result = view_se_data()
			clean_df = pd.DataFrame(result,columns=['product_name', 'product_type', 'price', 'quantity', 'seller_id'])
			st.dataframe(clean_df)

	elif choice == "Buy Product":
		st.subheader("Buy Product")
		with st.expander("View Data"):
			result = view_buy_data()
			clean_df = pd.DataFrame(result,columns=['product_id','product_name', 'product_type', 'price', 'quantity','seller_id'])
			st.dataframe(clean_df)
		
		pid = st.number_input("Enter Product ID",step=1)
		sid = st.number_input("Enter Seller ID",step=1)
		bname = st.text_input("Buyer Name")
		bphno = st.text_input("Buyer Phone No")
		datepu = st.date_input("Purchase Date")
		payment_method = ['None','UPI','Credit Card','Debit Card']
		paymode = st.selectbox("Choose Payment Method-",payment_method)
		pamount = st.number_input("Payment Amount",step=1)
		if st.button("Place Order"):
			payid = place_order(pid, sid, bphno, paymode, pamount,datepu)
			st.warning("Your order has been placed with Payment ID: '{}'".format(payid))

	elif choice == "Employee Access":
		list_of_views = ['None','Transactions','Purchases made by Buyers','Sellers Rating','Sellers Data','Buyers Data']
		selected_view = st.selectbox("Choose view:",list_of_views)
		if(selected_view == "Transactions"):
			with st.expander("View Data"):
				result = view_all_transactions()
				clean_df = pd.DataFrame(result,columns=['transaction id', 'amount', 'date', 'mode'])
				st.dataframe(clean_df)
		elif(selected_view == "Purchases made by Buyers"):
			with st.expander("View Data"):
				result = view_all_purbybuyers()
				clean_df = pd.DataFrame(result,columns=['buyer_id', 'product_id', 'amount'])
				st.dataframe(clean_df)
		elif(selected_view == "Sellers Rating"):
			with st.expander("View Data"):
				result = view_all_sellers_rating()
				clean_df = pd.DataFrame(result,columns=['id', 'name','rating'])
				st.dataframe(clean_df)
		elif(selected_view == "Sellers Data"):
			with st.expander("View Data"):
				result = view_all_sellers()
				clean_df = pd.DataFrame(result,columns=['id', 'name', 'phone_no','rating'])
				st.dataframe(clean_df)
		elif(selected_view == "Buyers Data"):
			with st.expander("View Data"):
				result = view_buyer_data()
				clean_df = pd.DataFrame(result,columns=['name','phone_no','email','state','postal_zip','budget'])
				st.dataframe(clean_df)
	
	elif choice == "About":
		st.subheader("Made By-")
		st.info("Kartik Jain")
		st.info("Jay Saraf")
		st.info("Teja Bhavani Shankar Parachoori")
		st.info("Vansh Gupta")

if __name__ == '__main__':
	main()

