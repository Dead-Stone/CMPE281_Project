import streamlit as st
import requests

# Set the base URL for the backend API
BASE_URL = "http://localhost:5000/api"

# Title for the app
st.title("Security Service Alert Management System")

# Navigation Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose a page", [
    "Dashboard",
    "Create Alert",
    "View All Alerts",
    "Search by Robot ID",
    "Update Robot Status Alert",
    "Delete Alert"
])

# Dashboard Overview
if page == "Dashboard":
    st.header("Dashboard Overview")

    try:
        # Fetch all alerts
        response = requests.get(f"{BASE_URL}/alerts")
        if response.status_code == 200:
            alerts = response.json()

            # Calculate metrics
            total_alerts = len(alerts)
            critical_alerts = sum(1 for alert in alerts if alert.get("severity") == "critical")
            resolved_alerts = sum(1 for alert in alerts if alert.get("status") == "resolved")

            st.metric("Total Alerts", total_alerts)
            st.metric("Critical Alerts", critical_alerts)
            st.metric("Resolved Alerts", resolved_alerts)

            # Example chart: Count alerts by severity
            severity_count = {
                "low": sum(1 for alert in alerts if alert.get("severity") == "low"),
                "medium": sum(1 for alert in alerts if alert.get("severity") == "medium"),
                "high": sum(1 for alert in alerts if alert.get("severity") == "high"),
                "critical": critical_alerts
            }
            st.bar_chart(list(severity_count.values()))
        else:
            st.error("Failed to fetch alerts for the dashboard.")
    except Exception as e:
        st.error(f"Error: {str(e)}")

# Create Alert
if page == "Create Alert":
    st.header("Create a New Alert")
    robot_id = st.number_input("Robot ID", min_value=1, step=1)
    alert_type = st.text_input("Alert Type")
    severity = st.selectbox("Severity", ["low", "medium", "high", "critical"])
    description = st.text_area("Description")
    # timestamp = st.text_input("Timestamp (YYYY-MM-DDTHH:MM:SS)")

    if st.button("Create Alert"):
        payload = {
            "robot_id": robot_id,
            "alert_type": alert_type,
            "severity": severity,
            "description": description
        }
        try:
            response = requests.post(f"{BASE_URL}/alerts/create", json=payload)
            if response.status_code == 201:
                st.success("Alert created successfully!")
            else:
                st.error(f"Error: {response.json().get('error', 'Failed to create alert')}")
        except Exception as e:
            st.error(f"Error: {str(e)}")

# View All Alerts
if page == "View All Alerts":
    st.header("All Alerts")
    try:
        response = requests.get(f"{BASE_URL}/alerts")
        if response.status_code == 200:
            alerts = response.json()
            if alerts:
                st.table(alerts)
            else:
                st.info("No alerts found.")
        else:
            st.error("Failed to fetch alerts.")
    except Exception as e:
        st.error(f"Error: {str(e)}")

# Search Alerts by Robot ID
if page == "Search by Robot ID":
    st.header("Search Alerts by Robot ID")
    robot_id = st.number_input("Enter Robot ID", min_value=1, step=1)
    if st.button("Search Alerts"):
        try:
            response = requests.get(f"{BASE_URL}/alerts/{robot_id}")
            # print("response", response.json())

            if response.status_code == 200:
                alerts = response.json().get("alerts", [])
                if alerts:
                    st.table(alerts)
                else:
                    st.info(f"No alerts found for Robot ID {robot_id}.")
            else:
                st.error("Failed to fetch alerts.")
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Update Alert
if page == "Update Robot Status Alert":
    st.header("Update Robot Status Alert")
    alert_id = st.number_input("Alert ID", min_value=1, step=1)
    status = st.selectbox("Status", ["pending", "resolved", "dismissed"])
    if st.button("Update Robot Status Alert"):
        payload = {"status": status}
        try:
            response = requests.put(f"{BASE_URL}/alerts/update_robot_status/{alert_id}", json=payload)
            if response.status_code == 200:
                st.success("Alert updated successfully!")
            else:
                st.error(f"Error: {response.json().get('error', 'Failed to update alert')}")
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Delete Alert
if page == "Delete Alert":
    st.header("Delete Alert")
    alert_id = st.number_input("Alert ID", min_value=1, step=1)
    if st.button("Delete Alert"):
        try:
            response = requests.delete(f"{BASE_URL}/alerts/delete/{alert_id}")
            if response.status_code == 200:
                st.success("Alert deleted successfully!")
            else:
                st.error(f"Error: {response.json().get('error', 'Failed to delete alert')}")
        except Exception as e:
            st.error(f"Error: {str(e)}")
