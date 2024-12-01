import streamlit as st
import requests
import json

# Streamlit title
st.title("Backend System API Tester")

# Select the database type (MySQL or MongoDB)
db_type = st.selectbox("Select Database Type", ["MySQL", "MongoDB"])

# Fetch the list of tables/collections from the backend
if db_type == "MySQL":
    response = requests.get("http://localhost:5000/api/list_tables?db_type=mysql")
elif db_type == "MongoDB":
    response = requests.get("http://localhost:5000/api/list_tables?db_type=mongodb")

# Check for successful response
if response.status_code == 200:
    data = response.json()
    tables_or_collections = data.get("tables") if db_type == "MySQL" else data.get("collections")
    if tables_or_collections:
        # Select the table or collection from the list
        table_name = st.selectbox("Select Table/Collection", tables_or_collections)
    else:
        st.error("No tables or collections found.")
else:
    st.error("Failed to fetch tables or collections from the backend.")

# Select CRUD Operation
operation = st.selectbox("Select Operation", ["Create", "Read", "Update", "Delete"])

# Input Fields for Create and Update
if operation in ["Create", "Update"]:
    data_input = st.text_area("Enter Data in JSON format (e.g., {\"name\": \"John\", \"email\": \"john@example.com\"})")
    if data_input:
        try:
            data = json.loads(data_input)
        except json.JSONDecodeError:
            st.error("Invalid JSON format. Please check your input.")
            data = None

# Record ID for Update and Delete
if operation in ["Update", "Delete"]:
    record_id = st.text_input("Enter Record ID (for MongoDB, use the ObjectId as a string)")

# Perform the Operation
if st.button("Submit"):
    base_url = f"http://localhost:5000/api/{table_name}"
    params = {"use_mongodb": "true"} if db_type == "MongoDB" else {}

    try:
        if operation == "Create" and data:
            response = requests.post(f"{base_url}/create", json=data, params=params)
        elif operation == "Read":
            response = requests.get(f"{base_url}/read", params=params)
        elif operation == "Update" and data:
            response = requests.put(f"{base_url}/update/{record_id}", json=data, params=params)
        elif operation == "Delete":
            response = requests.delete(f"{base_url}/delete/{record_id}", params=params)
        else:
            st.error("Missing required fields.")

        # Display the Response
        if response.status_code == 200:
            st.write("Success:", response.json())
        else:
            st.write("Error:", response.json())

    except Exception as e:
        st.write("An error occurred:", str(e))
