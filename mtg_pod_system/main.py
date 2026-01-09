#!/usr/bin/env python3
"""
MTG Pod Randomizer - Main Entry Point

A cross-platform system for randomly assigning Magic: The Gathering players to pods.
Works on desktop, mobile (via terminal apps), and web browsers.

Author: MTG Pod System
Version: 1.0.0
"""

import sys
import os

# Add the project root to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from interfaces.terminal_app import main as terminal_main

def main():
    """Main entry point with interface selection"""
    print("MTG Pod Randomizer v1.0.0")
    print("=" * 50)
    
    # Check available interfaces
    interfaces = []
    
    # Terminal interface (always available)
    interfaces.append(("terminal", "Terminal Interface", terminal_main))
    
    # Check for web interface capabilities
    try:
        import http.server
        import socketserver
        import webbrowser
        interfaces.append(("web", "Web Interface (Browser)", None))
    except ImportError:
        pass
    
    print("Available Interfaces:")
    for i, (key, name, _) in enumerate(interfaces, 1):
        print(f"  {i}. {name}")
    
    # Auto-select terminal if only one option
    if len(interfaces) == 1:
        print(f"\nLaunching {interfaces[0][1]}...")
        interfaces[0][2]()
        return
    
    # Let user choose
    try:
        choice = input(f"\nSelect interface (1-{len(interfaces)}) [1]: ").strip()
        if not choice:
            choice = "1"
        
        choice = int(choice)
        if 1 <= choice <= len(interfaces):
            selected = interfaces[choice - 1]
            print(f"\nLaunching {selected[1]}...")
            
            if selected[2]:
                # Terminal interface
                selected[2]()
            else:
                # Web interface
                launch_web_interface()
        else:
            print("Invalid choice. Launching terminal interface...")
            terminal_main()
            
    except (ValueError, KeyboardInterrupt):
        print("\nLaunching terminal interface...")
        terminal_main()

def launch_web_interface():
    """Launch the web interface"""
    import http.server
    import socketserver
    import webbrowser
    import threading
    import time
    
    # Change to the web directory
    web_dir = os.path.join(project_root, 'mobile_web')
    os.chdir(web_dir)
    
    # Find an available port
    port = 8000
    while port < 9000:
        try:
            with socketserver.TCPServer(("", port), http.server.SimpleHTTPRequestHandler) as httpd:
                print(f"Web interface starting on http://localhost:{port}")
                print("Press Ctrl+C to stop the server")
                
                # Open browser in a separate thread
                def open_browser():
                    time.sleep(1)  # Wait for server to start
                    webbrowser.open(f"http://localhost:{port}")
                
                browser_thread = threading.Thread(target=open_browser)
                browser_thread.daemon = True
                browser_thread.start()
                
                # Run the server
                httpd.serve_forever()
                break
        except OSError:
            port += 1
    else:
        print("Could not find an available port for web interface")
        print("Falling back to terminal interface...")
        terminal_main()

if __name__ == "__main__":
    main()