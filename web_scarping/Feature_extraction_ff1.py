import web_scarping.feature_init_ff1 as fe
import requests
from bs4 import BeautifulSoup

protocols = ["https", "http"]

def get_url_from_domain(domain, protocol):
    return f"{protocol}://{domain}"

def process_urls(domain_name, protocols):
    list_200 = []
    
    for protocol in protocols:
        try:
            url = get_url_from_domain(domain_name, protocol)
            response = requests.get(url)
            if response.status_code==200:
                list_200.append(url)
            else:
                print(response.status_code)
        except Exception as e:
            pass
    return list_200

#main
def data_set_list_creation(domain):
    try:
        lis_success = process_urls(domain, protocols)
        if len(lis_success) != 0:
            url = lis_success[0]
            url = str(url)
            response = requests.get(url)
            print("{url} --> ",url,"{Response} = ",response.status_code)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
            else:
                return "Not accessable "+url
        else:
            return "Not accessable"+url
    except Exception as e:
        pass

    try:
        if soup != None:
            domain = fe._url_domain(url)
            features_list_ml = [
                        fe.url_length(domain),
                        fe.number_of_special_charectors(domain),
                        fe._has_ssl(domain),
                        fe.number_of_name_servers(domain),
                        fe.number_of_href_links(soup),
                        fe.has_pop_up(soup),
                        fe.has_input(soup),
                        fe.has_password(soup),
                        fe.domain_age(domain),
                        fe.number_of_subdomains(url),
                        fe.has_favicon(soup, domain),
                        #fe.NonStdPort(domain),
                        fe.LinksInScriptTags(domain, soup),
                        fe.has_title(soup),
                        fe.has_submit(soup),
                        fe.has_button(soup),
                        fe.has_link(soup),
                        fe.has_email_input(soup),
                        fe.has_hidden_element(soup),
                        fe.has_audio(soup),
                        fe.has_video(soup),
                        fe.number_of_inputs(soup),
                        fe.number_of_images(soup),
                        fe.number_of_option(soup),
                        fe.number_of_list(soup),
                        fe.number_of_TR(soup),
                        fe.number_of_TH(soup),
                        fe.number_of_paragraph(soup),
                        fe.number_of_script(soup),
                        fe.length_of_title(soup),
                        fe.has_h1(soup),
                        fe.has_h2(soup),
                        fe.has_h3(soup),
                        fe.length_of_text(soup),
                        fe.number_of_clickable_button(soup),
                        fe.number_of_a(soup),
                        fe.number_of_div(soup),
                        fe.number_of_figure(soup),
                        fe.has_footer(soup),
                        fe.has_form(soup),
                        fe.has_text_area(soup),
                        fe.has_iframe(soup),
                        fe.has_text_input(soup),
                        fe.number_of_meta(soup),
                        fe.has_nav(soup),
                        fe.has_object(soup),
                        fe.has_picture(soup),
                        fe.number_of_sources(soup),
                        fe.number_of_span(soup),
                        fe.number_of_table(soup),
                        fe.number_link(soup),
                        fe.has_abnormalURL(response, domain),
                        fe.has_dns_recording(domain),
                        #fe.GoogleIndex(url),
                        #fe.double_slash_redirecting(domain),
                        fe.domain_registration_length(domain),
                        fe.statistical_report(url, domain),
                        fe.submitting_to_email(soup),
                        #fe.https_token(domain),
                        fe.count_redirects(domain),
                        fe.has_executable_files(soup),
                        fe.count_javascript_files(soup),
                        fe.number_of_emails(domain),
                        fe.get_ssl_update_age(domain),
                        fe.get_ip_count(domain),
                        fe.get_ssl_expiry_duration(domain),
                        fe.number_of_smtp_servers(domain),
                        fe.number_of_txt_records(domain),
                        fe.shortening_service(url),

            ]
            return features_list_ml
        else:
            print("Else")
    except Exception as e:
        print(e)