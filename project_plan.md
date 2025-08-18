# Financial Tracker

---

### **Project Plan: Financial Tracker**

Project Objective:

- To create an application for tracking financial expenses.

---

### **1. Scope and Goals**

**Minimum Viable Product (MVP):**

- Creation/Deletion of expenses with  these fields:
    - Date
    - Vendor
    - Currency
    - Amount
    - Type of payment
    - Category
        - Subcategory
    - Account
- View of Expenses:
    - Date
    - Business
    - Currency
    - Amount
    - Type of payment
    - Category
        - Subcategory
    - Account
- Creation/Deletion of Account
    - Name
    - Currency
    - Current Balance
    - Transaction
        - Credit/Debit

**Future Features:**

- Receipt Scanner
- Annotation/description field

---

### **2. Research and Design**

**Technology Stack:**

- **Language: Python, SQL**
- **Libraries/Tools:**
    - SQLite (Database)
    - PyQT/tkinter (UI)
    - 

**Interface Design (User Experience):**

- View
    - Basic table UI for display of information.
    - Search bar
    - Update and Delete buttons
    - Filter Options
- Add
    - Pop-up table
    - Table fields for information
        - Drop down menu for fields with past input:
            - Category/Subcategory
            - Account
            - Transaction type
    - Add Button
    - Confirmation message
- Update
    - Similar to Add UI but with update button instead of add
- Delete/Remove
    - Show user the information that’s going to be delete and ask for confirmation
    - Popup window for user input, user must account name and business name for deletion:
        - my_bank/247_shop
    - Confirmation or Error Message after deletion

---

### **3. Development Plan**

**Environment Control:**

- Virtual Environment to prevent conflict between libraries and modules

**Version Control:**

- GitHub Repository to keep track of changes
- Github Actions for automating testing and formatting on every repository push:
    - pytest for unit testing and integration testing
    - ruff for linting and formatting

**Task List :**

- **To Do (MVP):**
    - Design database schema:
        - account table schema
        - transaction table schema
    - Add Entity to database
    - Remove Entity from database
    - Update database
    - Display information to user
        - Filter by date, name, type

---

### **4. Execution and Testing**

**Development Process:**

- Testing:
    - Unit Testing
        - Data validation:
            - Correctly identify data depending on the field
            - Identify missing data before attempting to store data
        - Transaction Logic
            - Calculations add/removing/updating balance after a transaction must be tested.
        - Mocking user experience and interaction with database
            - Mock add
            - Mock remove
            - Mock update
    - Integration Testing:
        - Test that CRUD operations interact with each other as expected.
