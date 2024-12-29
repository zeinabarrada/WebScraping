from urllib.parse import urljoin
import pandas as pd
import SoupCreation

# Starting URL for TripAdvisor's Cairo Attractions
url = "https://www.tripadvisor.com/Attractions-g294201-Activities-a_allAttractions.true-Cairo_Cairo_Governorate.html"

def CairoAttractions(url):
    # Initialize variables
    current_url = url
    cairo_attractions = []
    page_count = 0

    while current_url:
        page_count += 1
        print(f"Fetching page {page_count}: {current_url}")

        if page_count > 5:
            print("Page limit reached, stopping to avoid an infinite loop.")
            break

        # Fetch and parse the page using BeautifulSoup
        

        soup = SoupCreation.createSoup(current_url)
        if not soup:
            print("Failed to fetch or parse the page.")
            break

        # Find all attraction cards
        attraction_cards = soup.find_all("article", {'class': 'GTuVU XJlaI'})  # Update selector based on TripAdvisor's current structure
        if not attraction_cards:
            print(f"No attraction cards found on page {page_count}. Ending scrape.")
            break

        for card in attraction_cards:
            attraction_data = {}  # Store data for each attraction

            # Extract the name
            name = card.find('h3')
            attraction_data['name'] = name.text.strip() if name else 'No name available'

            # Extract the description
            description = card.find('span', {'class': 'SwTtt'})
            attraction_data['description'] = description.text.strip() if description else 'No description available'

            # Extract the category
            category = card.find('div', {'class': 'biGQs _P pZUbB hmDzD'})
            attraction_data['category'] = category.text.strip() if category else 'No category available'

            # Extract the image src or data-src (for lazy-loaded images)
            image = card.find('img')
            if image:
                attraction_data['image'] = image.get('data-src', image.get('src', 'No image available'))
            else:
                attraction_data['image'] = 'No image available'

            cairo_attractions.append(attraction_data)

        print(f"Page {page_count} processed: {len(attraction_cards)} attractions found.")

        # Find the "Next" button for pagination
        next_page = soup.find('a', {'class': 'BrOJk u j z _F wSSLS tIqAi unMkR'})  # Update selector as needed
        if next_page and next_page.get('href'):
            next_url = next_page['href']
            # Ensure the next_url is joined with the base current_url
            current_url = urljoin(current_url, next_url)
            print(current_url)
        else:
            print("No more pages found. Ending scrape.")
            break

    # Convert the extracted data to a DataFrame and save it as an Excel file
    if cairo_attractions:
        df = pd.DataFrame(cairo_attractions)
        df.to_excel("CairoAttractions.xlsx", index=False)
        print(f"Saved {len(cairo_attractions)} attractions to CairoAttractions.xlsx")
    else:
        print("No attractions data found to save.")

# Run the scraper
CairoAttractions(url)
