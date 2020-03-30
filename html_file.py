# With local file
with open('simple.html', 'r') as html_file:
    soup = BeautifulSoup(html_file, 'lxml')

# Looping over multiple elements
for article in soup.find_all('div', class_='article'):
    headline = article.h2.a.text
    print(headline)

    summary = article.p.text
    print(summary)
    
    print()