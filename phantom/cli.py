import click
from colorama import Fore, Style, init
from tabulate import tabulate
import json
import sys
from phantom.reconnaissance.username import UsernameRecon
from phantom.reconnaissance.email import EmailRecon
from phantom.reconnaissance.phone import PhoneRecon
from phantom.reconnaissance.ip import IPRecon
from phantom.utils.output import print_header, print_success, print_info, print_error

init(autoreset=True)

@click.group()
def cli():
    """PHANTOM - Unified OSINT Intelligence Gatherer
    
    Fast, parallel reconnaissance across 600+ platforms.
    Search usernames, emails, phones, and IP addresses.
    """
    pass

@cli.command()
@click.argument('username')
@click.option('--threads', default=10, help='Number of threads (default: 10)')
@click.option('--export', type=click.Path(), help='Export results to JSON')
@click.option('--verbose', is_flag=True, help='Verbose output')
def user(username: str, threads: int, export: str, verbose: bool):
    """Search username across 600+ platforms"""
    print_header(f"USERNAME RECONNAISSANCE: {username}")
    
    recon = UsernameRecon(username, threads=threads)
    print_info(f"Scanning platforms with {threads} threads...")
    
    results = recon.scan()
    found = sum(1 for r in results.values() if r.get('found'))
    
    for site, result in sorted(results.items()):
        if result.get('found'):
            print_success(f"{site}: {result.get('url', '')}")
        elif verbose and result.get('error'):
            print_error(f"{site}: {result['error']}")
    
    print_header(f"RESULTS: Found on {found}/{len(results)} platforms")
    
    if export:
        with open(export, 'w') as f:
            json.dump(results, f, indent=2)
        print_success(f"Exported to {export}")

@cli.command()
@click.argument('email')
@click.option('--export', type=click.Path(), help='Export results to JSON')
def email(email: str, export: str):
    """Check email in breaches and validate"""
    print_header(f"EMAIL RECONNAISSANCE: {email}")
    
    recon = EmailRecon()
    results = recon.scan(email)
    
    if not results['valid']:
        print_error("Invalid email format")
        return
    
    print_success("Email format valid")
    
    hibp = results.get('hibp', {})
    if hibp.get('found'):
        print_error(f"Found in {hibp['breach_count']} breaches:")
        for breach in hibp.get('breaches', []):
            print(f"  {Fore.RED}•{Style.RESET_ALL} {breach}")
    else:
        print_success("Not found in known breaches (HIBP)")
    
    emailrep = results.get('emailrep', {})
    if emailrep.get('found'):
        rep = emailrep.get('reputation', 'unknown')
        fraud = emailrep.get('fraud_level')
        print_info(f"EmailRep reputation: {rep}")
        if fraud:
            print_error(f"Fraud level: {fraud}")
    
    print_header("EMAIL CHECK COMPLETE")
    
    if export:
        with open(export, 'w') as f:
            json.dump(results, f, indent=2)
        print_success(f"Exported to {export}")

@cli.command()
@click.argument('phone')
@click.option('--export', type=click.Path(), help='Export results to JSON')
def phone(phone: str, export: str):
    """Validate phone and get lookup URLs"""
    print_header(f"PHONE RECONNAISSANCE: {phone}")
    
    recon = PhoneRecon()
    results = recon.scan(phone)
    
    if not results['valid']:
        print_error("Invalid phone format")
        return
    
    print_success(f"Valid phone ({results['region']}): {results['clean']}")
    print_info(f"Truecaller lookup: {results['truecaller']}")
    
    print_header("PHONE CHECK COMPLETE")
    
    if export:
        with open(export, 'w') as f:
            json.dump(results, f, indent=2)
        print_success(f"Exported to {export}")

