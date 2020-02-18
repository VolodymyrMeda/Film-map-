# Film-map-

Description:
The program generates the map and there puts icons of 10 closest films to the location user entered and includes 
the layer of countries population


Packages used:
- folium - map generating 
- pandas - reading the csv file
- ssl - error fixing
- geocoder - getting lat-lon location 
- math - counting the distance between two locations


Program functions:
1. year_films - function returns a list of tuples in which first element is a film
    name, second element is year and the third one is location.
    That reduces the number of elements that have to be investigated
2. closest_films - function reads the file, gets locations of the films stared in
    entered year and returns a list with 10 closest films
    depending on the location user entered
3. distance_count - function counts the distance between two lat-lon coordinates
4. distance_sorter - function returns sorted by distance list of tuples
5. main_map - function generates a map with film icons

Example:
