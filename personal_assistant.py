import ollama
import subprocess
import pyautogui
import speech_recognition as sr
import platform
import json
import os
import sys
import time
import shutil

# Configuration
MODEL_NAME = "llama3"  # Ensure you have run 'ollama pull llama3'

class LocalAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.os_name = platform.system()
        print(f"Initializing Local Assistant on {self.os_name}...")
        
        # Check connection before starting
        self.check_ollama_connection()

        # PyAutoGUI fail-safe: Drag mouse to top-left corner to abort script
        pyautogui.FAILSAFE = True 

    def check_ollama_connection(self):
        """Verifies that the Ollama server is running with retries."""
        print("Checking connection to Ollama (Local Brain)...")
        
        # 1. Attempt to find the Ollama executable
        ollama_path = shutil.which("ollama")
        
        # If not in global PATH, check default Windows install location
        if ollama_path is None and self.os_name == "Windows":
            local_app_data = os.environ.get('LOCALAPPDATA', '')
            possible_path = os.path.join(local_app_data, "Programs", "Ollama", "ollama.exe")
            if os.path.exists(possible_path):
                ollama_path = possible_path

        if ollama_path is None:
            print("\n❌ CRITICAL ERROR: Ollama executable not found.")
            print("-----------------------------------------------------")
            print("It looks like Ollama is not installed.")
            print("1. Download it here: https://ollama.com/download")
            print("2. Install it.")
            print("3. Restart this terminal.")
            print("-----------------------------------------------------")
            sys.exit(1)

        # 2. Check if the server is running
        max_retries = 3
        for i in range(max_retries):
            try:
                ollama.list()
                print("✅ Connected to Ollama successfully.")
                return
            except Exception:
                print(f"   Attempt {i+1}/{max_retries} failed...")
                time.sleep(1)

        # If we reach here, connection failed multiple times
        print("\n❌ CRITICAL ERROR: Local AI Service (Ollama) not found.")
        print("-----------------------------------------------------")
        print("The 'Brain' is not running. To fix this:")
        print("1. Open a NEW terminal window.")
        
        if "AppData" in ollama_path:
            # Provide the specific path command if it's not in global PATH
            print(f"2. Run this EXACT command:\n   & \"{ollama_path}\" serve")
        else:
            print("2. Type command: ollama serve")
            
        print("3. Wait for it to say 'Listening' and keep that window OPEN.")
        print("-----------------------------------------------------")
        
        while True:
            choice = input("Press Enter to retry connection, or type 'exit' to quit: ")
            if choice.lower() == 'exit':
                sys.exit(1)
            
            try:
                ollama.list()
                print("✅ Connected! Starting assistant...")
                return
            except Exception as e:
                print(f"❌ Still failing. Detailed error: {e}")
                print("   (Make sure 'ollama serve' is running in another window)")

    def listen(self):
        """Listens to microphone input and converts to text."""
        with sr.Microphone() as source:
            print("\nListening... (Say 'exit' to stop)")
            self.recognizer.adjust_for_ambient_noise(source)
            try:
                # Reduced timeout to make it snappier
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=8)
                text = self.recognizer.recognize_google(audio).lower()
                print(f"You said: {text}")
                return text
            except sr.WaitTimeoutError:
                return None
            except sr.UnknownValueError:
                print("Could not understand audio.")
                return None
            except sr.RequestError:
                print("Could not request results. Check internet connection (for STT only).")
                return None

    def get_llm_decision(self, user_prompt):
        """
        Sends the user command to the local LLM and asks for a structured JSON response.
        """
        
        # IMPROVED SYSTEM PROMPT: More examples and stricter JSON enforcement
        system_prompt = """
        You are a desktop automation engine. You are NOT a chatbot.
        You strictly output a JSON array of objects. Do NOT output any markdown, explanations, or conversational text.
        
        Available Tools:
        1. open_app(app_name): Opens an app. Use standard executable names (e.g., "calc", "notepad", "explorer", "chrome", "spotify").
        2. type_text(text): Types text.
        3. press_key(key): Presses keys (e.g., "enter", "tab", "alt+f4", "ctrl+c", "win").

        Example 1: "Open calculator"
        Output: [{"tool": "open_app", "args": "calc"}]

        Example 2: "Type hello world then press enter"
        Output: [{"tool": "type_text", "args": "hello world"}, {"tool": "press_key", "args": "enter"}]
        """

        try:
            response = ollama.chat(model=MODEL_NAME, messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_prompt},
            ])
            
            content = response['message']['content']
            
            # Try to extract JSON if the model wrapped it in text
            start = content.find('[')
            end = content.rfind(']') + 1
            
            if start != -1 and end != -1:
                json_str = content[start:end]
                return json.loads(json_str)
            else:
                # Debugging: Print raw output if JSON parsing fails
                print(f"❌ LLM Output was not JSON. It said:\n{content}")
                return []
        except Exception as e:
            print(f"LLM Error: {e}")
            return []

    def execute_actions(self, actions):
        """Parses the JSON list and executes Python functions."""
        for action in actions:
            tool = action.get('tool')
            args = action.get('args')

            print(f"Executing: {tool} ('{args}')")
            
            if tool == "open_app":
                self.open_application(args)
                time.sleep(2) # Wait for app to open
            elif tool == "type_text":
                pyautogui.write(args, interval=0.05)
            elif tool == "press_key":
                if '+' in args:
                    keys = args.split('+')
                    pyautogui.hotkey(*keys)
                else:
                    pyautogui.press(args)
            elif tool == "unknown":
                print("I don't know how to do that physically yet.")

    def open_application(self, app_name):
        """OS-agnostic app opener with smart mapping."""
        # Common Name -> Executable Name mapping
        common_apps = {
            "calculator": "calc",
            "file explorer": "explorer",
            "explorer": "explorer",
            "notepad": "notepad",
            "paint": "mspaint",
            "settings": "ms-settings:",
            "chrome": "chrome",
            "google chrome": "chrome",
            "edge": "msedge",
            "spotify": "spotify",
            "cmd": "cmd",
            "terminal": "cmd"
        }
        
        # Check mapping, otherwise use the raw name provided by LLM
        target_app = common_apps.get(app_name.lower(), app_name)

        try:
            if self.os_name == "Windows":
                # 'start' command is robust for finding apps in PATH
                subprocess.Popen(f"start {target_app}", shell=True)
            elif self.os_name == "Darwin": # macOS
                subprocess.Popen(["open", "-a", target_app])
            elif self.os_name == "Linux":
                subprocess.Popen([target_app])
        except Exception as e:
            print(f"Failed to open {app_name} (target: {target_app}): {e}")

    def run(self):
        print("--- Local AI Automation Agent ---")
        print("1. Voice Mode")
        print("2. Text Mode")
        mode = input("Select mode (1/2): ")

        while True:
            user_input = ""
            
            if mode == "1":
                user_input = self.listen()
                if user_input is None: continue
            else:
                user_input = input("\nType command (or 'exit'): ")

            # Flexible exit condition
            if user_input and ('exit' in user_input.lower() or 'quit' in user_input.lower()):
                print("Exiting...")
                break
            
            # Step 1: Think (LLM Processing)
            print("Thinking...")
            actions = self.get_llm_decision(user_input)
            
            # Step 2: Act (Execution)
            if actions:
                self.execute_actions(actions)
            else:
                print("No actionable commands found.")

if __name__ == "__main__":
    agent = LocalAssistant()
    agent.run()