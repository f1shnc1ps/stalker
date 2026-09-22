from colorama import Fore, Style, init

init(autoreset=True)

def print_header(text: str):
    """Print formatted header"""
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"{text.center(70)}")
    print(f"{'='*70}{Style.RESET_ALL}\n")

def print_success(text: str):
    """Print success message"""
    print(f"{Fore.GREEN}[+]{Style.RESET_ALL} {text}")

def print_info(text: str):
    """Print info message"""
    print(f"{Fore.BLUE}[*]{Style.RESET_ALL} {text}")

def print_error(text: str):
    """Print error message"""
    print(f"{Fore.RED}[-]{Style.RESET_ALL} {text}")

def print_warning(text: str):
    """Print warning message"""
    print(f"{Fore.YELLOW}[!]{Style.RESET_ALL} {text}")
