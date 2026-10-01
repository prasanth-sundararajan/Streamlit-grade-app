# Import Streamlit and give it the short name used in this file.
import streamlit as st


# Set the browser tab title and center the app's content.
st.set_page_config(page_title="Student Grade Manager", layout="centered")


# Convert one valid numeric mark into its letter grade.
def get_grade(mark):
    # Check the highest band first so every mark of 90 or more receives A.
    if mark >= 90:
        return "A"
    # Marks below 90 but at least 80 receive B.
    if mark >= 80:
        return "B"
    # Marks below 80 but at least 70 receive C.
    if mark >= 70:
        return "C"
    # Marks below 70 but at least 60 receive D.
    if mark >= 60:
        return "D"
    # Every remaining valid mark is below 60 and receives E.
    return "E"


# Create the list only on the first run; later reruns keep the existing list.
if "students" not in st.session_state:
    # Store student records in session state instead of a temporary local list.
    st.session_state.students = []

# Add the main heading at the top of the page.
st.title("Student Grade Manager")
# Explain the purpose of the page in a short line under the heading.
st.caption("Add student marks and see the class results update instantly.")

# Group the inputs so Streamlit submits them together when the button is pressed.
with st.form("add_student", clear_on_submit=True):
    # Label the student-entry section.
    st.subheader("Add a student")
    # Ask for the student's name and keep the entered text in this run.
    name = st.text_input("Student name")
    # Ask for a mark and configure its numeric bounds and display precision.
    mark = st.number_input(
        "Mark",  # Show this label beside the numeric control.
        min_value=0.0,  # Prevent marks below the allowed minimum.
        max_value=100.0,  # Prevent marks above the allowed maximum.
        value=0.0,  # Start each new form with a valid mark.
        step=0.1,  # Let users adjust the mark in tenths.
        format="%.1f",  # Display the entered mark with one decimal place.
    )  # Finish configuring the mark input.
    # Submit the name and mark together and highlight the form action.
    submitted = st.form_submit_button("Add student", type="primary")

# Process a record only on the run triggered by a form submission.
if submitted:
    # Trim whitespace so a name containing only spaces counts as blank.
    clean_name = name.strip()
    # Reject an empty name and explain how to fix it.
    if not clean_name:
        st.error("Enter a student name before adding the result.")
    # Save the valid record and show confirmation when a name was supplied.
    else:
        # Append a dictionary so the table can use its keys as column names.
        st.session_state.students.append(
            {"Name": clean_name, "Mark": mark, "Grade": get_grade(mark)}
        )
        # Confirm which student was added to the session.
        st.success(f"Added {clean_name}.")

# Separate data entry from the class summary visually.
st.divider()
# Introduce the results table and class figures.
st.subheader("Class results")

# Read the persistent records from session state for this script run.
students = st.session_state.students
# Calculate figures and draw the table only when at least one record exists.
if students:
    # Extract numeric marks once so the summary calculations stay concise.
    marks = [student["Mark"] for student in students]
    # Create three side-by-side spaces for the class metrics.
    average, highest, lowest = st.columns(3)
    # Show the arithmetic mean to one decimal place.
    average.metric("Class average", f"{sum(marks) / len(marks):.1f}")
    # Show the largest mark to one decimal place.
    highest.metric("Highest mark", f"{max(marks):.1f}")
    # Show the smallest mark to one decimal place.
    lowest.metric("Lowest mark", f"{min(marks):.1f}")
    # Format marks compactly for display without changing stored numeric values.
    display_students = [
        {**student, "Mark": f"{student['Mark']:g}"} for student in students
    ]
    # Render each student's name, mark, and grade as a table.
    st.table(display_students)
# Show placeholder metrics and a message before the first student is added.
else:
    # Keep the empty-state metrics in the same three-column layout.
    average, highest, lowest = st.columns(3)
    # Show a dash because no class average exists yet.
    average.metric("Class average", "-")
    # Show a dash because no highest mark exists yet.
    highest.metric("Highest mark", "-")
    # Show a dash because no lowest mark exists yet.
    lowest.metric("Lowest mark", "-")
    # Tell the user why the table and class figures are currently empty.
    st.info("No students added yet.")