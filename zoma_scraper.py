import csv, json, requests, random
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

def fetch_data():
    unique = []
    base_url = 'https://www.zomato.com'
    country_url = 'https://www.zomato.com/india'  # change with country u want to scrape
    profile = FirefoxProfile(r"E:\SCRAPING\Tor Browser\Browser\TorBrowser\Data\Browser\profile.default")
    profile.set_preference('network.proxy.type', 5)
    profile.set_preference('network.proxy.socks', '127.0.0.1')
    profile.set_preference('network.proxy.socks_port', 9050)
    profile.set_preference("network.proxy.socks_remote_dns", False)
    profile.update_preferences()
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.set_headless(headless=True)
    with webdriver.Firefox(firefox_profile= profile, options = firefox_options, executable_path=r'E:\SCRAPING\geckodriver.exe') as driver:
        driver.get(country_url)

        soup1 = BeautifulSoup(driver.page_source, 'lxml')
        states_links = soup1.find('div', {'class': 'states-container'}).findAll('div', {'class':'bke1zw-1'})
        random.shuffle(states_links)
        for div in states_links:
            driver.get(div.find('a')['href'])
            sleep(2.5)
            try:
                l = driver.find_elements_by_class_name('jumbo-tracker')
                while True:
                    driver.execute_script("arguments[0].scrollIntoView(true);", l[-1])
                    sleep(3.5)
                    new_divs = driver.find_elements_by_class_name('jumbo-tracker')
                    if len(l) == len(new_divs):
                        break
                    l = driver.find_elements_by_class_name('jumbo-tracker')
                sleep(5)
                soup2 = BeautifulSoup(driver.page_source, 'lxml')
                divs = soup2.findAll('div', {'class': 'jumbo-tracker'})
                random.shuffle(divs)
                for link in divs:
                    if link.findAll('a'):
                        page_url = base_url + link.findAll('a')[0]['href']
                        driver.get(page_url)
                        # sleep(2)
                        soup3 = BeautifulSoup(driver.page_source, 'lxml')
                        scripts = soup3.findAll('script', {'type':'application/ld+json'})
                        for i in scripts:
                            tag = str(i).split('son">')[1].split('</script>')[0]
                            jd = json.loads(tag)
                            if jd['@type'] == "Restaurant":
                                item = []
                                item.append(base_url)
                                item.append(jd['name'])
                                item.append(jd['address']['streetAddress'].replace(jd['address']['addressLocality'], ''))
                                item.append(jd['address']['addressLocality'].replace(jd['address']['addressRegion'], ''))
                                item.append(jd['address']['addressRegion'])
                                item.append(jd['address']['postalCode'])
                                item.append(jd['address']['addressCountry'])
                                item.append(jd['@type'])
                                item.append(jd['geo']['latitude'])
                                item.append(jd['geo']['longitude'])
                                item.append(jd['telephone'])
                                item.append(jd['paymentAccepted'])
                                item.append(jd['servesCuisine'])
                                if 'aggregateRating' in jd.keys():
                                    item.append(jd['aggregateRating']['ratingValue'])
                                    item.append(jd['aggregateRating']['ratingCount'])
                                else:
                                    item.append("<MISSING>")
                                    item.append("<MISSING>")
                                item.append(page_url)
                                item = [str(x).replace('\n', ' ').replace('\t', '').replace('\r', '') if x else "<MISSING>" for x in item]
                                if item[1]+item[2] not in unique:
                                    unique.append(item[1]+item[2])
                                    yield item
                    else:
                        print(link)

            except :
                soup4 = BeautifulSoup(driver.page_source, 'lxml')
                area_urls = soup4.find('div', class_='title').next_sibling.findAll('a')
                random.shuffle(area_urls)
                for area in area_urls:
                    driver.get(area['href'])
                    sleep(2)
                    l = driver.find_elements_by_class_name('jumbo-tracker')
                    while True:
                        driver.execute_script("arguments[0].scrollIntoView(true);", l[-1])
                        sleep(3.5)
                        new_divs = driver.find_elements_by_class_name('jumbo-tracker')
                        if len(l) == len(new_divs):
                            break
                        l = driver.find_elements_by_class_name('jumbo-tracker')
                    sleep(5)
                    soup5 = BeautifulSoup(driver.page_source, 'lxml')
                    divs = soup5.findAll('div', {'class': 'jumbo-tracker'})
                    random.shuffle(divs)
                    for page_div in divs:
                        if page_div.findAll('a'):
                            page_url = base_url + page_div.findAll('a')[0]['href']
                            driver.get(page_url)
                            # sleep(2)
                            soup3 = BeautifulSoup(driver.page_source, 'lxml')
                            scripts = soup3.findAll('script', {'type':'application/ld+json'})
                            for i in scripts:
                                tag = str(i).split('son">')[1].split('</script>')[0]
                                jd = json.loads(tag)
                                if jd['@type'] == "Restaurant":
                                    item = []
                                    item.append(base_url)
                                    item.append(jd['name'])
                                    item.append(jd['address']['streetAddress'].replace(jd['address']['addressLocality'], ''))
                                    item.append(jd['address']['addressLocality'].replace(jd['address']['addressRegion'], ''))
                                    item.append(jd['address']['addressRegion'])
                                    item.append(jd['address']['postalCode'])
                                    item.append(jd['address']['addressCountry'])
                                    item.append(jd['@type'])
                                    item.append(jd['geo']['latitude'])
                                    item.append(jd['geo']['longitude'])
                                    item.append(jd['telephone'])
                                    item.append(jd['paymentAccepted'])
                                    item.append(jd['servesCuisine'])
                                    if 'aggregateRating' in jd.keys():
                                        item.append(jd['aggregateRating']['ratingValue'])
                                        item.append(jd['aggregateRating']['ratingCount'])
                                    else:
                                        item.append("<MISSING>")
                                        item.append("<MISSING>")
                                    item.append(page_url)
                                    item = [str(x).replace('\n', ' ').replace('\t', '').replace('\r', '') if x else "<MISSING>" for x in item]
                                    if item[1]+item[2] not in unique:
                                        unique.append(item[1]+item[2])
                                        yield item
                        else:
                            print(div)

def write_output(data):
    with open('zomato_india.csv', mode='w', encoding="utf-8",newline="") as output_file:
        writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerow(["base_url", "location_name", "street_address", "locality", "city", "zip", "country",
                         "location_type", "latitude", "longitude", "phone", "payment_methods_accepted", "types_of_food_served", "rating", "no_of_reviews", "page_url"])
        for row in data:
            writer.writerow(row)

def scrape():
    data = fetch_data()
    write_output(data)

scrape()
