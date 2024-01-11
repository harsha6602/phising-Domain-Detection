import re
import socket
import ssl
import requests
from urllib.parse import urlparse
import whois
from datetime import date, datetime, time
from googlesearch import search
import bs4
from bs4 import BeautifulSoup
import dns.resolver

http_https = r"https://|http://"
special_characters = """!@#$%^&*()_+}{[]|\:"';<>?,-1234567890"""
shortening_services = r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|" \
                      r"yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|" \
                      r"short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|" \
                      r"doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|db\.tt|" \
                      r"qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|q\.gs|is\.gd|" \
                      r"po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|x\.co|" \
                      r"prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|" \
                      r"tr\.im|link\.zip\.net"


def _url_domain(url):
    try:
        pr_url = urlparse(url)
    except Exception as e:
        return 0
    return pr_url.netloc
#1
def has_ip(domain_name):
    try:
        ip_address = socket.gethostbyname(domain_name)
    except Exception as e:
        ip_address = ''              

    if (ip_address != ''):
        return 1
    else:
        return 0
#2
def url_length(url):
    try:
            if len(url) > 0:
                return len(url)
            else:
                return 0
    except Exception as e:
        return 0
#3
def number_of_special_charectors(domain_name):
    try:
        count_specil_charectors_in_domain = 0
        for i in domain_name.strip():
            if i in special_characters:
                count_specil_charectors_in_domain +=1
        if count_specil_charectors_in_domain > 0:
            return count_specil_charectors_in_domain
        else:
            return 0
    except:
        pass
#4
def _has_ssl(hostname):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
    except Exception as e:
        return 0
    return 1
#5
def number_of_name_servers(domain):
    try:
        name_servers = 0
        ns_records = dns.resolver.resolve(domain, 'NS')
        name_servers = len(ns_records)
        return name_servers
    except Exception as e:
        return 0
#6 and #7
def number_of_href_links(soup):
    try:
        href_links = []
        for link in soup.findAll('a'):
            href_links.append(link.get('href'))
        if len(href_links) > 0:
            return len(href_links)
        return 0
    except Exception as e:
        return 0

#8
def has_pop_up(soup):
    javascript_code = soup.find_all('script')
    popup_keywords = ["alert(", "window.open(", "modal("]
    found_popups = False
    
    for code in javascript_code:
        if code.string:
            for keyword in popup_keywords:
                if keyword in code.string:
                    found_popups = True
                    break
        if found_popups:
            break  
    
    if found_popups:
        return 1
    else:
        return 0

#9
def has_input(soup):
    if len(soup.find_all("input")):
        return 1
    else:
        return 0
#10
def has_password(soup):
    for input in soup.find_all("input"):
        if (input.get("type") or input.get("name") or input.get("id")) == "password":
            return 1
        else:
            pass
    return 0
#11
def domain_age(domain_name):
    try:
        domain_info = whois.whois(domain_name)
        if isinstance(domain_info.creation_date, list):
            creation_date = domain_info.creation_date[0]
        else:
            creation_date = domain_info.creation_date
        
        if creation_date:
            current_year = 2023
            domain_age = current_year - creation_date.year
            return domain_age
        else:
            return 0
    except Exception as e:
        return -1
#12
def number_of_subdomains(url):
        dot_count = len(re.findall("\.", url))
        if dot_count == 1:
            return 1
        elif dot_count == 2:
            return 0
        return -1

#13
def has_favicon(soup, domain):
    try:
        for head in soup.find_all('head'):
            for head_link in soup.find_all('link', href=True):
                dots = [x.start(0) for x in re.finditer('\.', head_link['href'])]
                if domain in head_link['href'] or len(dots) == 1:
                    return 1
        return 0
    except:
        return -1
#14
def NonStdPort(domain):
    try:
        port = domain.split(":")
        if len(port)>1:
            return -1
        return 1
    except:
        return -1
