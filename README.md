# ONLINE-MUSEUM-TICKET-BOOKING-SYSTEM
This project is a comprehensive Online Museum Ticket Booking System designed to streamline and enhance the ticket booking process for the Gedee Car Museum. The system includes a user-friendly chatbot interface integrated with a robust backend to manage bookings, payments, and customer interactions seamlessly.

Follow these steps to set up Rasa for the Gedee Car Museum Ticket Booking System:

Prerequisites
Python 3.7 or later installed on your system.
pip (Python package manager).
A virtual environment tool like venv or virtualenv.

Installation Steps

1. Clone the Repository

git clone https://github.com/yourusername/your-repository-name.git  
cd your-repository-name

3. Create a Virtual Environment

python -m venv rasa_env  
source rasa_env/bin/activate   # For Linux/Mac  
rasa_env\Scripts\activate      # For Windows
  
4. Install Rasa
Install the Rasa framework using pip:

pip install rasa  

4. Install Dependencies
   
Install the additional dependencies required for the chatbot:

pip install -r requirements.txt 

Setting Up the Rasa Project

1. Initialize Rasa
If starting a new Rasa project:

rasa init --no-prompt 

For existing projects, ensure you have the necessary domain.yml, nlu.yml, stories.yml, and config.yml files in the my_project/rasa folder.

3. Train the Chatbot
Train the Rasa model with the provided data:

rasa train  

3. Run the Rasa Actions Server
   
If you have custom actions in actions.py, start the action server:

rasa run actions  

4. Start the Rasa Chatbot
Run the chatbot locally:

rasa shell  

Running the Rasa Chatbot with Django

Start the Django server:

python manage.py runserver  

Start the Rasa server:

rasa run --enable-api --cors "*"  
Test the chatbot via the Django interface or API endpoint.

Testing the Chatbot
Use the Rasa shell for testing locally:

rasa shell  

Test integrations by interacting with the chatbot interface in your browser.
Troubleshooting

If you encounter version conflicts, update dependencies with:

pip install --upgrade pip setuptools  

Ensure your Rasa action server is running for custom actions.

Check logs for errors using the --debug flag:

rasa run --debug  

This setup should get your Rasa chatbot running smoothly for the Gedee Car Museum Ticket Booking System.
