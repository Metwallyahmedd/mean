import tkinter as tk
from tkinter import messagebox
from geopy.geocoders import Nominatim
import folium
import webbrowser

# Create the main application window
root = tk.Tk()
root.title("Geo-Enabled To-Do List App")
root.geometry("400x400")

# Initialize the geolocator
geolocator = Nominatim(user_agent="GeoTodoApp")

# List to store tasks, each task will have a description, location, and coordinates
tasks = []

# Function to update the task list display
def update_task_list():
    task_listbox.delete(0, tk.END)
    for task in tasks:
        task_listbox.insert(tk.END, f"{task[0]} - {task[1]}")

# Function to add a task
def add_task():
    task_description = task_entry.get()
    location = location_entry.get()
    
    if task_description == "" or location == "":
        messagebox.showwarning("Input Error", "Please enter both task description and location.")
        return
    
    # Convert location to latitude and longitude
    try:
        location_obj = geolocator.geocode(location)
        if location_obj:
            task_coordinates = (location_obj.latitude, location_obj.longitude)
            tasks.append((task_description, location, task_coordinates))
            task_entry.delete(0, tk.END)
            location_entry.delete(0, tk.END)
            update_task_list()
        else:
            messagebox.showwarning("Location Error", "Could not find the location.")
    except Exception as e:
        messagebox.showwarning("Error", f"An error occurred: {e}")

# Function to delete a selected task
def delete_task():
    try:
        task_index = task_listbox.curselection()[0]
        tasks.pop(task_index)
        update_task_list()
    except IndexError:
        messagebox.showwarning("Selection Error", "Please select a task to delete.")

# Function to mark a selected task as completed
def mark_completed():
    try:
        task_index = task_listbox.curselection()[0]
        task = tasks[task_index]
        tasks[task_index] = (f"{task[0]} (Completed)", task[1], task[2])
        update_task_list()
    except IndexError:
        messagebox.showwarning("Selection Error", "Please select a task to mark as completed.")

# Function to view tasks on the map
def view_map():
    if not tasks:
        messagebox.showwarning("No Tasks", "There are no tasks to display on the map.")
        return
    
    # Create a map centered at the first task's location
    map_obj = folium.Map(location=[tasks[0][2][0], tasks[0][2][1]], zoom_start=12)
    
    # Add markers for each task's location
    for task in tasks:
        folium.Marker(location=[task[2][0], task[2][1]], popup=f"{task[0]} - {task[1]}").add_to(map_obj)
    
    # Save the map as an HTML file and open it in the default browser
    map_obj.save("tasks_map.html")
    webbrowser.open("tasks_map.html")

# Function to clear all tasks
def clear_all():
    response = messagebox.askyesno("Clear All", "Are you sure you want to clear all tasks?")
    if response:
        tasks.clear()
        update_task_list()

# Create an entry field for the task description
task_entry = tk.Entry(root, width=35)
task_entry.pack(pady=10)

# Create an entry field for the location
location_entry = tk.Entry(root, width=35)
location_entry.pack(pady=10)

# Create Add Task button
add_button = tk.Button(root, text="Add Task", width=20, command=add_task)
add_button.pack(pady=5)

# Create a Listbox to display the tasks
task_listbox = tk.Listbox(root, width=40, height=10)
task_listbox.pack(pady=10)

# Create a Mark Completed button
complete_button = tk.Button(root, text="Mark Completed", width=20, command=mark_completed)
complete_button.pack(pady=5)

# Create a Delete Task button
delete_button = tk.Button(root, text="Delete Task", width=20, command=delete_task)
delete_button.pack(pady=5)

# Create a View Map button
view_map_button = tk.Button(root, text="View Map", width=20, command=view_map)
view_map_button.pack(pady=5)

# Create a Clear All button
clear_button = tk.Button(root, text="Clear All", width=20, command=clear_all)
clear_button.pack(pady=5)

# Run the Tkinter event loop
root.mainloop()
