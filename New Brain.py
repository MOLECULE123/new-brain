import sys
import time

def print_aesthetic_morning():
    # Clear the terminal screen for a clean look
    sys.stdout.write("\033[H\033[2J")
    sys.stdout.flush()
    
    # ANSI escape colors (using 256-color palette for smooth gradients)
    # 208: Orange, 214: Warm Yellow, 117: Soft Sky Blue, 45: Bright Cyan, 15: Pure White
    orange = "\033[38;5;208m"
    yellow = "\033[38;5;214m"
    sky_blue = "\033[38;5;117m"
    cyan = "\033[38;5;45m"
    white = "\033[38;5;15m"
    bold = "\033[1m"
    reset = "\033[0m"

    # Decorative elements
    border = f"{sky_blue}✧･ﾟ: * {cyan}✧･ﾟ:* ---------------------------- *:･ﾟ✧*:･ﾟ✧{reset}"
    
    # The Text Art / Message
    print("\n" * 2)
    print(border.center(80))
    print("\n")
    
    # Multi-colored "GOOD MORNING" using soft, warm-to-cool tones
    sys.stdout.write(" " * 20) # Center alignment padding
    for char, color in zip("GOOD MORNING", [orange, orange, yellow, yellow, yellow, white, sky_blue, sky_blue, cyan, cyan, cyan, cyan]):
        sys.stdout.write(f"{bold}{color}{char}{reset}")
        sys.stdout.flush()
        time.sleep(0.05) # Subtle fade-in typing effect
        
    print("\n\n")
    print(f"{white}May your day be as bright and productive as your code.{reset}".center(80))
    print("\n")
    print(border.center(80))
    print("\n" * 2)

if __name__ == "__main__":
    print_aesthetic_morning()