#15
def LinksInScriptTags(domain, soup):
    try:
        i, success = 0, 0

        for link in soup.find_all('link', href=True):
            if domain in link['href']:
                success += 1
            i += 1

        for script in soup.find_all('script', src=True):
            if domain in script['src']:
                success += 1
            i += 1

        try:
            percentage = success / float(i) * 100
            if percentage < 17.0:
                return 1
            elif 17.0 <= percentage < 81.0:
                return 0
            else:
                return -1
        except ZeroDivisionError:
            return 0
    except Exception as e:
        return -1
#17
def has_title(soup):
    if soup.title is None:
        return 0
    if len(soup.title.text) > 0:
        return 1
    else:
        return 0
#18
def has_submit(soup):
    for button in soup.find_all("input"):
        if button.get("type") == "submit":
            return 1
        else:
            pass
    return 0
#19
def has_button(soup):
    if len(soup.find_all("button")) > 0:
        return 1
    else:
        return 0
#20
def has_link(soup):
    if len(soup.find_all("link")) > 0:
        return 1
    else:
        return 0

#22
def has_email_input(soup):
    for input in soup.find_all("input"):
        if (input.get("type") or input.get("id") or input.get("name")) == "email":
            return 1
        else:
            pass
    return 0
#23
def has_hidden_element(soup):
    for input in soup.find_all("input"):
        if input.get("type") == "hidden":
            return 1
        else:
            pass
    return 0
#24
def has_audio(soup):
    if len(soup.find_all("audio")) > 0:
        return 1
    else:
        return 0
#25
def has_video(soup):
    if len(soup.find_all("video")) > 0:
        return 1
    else:
        return 0
#26
def number_of_inputs(soup):
    if len(soup.find_all("input")) > 0:
        return len(soup.find_all("input"))
    else:
        return 0
#28
def number_of_images(soup):
    image_tags = len(soup.find_all("image"))
    count = 0
    for meta in soup.find_all("meta"):
        if meta.get("type") or meta.get("name") == "image":
            count += 1
    return image_tags + count
#29
def number_of_option(soup):
    if len(soup.find_all("option")) > 0:
        return len(soup.find_all("option"))
    else:
        return 0
#30
def number_of_list(soup):
    if len(soup.find_all("li")) > 0:
        return len(soup.find_all("li"))
    else:
        return 0
#31
def number_of_TR(soup):
    if len(soup.find_all("tr")) > 0:
        return len(soup.find_all("tr"))
    else:
        return 0
#32
def number_of_TH(soup):
    if len(soup.find_all("th")) > 0:
        return len(soup.find_all("th"))
    else:
        return 0
#33
def number_of_paragraph(soup):
    if len(soup.find_all("p")) > 0:
        return len(soup.find_all("p"))
    else:
        return 0
#34
def number_of_script(soup):
    if len(soup.find_all("script")) > 0:
        return len(soup.find_all("script"))
    else:
        return 0
#35
def length_of_title(soup):
    title = soup.find('title')

    if title is not None:
        title_text = title.get_text()
        return len(title_text)
    else:
        return 0
#36
def has_h1(soup):
    if len(soup.find_all("h1")) > 0:
        return 1
    else:
        return 0
#37
def has_h2(soup):
    if len(soup.find_all("h2")) > 0:
        return 1
    else:
        return 0
#38
def has_h3(soup):
    if len(soup.find_all("h3")) > 0:
        return 1
    else:
        return 0
#39
def length_of_text(soup):
    return len(soup.get_text())
#40
def number_of_clickable_button(soup):
    try:
        count = 0
        for button in soup.find_all("button"):
            if button.get("type") == "button":
                count += 1
            return count
        return 0
    except Exception as e:
        return 0
#41
def number_of_a(soup):
    if len(soup.find_all("a")) > 0:
        return len(soup.find_all("a"))
    else:
        return 0
#42
def number_of_div(soup):
    if len(soup.find_all("div")) > 0:
        return len(soup.find_all("div"))
    else:
        return 0
#43
def number_of_figure(soup):
    if len(soup.find_all("figure")) > 0:
        return len(soup.find_all("figure"))
    return 0
#44
def has_footer(soup):
    if len(soup.find_all("footer")) > 0:
        return 1
    else:
        return 0
