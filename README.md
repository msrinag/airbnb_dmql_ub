

# Airbnb Ratings Dataset Project

## Data Source
The dataset used for this project is available at: [Airbnb Ratings Dataset](https://www.kaggle.com/datasets/samyukthamurali/airbnb-ratings-dataset/data?select=airbnb_sample.csv)

## Hosted Website
Our project is hosted on: [Airbnb Ratings Streamlit App](https://dmql-pahse-2-excel-was-better.streamlit.app/)

## Recreating the Project

### Step 1: Preprocessing
- Run the `pahse2_preprocessing.ipynb` notebook.
- This will generate `airbnb_sample.csv`, which is the processed data for our database.

### Step 2: Database Setup
- Open the query tool in pgAdmin.
- Open `create.sql` and execute it.
  - This script will create all the required tables.

### Step 3: Data Loading
- Open `load.sql` and execute it.
  - This script will insert all the required production data into the tables.

### Step 4: Optional Operations
- Run `insert.sql` for inserting single records.
- Run `update.sql` for updating single records.
- Run `alter.sql` for altering single records.
- Ignore `mile1.sql`, as it's the old script for phase 1.

### Step 5: Additional Queries
- Explore the interesting outputs and insights from the database by running individual queries from `all_queries.sql`.
- Use `problematic.sql` to identify and visualize query flows by highlighting each query and clicking on the explain button.

### Step 6: Database Backup
- Utilize the backup dump file to recreate the database in pgAdmin.

### Step 7: Streamlit App Database
- Run `pgadmin_to_sql_db.ipynb` to generate a new database file for the Streamlit app.
  - This step eliminates the need for hosting a pgAdmin server.

### Step 8: Run the App
- Execute `streamlit run home.py` command to launch the Streamlit app.
- Enjoy exploring the app!

--- 

I've organized the steps in a clearer and more concise manner, ensuring each step is explained thoroughly. Let me know if you need further adjustments!
