#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Facebook CLI Tool for Termux
Simple Facebook login and browsing tool
"""

import requests
import json
import os
import sys
from datetime import datetime

class FacebookCLI:
    def __init__(self):
        self.session = requests.Session()
        self.user_agent = "Mozilla/5.0 (Linux; Android 10; Pixel 4) AppleWebKit/537.36"
        self.session.headers.update({'User-Agent': self.user_agent})
        self.cookies_file = os.path.expanduser("~/.fb_cookies.json")
        self.logged_in = False
        self.user_info = {}
        
    def save_cookies(self):
        """Save cookies to file"""
        try:
            with open(self.cookies_file, 'w') as f:
                json.dump(requests.utils.dict_from_cookiejar(self.session.cookies), f)
        except Exception as e:
            print(f"Error saving cookies: {e}")
    
    def load_cookies(self):
        """Load saved cookies from file"""
        if os.path.exists(self.cookies_file):
            try:
                with open(self.cookies_file, 'r') as f:
                    cookies = json.load(f)
                    self.session.cookies.update(cookies)
                    return True
            except Exception as e:
                print(f"Error loading cookies: {e}")
        return False
    
    def login(self, email, password):
        """Login to Facebook"""
        print("[*] Attempting login...")
        
        try:
            # Load Facebook homepage
            response = self.session.get('https://www.facebook.com/')
            
            # Prepare login data
            login_data = {
                'email': email,
                'pass': password,
                'login': 'Log In'
            }
            
            # Send login request
            response = self.session.post(
                'https://www.facebook.com/login.php',
                data=login_data,
                allow_redirects=True,
                timeout=10
            )
            
            # Check if login was successful
            if 'logout' in response.text.lower() or 'home' in response.text.lower():
                self.logged_in = True
                self.save_cookies()
                print("[+] Login successful!")
                return True
            else:
                print("[-] Login failed. Please check email/password.")
                return False
                
        except requests.exceptions.Timeout:
            print("[-] Connection timeout. Check your internet.")
            return False
        except Exception as e:
            print(f"[-] Error: {str(e)}")
            return False
    
    def get_feed(self):
        """Get and display news feed"""
        if not self.logged_in:
            print("[-] Please login first")
            return
        
        try:
            print("[*] Loading news feed...\n")
            response = self.session.get('https://www.facebook.com/')
            
            if response.status_code == 200:
                print("[+] Feed loaded (limited view)")
                print("-" * 50)
                print("[*] Visit Facebook.com for full feed access")
            else:
                print("[-] Could not load feed")
                
        except Exception as e:
            print(f"[-] Error: {str(e)}")
    
    def get_profile(self):
        """Get and display profile information"""
        if not self.logged_in:
            print("[-] Please login first")
            return
        
        try:
            print("[*] Loading profile...\n")
            response = self.session.get('https://www.facebook.com/')
            
            if response.status_code == 200:
                print("[+] Profile accessible")
                print("-" * 50)
                print("[*] Visit facebook.com/profile for full profile")
            else:
                print("[-] Could not load profile")
                
        except Exception as e:
            print(f"[-] Error: {str(e)}")
    
    def logout(self):
        """Logout from Facebook"""
        try:
            self.session.get('https://www.facebook.com/logout.php')
            self.logged_in = False
            if os.path.exists(self.cookies_file):
                os.remove(self.cookies_file)
            print("[+] Logout successful!")
        except Exception as e:
            print(f"[-] Error: {str(e)}")

def print_menu():
    """Display main menu"""
    print("\n" + "="*50)
    print("Facebook CLI - Termux Edition")
    print("="*50)
    print("1. Login")
    print("2. View News Feed")
    print("3. View Profile")
    print("4. Logout")
    print("5. Exit")
    print("="*50)

def main():
    fb = FacebookCLI()
    
    # Check for previous session
    if fb.load_cookies():
        fb.logged_in = True
        print("[+] Previous session found")
    
    while True:
        print_menu()
        choice = input("Select option (1-5): ").strip()
        
        if choice == '1':
            email = input("Email/Phone: ")
            password = input("Password: ")
            fb.login(email, password)
            
        elif choice == '2':
            fb.get_feed()
            
        elif choice == '3':
            fb.get_profile()
            
        elif choice == '4':
            fb.logout()
            
        elif choice == '5':
            print("[*] Goodbye!")
            sys.exit(0)
            
        else:
            print("[-] Invalid option")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[*] Program interrupted")
        sys.exit(0)
