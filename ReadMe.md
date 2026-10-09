OSINT Investigation Suite
A GUI application built with Python and customtkinter to perform basic Open Source Intelligence (OSINT) searches.

Features
GUI Interface: Built with CustomTkinter featuring dark mode styling.

Splash Screen: Displays an initial splash screen before opening the main interface.

Sherlock Integration: Executes background searches for target usernames via the sherlock tool (targeting platforms like GitHub and Twitter).

Asynchronous Execution: Runs investigation tasks in background threads to keep the user interface responsive.

Prerequisites
Python 3.8+ installed on your system.

Sherlock installed and available in your system's PATH.

Installation;
Clone or Download the Repository:


git clone <repository-url>
cd <repository-directory>
Install Required Python Dependencies:


pip install -r requirements.txt

Usage:
Run the application:
python main.py

Enter the target Username in the input field.

Click Start Investigation to launch the OSINT queries.

View real-time results in the built-in console output box.