# main_script.py
import SoupCreation

url = "https://www.tripadvisor.com/Attractions-g294201-Activities-a_allAttractions.true-Cairo_Cairo_Governorate.html"

def CairoAttractions(url):
    # Use SoupCreation to fetch the page and parse it into BeautifulSoup
    soup = SoupCreation.createSoup(url)
    
    cairo_attractions = []
    
    # Try finding the elements again using the correct class or structure
    attraction_cards = soup.find_all("article", {'class': 'GTuVU XJlaI'})
    
    for card in attraction_cards:
        # Example: extracting the name or other info from each attraction card
        attraction_name = card.find('h3')  # Adjust this selector as necessary
        if attraction_name:
            print(attraction_name.text)
            cairo_attractions.append(attraction_name.text)
    
    # You can now process the `cairo_attractions` list as needed
    print(cairo_attractions)

CairoAttractions(url)
