# Steps for Project Part 1 Using PyCharm

## Step 1: Create a Virtual Enviornment
* Open built in terminal in PyCharm
* cd .venv/Scripts
* ./activate

## Step 2: Install Libraries from requirements.txt
* Change the directory to CS670
    * cd ../..
* pip install -r requirements.txt

## Step 3: Change directory to Part1
* cd CS670/Part1

## Step 4: Run app.py
* python app.py
* File containing Game Set Up will open automatically and be saved under 'Layout' directory

# How the game works!

## Step 1: An xlsx file will be saved automatically under the 'Layout' folder
* If the directory does not exist, a new directory will be created called 'Layout'
* The xlsx file contains the information regarding the Game Setup
    * Solution will be shown under 'Solution Selection' sheet
    * All other setups will be shown under their respective sheets

## Step 2: You will have an option to select a starting character
* From the list provided type in your choice
    * Your input MUST match the options shown in the list
    * If you enter a character not in the list, you can retry your input
* You'll have a confirmation of the character selected and your Starting Room in the mansion

## Step 3: Now you'll have an option to either Make a Suggestion or Move between rooms
* Input 1 for Suggestion or 2 if you want to enter a new room
    * Your input MUST match one of these numbers
    * If you enter a number that is not 1 or 2, you can retry your input

## Making A Suggestion?
* Input a character from the list provided
    * MUST be a character within the list
    * If you enter a character not in the list, you can retry again
* Input a weapon from the list provided
    * MUST be a weapon within the list
    * If you enter a weapon not in the list, you can retry again
* Input a room from the list provided
    * MUST be a room within the list
    * If you enter a room not in the list, you can retry again

* If you guessed wrong, you'll have an option to move to a new room or retry your suggestion
    * If you retry your suggestion, following the second attempt and onwards you'll receive a hint

## Moving To A New Room?
* You MUST input a room from the choices represented in the list
    * If you input a room not in the list, you can retry again
    