#45
def has_form(soup):
    if len(soup.find_all("form")) > 0:
        return 1
    else:
        return 0
#46
def has_text_area(soup):
    if len(soup.find_all("textarea")) > 0:
        return 1
    else:
        return 0
#47
def has_iframe(soup):
    if len(soup.find_all("iframe")) > 0:
        return 1
    else:
        return 0
#48
def has_text_input(soup):
    for input in soup.find_all("input"):
        if input.get("type") == "text":
            return 1
    return 0
#49
def number_of_meta(soup):
    return len(soup.find_all("meta"))
#50
def has_nav(soup):
    if len(soup.find_all("nav")) > 0:
        return 1
    else:
        return 0

#51
def has_object(soup):
    if len(soup.find_all("object")) > 0:
        return 1
    else:
        return 0
#52
def has_picture(soup):
    if len(soup.find_all("picture")) > 0:
        return 1
    else:
        return 0
#53
def number_of_sources(soup):
    if len(soup.find_all("source"))>0:
        return len(soup.find_all("source"))
    else:
        return 0
#54
def number_of_span(soup):
    if len(soup.find_all("span")) > 0:
        return len(soup.find_all("span"))
    else:
        return 0
#55
def number_of_table(soup):
    if len(soup.find_all("table")) > 0:
        return len(soup.find_all("table"))
    else:
        return 0
#56
def number_link(soup):
    if len(soup.find_all("img")) > 0:
        return len(soup.find_all("img"))
    else:
        return 0
#57
def has_abnormalURL(response, domain):
    try:
        whois_response = whois.whois(domain)
        if response.text == str(whois_response):
            return 1
        else:
            return 0
    except Exception as e:
        return -1
#58
def has_dns_recording(domain):
    try:
        whois_response = whois.whois(domain)
        creation_date = whois_response.creation_date
        try:
            if(len(creation_date)):
                creation_date = creation_date[0]
        except Exception as e:
            print(e)
            return -1
        today  = date.today()
        age = (today.year-creation_date.year)*12+(today.month-creation_date.month)
        if age >=6:
            return 1
        return 0
    except Exception as e:
        return 0
#59
def GoogleIndex(url):
    try:
        site = search(url, 5)
        if site:
            return 1
        else:
            return 0
    except:
        return -1
#60
def double_slash_redirecting(domain):
    last_double_slash = domain.rfind('//')
    return -1 if last_double_slash > 6 else 1

#61
def domain_registration_length(domain):
    try:
        # Extract the domain name from the URL
        domain_info = whois.whois(domain)

        if isinstance(domain_info.expiration_date, list):
            expiration_date = domain_info.expiration_date[0]
        else:
            expiration_date = domain_info.expiration_date

        if not expiration_date:
            return -1

        today = datetime.now()
        registration_length = (expiration_date - today).days

        return 0 if registration_length / 365 <= 1 else 1
    except Exception as e:
        return 0
#62
def statistical_report(url, hostname):
    try:
        ip_address = socket.gethostbyname(hostname)
    except:
        return -1
    url_match = re.search(
        r'at\.ua|usa\.cc|baltazarpresentes\.com\.br|pe\.hu|esy\.es|hol\.es|sweddy\.com|myjino\.ru|96\.lt|ow\.ly', url)
    ip_match = re.search(
        '146\.112\.61\.108|213\.174\.157\.151|121\.50\.168\.88|192\.185\.217\.116|78\.46\.211\.158|181\.174\.165\.13|46\.242\.145\.103|121\.50\.168\.40|83\.125\.22\.219|46\.242\.145\.98|'
        '107\.151\.148\.44|107\.151\.148\.107|64\.70\.19\.203|199\.184\.144\.27|107\.151\.148\.108|107\.151\.148\.109|119\.28\.52\.61|54\.83\.43\.69|52\.69\.166\.231|216\.58\.192\.225|'
        '118\.184\.25\.86|67\.208\.74\.71|23\.253\.126\.58|104\.239\.157\.210|175\.126\.123\.219|141\.8\.224\.221|10\.10\.10\.10|43\.229\.108\.32|103\.232\.215\.140|69\.172\.201\.153|'
        '216\.218\.185\.162|54\.225\.104\.146|103\.243\.24\.98|199\.59\.243\.120|31\.170\.160\.61|213\.19\.128\.77|62\.113\.226\.131|208\.100\.26\.234|195\.16\.127\.102|195\.16\.127\.157|'
        '34\.196\.13\.28|103\.224\.212\.222|172\.217\.4\.225|54\.72\.9\.51|192\.64\.147\.141|198\.200\.56\.183|23\.253\.164\.103|52\.48\.191\.26|52\.214\.197\.72|87\.98\.255\.18|209\.99\.17\.27|'
        '216\.38\.62\.18|104\.130\.124\.96|47\.89\.58\.141|78\.46\.211\.158|54\.86\.225\.156|54\.82\.156\.19|37\.157\.192\.102|204\.11\.56\.48|110\.34\.231\.42',
        ip_address)
    if url_match:
        return -1
    elif ip_match:
        return -1
    else:
        return 1
