# WalkQuest

A Kivy-based Android application.

Setup Instructions
----------------

1. Install Python 3 on macOS:
   brew install python3

2. Install project dependencies:
   pip3 install -r requirements.txt

3. For Android development, install additional dependencies:
   brew install pkg-config sdl2 sdl2_image sdl2_ttf sdl2_mixer gstreamer
   brew install wget
   brew install ant
   brew install openjdk

Development
----------

Running the App Locally:
- To test the app on desktop:
  python3 main.py

Building for Android:
1. Initialize buildozer (only needed once):
   buildozer init

2. Build and deploy to Android:
   buildozer android debug deploy run

Project Structure
---------------
- main.py - Main application file
- buildozer.spec - Android build configuration
- requirements.txt - Python dependencies

Current Features
--------------
- Simple UI with a customized button
- White background with light blue button
- Responsive layout with padding

Next Steps
---------
The app is ready for additional features such as:
- Multiple screens
- Navigation
- User input
- Data storage
- Custom themes
- Animations