# Steps for Project Part 2 Using PyCharm

## Step 1: Create a Virtual Enviornment
* Open built in terminal in PyCharm
* cd .venv/Scripts
* ./activate

## Step 2: Install Libraries from requirements.txt
* Change the directory to CS670
    * cd ../..
* pip install -r requirements.txt

## Step 3: Change directory to Part2
* cd CS670/Part2

## Step 4: Run app.py
* python app.py
* File containing Game Set Up will open automatically and be saved under 'Layout' directory

# How the game works!

## Step 1: Home Page
* Let's Play! (Button)
    * Starts the Clue Game (Continue to Step 2)

* Download Game Layout (Button)
    * An xlsx file will be saved automatically under the 'Layout' folder
    * If the directory does not exist, a new directory will be created called 'Layout'
    * The xlsx file contains the information regarding the Game Setup
        * Solution will be shown under 'Solution Selection' sheet
        * All other setups will be shown under their respective sheets

![Home Page](step_images/Step_1.png)

## Step 2: Character Selection
* You have the option to select a character from the form. 
    * The character chosen, will be saved throughout the rest of the game.
    * NOTE: You MUST select a character to continue to Step 3.
  
![Character Selection](step_images/Step_2.png)

* Character Selection Confirmation 

![Character Selection Confirm](step_images/Step_2B.png)

## Step 3: Room Selection
* You will now have to select a room inside the mansion.
    * You can always navigate to different rooms (Follow Step 4)
* NOTE: You MUST select a room to continue to Step 4

![Room Selection](step_images/Step_3.png)

## Step 4: 