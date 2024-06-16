import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

'''
edge_driver_path = 'C:\\Users\\User\\Desktop\\webdriver\\msedgedriver.exe'  # Update this path


edge_service = EdgeService(executable_path=edge_driver_path)
driver = webdriver.Edge(service=edge_service)



def Percentage_Expenditure_Func(country, url='https://data.worldbank.org/indicator/GC.XPN.TOTL.GD.ZS'):
    
    driver.get(url)
    target_div = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, f"div[data-customlink='nl:body content'][data-text='{country_name}']"))
    )
    sibling_div = target_div.find_element(By.XPATH, "following-sibling::div")
    sibling_div = sibling_div.find_element(By.XPATH, "following-sibling::div")
    # Print the text content of the target div
    Percentage_Expenditure = sibling_div.text
    return(Percentage_Expenditure)

def Population_Func(country, url='https://data.worldbank.org/indicator/SP.POP.TOTL?most_recent_value_desc=true'):
    
    driver.get(url)
    target_div = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, f"div[data-customlink='nl:body content'][data-text='{country}']"))
    )
    sibling_div = target_div.find_element(By.XPATH, "following-sibling::div")
    sibling_div = sibling_div.find_element(By.XPATH, "following-sibling::div")
    Population = sibling_div.text
    print(Population)

def scrape(country_name):
    #Not implemented
    try:
        percentageExpenditure = Percentage_Expenditure_Func(country_name)
        population = Population_Func(country_name)
        co2 = CO2_Func(country_name)
        totalExpenditura = Total_Expenditure_Func(country_name)
        gdp = GDP_Func(country_name)
        smoking = Smoking_Func(country_name)
        schooling = Schooling_Func(country_name)
        alcohol = Alcohol_Func(country_name)


    except:
        print("There has been an issue while scraping the web for updated data")

    

# Wait for the content to load

Developed = ["France", "Finland", "Grece", "Estonia"]
try:
    
    country = input("Write the country here with the first letter being uppercase: ")
    scrape(country)
    if country in Developed:
        status = "1"
    else:
        status = "0"
except Exception as e:
    if country == "Slovakia":
        country = "Slovak Republic"
    scrape(country)
finally:
    
    driver.quit()
'''