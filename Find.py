import asyncio
async def GetPrices(ADDRESS : str, HOUSE_NUMBER : str):
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    import time
    import logging

    # Dissable logging
    logger = logging.getLogger('selenium.webdriver.remote.remote_connection')
    logger.setLevel(logging.CRITICAL)

    # Create Edge option settings
    options = webdriver.EdgeOptions()
    options.add_argument("--headless")
    options.add_argument('window-size=1920x1080')
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("--log-level=3")

    # Create Edge driver
    driver = webdriver.Edge(options=options)

    # Go to uswitch.com
    driver.get("https://www.uswitch.com/broadband/")

    # Hide the cookie banner
    driver.execute_script('document.getElementsByClassName("ucb")[0].style.display="none"')
    driver.implicitly_wait(3)

    # Input the address
    driver.find_element(By.ID,"hero-postcode-input").send_keys(ADDRESS)
    driver.find_element(By.ID,"hero-postcode-input").click()
    driver.implicitly_wait(3)

    # Click the correct house number
    addresses={a.text : a for a in driver.find_elements(By.CSS_SELECTOR,'[data-cypress-id="address-list-item"]')}
    addresses=([a[1] for a in addresses.items() if a[0].split()[0]==HOUSE_NUMBER])[0].click()

    # Set "I'm not sure" for the provider and submit the form
    driver.find_elements(By.CSS_SELECTOR,'[data-cypress-id="provider-dropdown"]')[0].click()
    driver.find_element(By.CSS_SELECTOR,'[value="im-not-sure"]').click()
    driver.find_element(By.CSS_SELECTOR,'[data-cypress-id="hero-form-submit"]').click()

    time.sleep(3)

    # Get the deals
    dealNames=[a.find_elements(By.CSS_SELECTOR,"*")[0].get_attribute('content') for a in driver.execute_script('return document.getElementsByClassName("styles-module__title___22yE+")')]
    dealSpeeds=[a.get_attribute("innerHTML") for a in driver.execute_script('return document.getElementsByClassName("styles-module__titleLarge___f1KtB")')[::2]]
    dealPrices=[a.find_elements(By.TAG_NAME,"span")[1].get_attribute("content") for a in driver.execute_script('return document.getElementsByClassName("styles-module__titleLarge___f1KtB")')[1::2]]
    
    # Close the driver
    driver.quit()

    # return it in a string
    return ",".join([(dealNames[i]+" "+dealSpeeds[i]+"Mbps "+"£"+dealPrices[i]) for i in range(len(dealNames))])

