#32-bit RISC-V Binary/Hex to Assembly Language Translator

A simple translator for converting 32-bit RISC-V machine code (binary or hex) into assembly language instructions.

This version includes MongoDB integration to store and retrieve translations for efficiency. It runs as an interactive CLI.

🔹 Setup & Installation

1. Clone the Repository
'''
git clone https://github.com/aaf091/Bin2ASM-RV.git
cd Bin2ASM-RV
'''

2. Install Required Dependencies

Ensure you have Python installed, then run:
'''
pip install -r requirements.txt
'''
(Make sure pymongo and python-dotenv are installed for MongoDB integration.)

3. Setup MongoDB Connection
	•	If using MongoDB Atlas, set up your connection string.
	•	Store it securely in an environment variable:

'''
export MONGODB_URI="your_mongodb_connection_string"
'''
or in a .env file (for local development):
'''
MONGODB_URI=mongodb+srv://your_user:your_password@cluster.mongodb.net/riscv_translator
'''
🔹 Running the Translator

Start the CLI by running:
'''
python convert.py
'''
