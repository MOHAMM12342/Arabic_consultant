import requests
import arabic_reshaper
from bidi.algorithm import get_display
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def ask_chatbot(query: str):
    url = "http://localhost:8081/api/chat"
    payload = {"query": query}
    
    print("Sending query to Spring Boot backend...")
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        # Extract the arabic response
        arabic_text = response.json().get("response", "")
        
        # 1. Reshape the arabic letters so they connect properly
        reshaped_text = arabic_reshaper.reshape(arabic_text)
        
        # 2. Reverse the text for left-to-right terminals
        bidi_text = get_display(reshaped_text)
        
        print("\n--- Chatbot Response ---")
        print(bidi_text)
        print("------------------------\n")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Test query in Darija
    user_query = "شكون عندو الحق في النفقة؟"    
    # Optional: Display the query correctly formatted in terminal
    print("User Query:", get_display(arabic_reshaper.reshape(user_query)))
    
    ask_chatbot(user_query)