@cli.command()
@click.argument('ip')
@click.option('--export', type=click.Path(), help='Export results to JSON')
@click.option('--shodan-key', envvar='SHODAN_API_KEY', help='Shodan API key')
def ipaddr(ip: str, export: str, shodan_key: str):
    """Full IP reconnaissance (geolocation, reputation, services)"""
    print_header(f"IP RECONNAISSANCE: {ip}")
    
    recon = IPRecon(shodan_key=shodan_key)
    results = recon.scan(ip)
    
    if not results['valid']:
        print_error("Invalid IP format")
        return
    
    print_success("Valid IP address")
    
    geo = results.get('geolocation', {})
    if geo and geo.get('country'):
        city = geo.get('city', 'N/A')
        region = geo.get('region', 'N/A')
        country = geo.get('country', 'N/A')
        print_info(f"Location: {city}, {region}, {country}")
        print_info(f"ISP: {geo.get('isp', 'N/A')}")
        print_info(f"Timezone: {geo.get('timezone', 'N/A')}")
        if geo.get('coordinates'):
            print_info(f"Coordinates: {geo['coordinates']}")
    
    abuse = results.get('reputation', {}).get('abuseipdb', {})
    if abuse and abuse.get('abuse_score'):
        score = abuse['abuse_score']
        reports = abuse.get('total_reports', 0)
        if score > 50:
            print_error(f"Abuse Score: {score}% ({reports} reports)")
        else:
            print_info(f"Abuse Score: {score}% ({reports} reports)")
    
    tor = results.get('reputation', {}).get('tor', {})
    if tor and tor.get('is_tor_exit'):
        print_error("⚠️  IP is Tor exit node")
    
    services = results.get('services', {})
    if services and services.get('open_ports'):
        ports = ', '.join(map(str, services['open_ports'][:20]))
        print_info(f"Open ports: {ports}")
        if services.get('hostnames'):
            print_info(f"Hostnames: {', '.join(services['hostnames'])}")
    
    dns = results.get('dns', {})
    if dns and dns.get('hostname'):
        print_info(f"Reverse DNS: {dns['hostname']}")
    
    print_header("IP CHECK COMPLETE")
    
    if export:
        with open(export, 'w') as f:
            json.dump(results, f, indent=2)
        print_success(f"Exported to {export}")

@cli.command()
@click.argument('target')
@click.option('--email', help='Email address to check')
@click.option('--phone', help='Phone number to check')
@click.option('--ip', help='IP address to check')
@click.option('--threads', default=10, help='Threads for username search')
@click.option('--export', type=click.Path(), help='Export all results to JSON')
@click.option('--shodan-key', envvar='SHODAN_API_KEY', help='Shodan API key')
def sweep(target: str, email: str, phone: str, ip: str, threads: int, export: str, shodan_key: str):
    """Full reconnaissance sweep (username + email + phone + IP)"""
    print_header("FULL OSINT RECONNAISSANCE SWEEP")
    
    all_results = {'target': target, 'scans': {}}
    
    if target:
        print_info("Running username scan...")
        user_recon = UsernameRecon(target, threads=threads)
        all_results['scans']['username'] = user_recon.scan()
        user_found = sum(1 for r in all_results['scans']['username'].values() if r.get('found'))
        print_success(f"Username found on {user_found} platforms")
    
    if email:
        print_info("Running email scan...")
        email_recon = EmailRecon()
        all_results['scans']['email'] = email_recon.scan(email)
        print_success("Email scan complete")
    
    if phone:
        print_info("Running phone scan...")
        phone_recon = PhoneRecon()
        all_results['scans']['phone'] = phone_recon.scan(phone)
        print_success("Phone scan complete")
    
    if ip:
        print_info("Running IP scan...")
        ip_recon = IPRecon(shodan_key=shodan_key)
        all_results['scans']['ip'] = ip_recon.scan(ip)
        print_success("IP scan complete")
    
    print_header("SWEEP COMPLETE")
    
    if export:
        with open(export, 'w') as f:
            json.dump(all_results, f, indent=2)
        print_success(f"All results exported to {export}")

@cli.command()
def version():
    """Show version"""
    from phantom import __version__
    print(f"PHANTOM v{__version__}")

def main():
    try:
        cli()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Scan interrupted{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print_error(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
