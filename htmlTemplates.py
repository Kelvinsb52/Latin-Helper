css = '''
<style>
    body {
        background-color: #F8F9FA;  /* Light background */
    }
    .stApp {
        background-color: #F8F9FA;
        font-family: 'Arial', sans-serif;
    }
    .sidebar .sidebar-content {
        background-color: #343A40;
        color: white;
    }
    .stButton button {
        border-radius: 10px;
        background-color: #4CAF50;
        color: white;
        font-size: 16px;
        padding: 8px 16px;
        border: none;
    }
    .stTextInput input {
        border-radius: 10px;
        border: 1px solid #000;  /* Black border for visibility */
        padding: 10px;
        background-color: white;  /* Ensures it does not blend in */
        color: black;  /* Text is clearly visible */
        font-size: 16px;
        caret-color: black !important;  /* Change cursor color to black */

    }
    .stTextInput {
        display: block !important;
        margin-bottom: 15px; 
    }
    .stHeader {
        display: block !important;
        font-size: 30px;  /* Bigger text */
        font-weight: bold;
        color: #000000 !important;  /* Force black text */
        background-color: #DDE1E6;  /* Light gray for contrast */
        padding: 15px;
        border-radius: 10px;
        text-align: center;
    }
    .chat-container {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
        margin-bottom: 15px;
    }
    .chat-message {
        padding: 1.5rem; 
        border-radius: 0.5rem; 
        margin-bottom: 1rem; 
        display: flex;
    }
    .chat-message.user {
        background-color: #2b313e;
    }
    .chat-message.bot {
        background-color: #475063;
    }
    .chat-message .avatar {
        width: 20%;
    }
    .chat-message .avatar img {
        max-width: 78px;
        max-height: 78px;
        border-radius: 50%;
        object-fit: cover;
    }
    .chat-message .message {
        width: 80%;
        padding: 0 1.5rem;
        color: #fff;
    }
</style>
'''



bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://www.pantheonpoets.com/wp-content/uploads/2020/06/virgil-min.jpg" 
             style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://cdn.topofart.com/images/artists/Willem_Drost/paintings-wm/drost002.jpg">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''
