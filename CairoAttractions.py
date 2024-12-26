import SoupCreation
from urllib.parse import urljoin
import pandas as pd

url = "https://www.tripadvisor.com/Attractions-g294201-Activities-a_allAttractions.true-Cairo_Cairo_Governorate.html"

def CairoAttractions(start_url):
    # Initialize the URL for the first page
    url = start_url
    cairo_attractions = []

    while url:
        # Use SoupCreation to fetch the page and parse it into BeautifulSoup
        soup = SoupCreation.createSoup(url)
        if not soup:
            print("Failed to fetch or parse the page.")
            break

        # Find the attraction cards
        attraction_cards = soup.find_all("article", {'class': 'GTuVU XJlaI'})

        for card in attraction_cards:
            attraction_data = {}  # Reset the data for each card
            
            # Extract the name
            attraction_name = card.find('h3')
            attraction_data['name'] = attraction_name.text.strip() if attraction_name else 'No name available'

            # Extract the description
            description = card.find('span', {'class': 'SwTtt'})
            attraction_data['description'] = description.text.strip() if description else 'No description available'

            # Extract the rating
            rating = card.find('span', {'class': 'biGQs _P pZUbB hmDzD'})
            attraction_data['rating'] = rating.text.strip() if rating else 'No rating available'

            # Extract the number of ratings
            num_ratings = card.find('span', {'class': 'biGQs _P pZUbB osNWb'})
            attraction_data['num_ratings'] = num_ratings.text.strip() if num_ratings else 'No ratings available'

            # Extract the category
            category = card.find('div', {'class': 'biGQs _P pZUbB hmDzD'})
            attraction_data['category'] = category.text.strip() if category else 'No category available'

            # Extract the image src
            image = card.find('picture', {'class': 'NhWcC _R mdkdE afQPz eXZKw'})
            if image:
                img_tag = image.find('img')  # Find the 'img' tag inside the 'picture'
                attraction_data['image'] = img_tag['src'] if img_tag and 'src' in img_tag.attrs else 'No image available'
            else:
                attraction_data['image'] = 'No image available'

            # Append the attraction data to the list
            cairo_attractions.append(attraction_data)

        # Find the "Next" button URL
        next_page = soup.find('a', {'class': 'BrOJk u j z _F wSSLS tIqAi unMkR'})
        if next_page:
            next_url = next_page.get('href')
            url = urljoin(start_url, next_url)
        else:
            print("No more pages to fetch.")
            break  # Exit the loop when no "Next" button is found

    # Print or process the extracted data
    for attraction in cairo_attractions:
        print(attraction)

    # Convert the list of attractions to a DataFrame and save as Excel
    df = pd.DataFrame(cairo_attractions)
    df.to_excel("CairoAttractions.xlsx", index=False)

    print(f"Saved {len(cairo_attractions)} attractions to CairoAttractions.xlsx")

# Call the function with the starting URL
CairoAttractions(url)