#----
#63
def submitting_to_email(soup):
    for form in soup.find_all('form', action=True):
        return -1 if "mailto:" in form['action'] else 1
    return 1

#64
def https_token(domain):
    match = re.search(http_https, domain)
    return 0 if match else 1

#65
def count_redirects(domain):
    try:
        url = "http://" + domain  # Assuming HTTP, you can modify this if your URLs might use HTTPS
        response = requests.get(url)
        redirect_count = 0

        while response.history:
            redirect_count += 1
            response = requests.get(response.url)

        return redirect_count
    except Exception as e:
        return -1

#66
def has_executable_files(soup):
    try:
        executable_extensions = ['.exe', '.bat', '.msi','.sh']
        links = soup.find_all('a', href=True)
        for link in links:
            href = link['href']
            if any(href.endswith(ext) for ext in executable_extensions):
                return 1
        return 0
    except Exception as e:
        return -1

#67
def count_javascript_files(soup):
    try:
        js_files = [script['src'] for script in soup.find_all('script', src=True) if script['src'].endswith('.js')]
        return len(js_files)
    except Exception as e:
        return -1
#68
def number_of_emails(domain):
    try:
        whois_info = whois.whois(domain)
        number_emails = whois_info['emails']
        if len(number_emails)>0:
            return len(number_emails)
        else:
            return 0
    except Exception as e:
        return -1
    return 0
#69
def get_ssl_update_age(domain):
    try:
        whois_response = whois.whois(domain)
        cert_data = whois_response["updated_date"]
        given_date_time_str = str(cert_data)
        given_date_time = datetime.strptime(given_date_time_str, "%Y-%m-%d %H:%M:%S")
        current_date_time = datetime.utcnow()
        age = current_date_time - given_date_time
        return age.days
    except Exception as e:
        return -1
#70
def get_ip_count(domain):
    try:
        ips = socket.gethostbyname_ex(domain)[2]
        return len(ips)
    except socket.gaierror:
        return 0
#71
def get_ssl_expiry_duration(domain):
    try:
        whois_response = whois.whois(domain)
        cert_data = whois_response["expiration_date"]
        expiry_date_str = str(cert_data[0]) if isinstance(cert_data, list) else str(cert_data)
        expiry_date_time = datetime.strptime(expiry_date_str, "%Y-%m-%d %H:%M:%S")
        current_date_time = datetime.utcnow()
        duration = expiry_date_time - current_date_time
        return duration.days
    except Exception as e:
        return -1
#72
def number_of_smtp_servers(domain):
    try:
        mx_records = dns.resolver.resolve(domain, 'MX')
        if len(mx_records)>0:
            return len(mx_records)
        else:
            return 0
    except Exception as e:
        return -1
#73
def number_of_txt_records(domain):
    try:
        txt_records = dns.resolver.resolve(domain, 'TXT')
        if len(txt_records)>0:
            return len(txt_records)
    except Exception as e:
        return -1
#74
def shortening_service(url):
    try:
        match = re.search(shortening_services, url)
        return 1 if match else 0
    except:
        return -1

