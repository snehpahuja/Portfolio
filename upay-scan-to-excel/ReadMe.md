# **UPAY Scan-to-Excel Analytics Dashboard**

This project is a web application prototype for the NGO, UPAY. It is designed to streamline the process of digitizing physical documents (like student records, attendance sheets, and receipts) and visualizing the extracted data in an interactive analytics dashboard.

The application consists of two main parts:

1. A static HTML/CSS front-end for user login, file uploads, and data review.  
2. An interactive Streamlit dashboard for data analysis and visualization, which is embedded directly into the main web interface.

## **Project Structure**

The project is organized into the following directories and files:

upay-analytics-project/  
│  
├── .streamlit/  
│   └── config.toml       \# Streamlit theme configuration to match the website's style.  
│  
├── data/  
│   └── (\*.csv)           \# Contains the pre-generated mock data files used by the Streamlit app.  
│  
├── templates/  
│   └── (\*.html)          \# All static HTML pages for the user interface.  
│  
├── upay\_app/  
│   ├── \_\_init\_\_.py  
│   └── centre\_analysis.py  \# The main Python script for the Streamlit dashboard.  
│  
└── README.md             \# This file.

## **How to Run the Application**

Follow these steps to set up and run the project on your local machine.

### **Step 1: Install Dependencies if not already installed**

First, you need to install the required Python libraries. Open your terminal in the upay-scan-to-excel root directory and run the following command if the directories are not already present:

**pip install streamlit pandas numpy plotly**

### **Step 2: Run the Streamlit Dashboard**

### Make sure you are in the upay-scan-to-excel root directory.

**streamlit run upay\_app/centre\_analysis.py**

The terminal will provide a local URL. The dashboard is now running.

### **Step 3: Open the Web Application**

To see the complete application with the dashboard embedded:

1. Navigate to the templates/ folder in your file explorer.  
2. Open the index.html file in your web browser.

This will display the main interface with the live, interactive Streamlit dashboard.

