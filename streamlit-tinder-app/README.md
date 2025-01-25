# Streamlit Tinder App

This project is a simple web application built using Streamlit that mimics the swiping functionality of Tinder for matching users based on their preferences.

## Project Structure

```
streamlit-tinder-app
├── src
│   ├── app.py          # Main entry point of the Streamlit application
│   └── utils
│       └── matching.py # Utility functions for matching users
├── requirements.txt    # List of dependencies
└── README.md           # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd streamlit-tinder-app
   ```

2. **Install the required dependencies:**
   ```
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```
   streamlit run src/app.py
   ```

## Usage

- Upon running the application, users can enter their name and preferences.
- Users can swipe left or right to indicate their interest in other users.
- Matches will be displayed based on mutual interest.

## Contributing

Feel free to submit issues or pull requests for improvements or bug fixes.