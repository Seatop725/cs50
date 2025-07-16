import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass



def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    
        source (date type Int): the id number of your source actor
        target (data type Int): the id number of your target actor
        
    Returns the path (data type list) of the form of tuples of (movie_id, person_id), 
    """
    start = Node(source, parent=None, action=None)
    # state = person_id of the person you are looking at currently
    # action = the movie they are involved in that connects them to the next 
    #          person in the sequence
    frontier = QueueFrontier()
    frontier.add(start)
    
    
    '''Figure out the use of birthdays once the code functions as is'''
    # sourceBY = people[source][1]
    # targetBY = people[target][1]
    # targetMovies = people[target][2]
    # targetMoviesYears = []
    # for m in targetMovies:
    #     year = m[1]
    #     targetMoviesYears.append(year)
    # minYear = min(targetMoviesYears)
    # This will be used to eliminate actors that cannot have been in a movie 
    # with the target by their birth year. An actor cannot have been in a movie
    # if they were born before it came out ie, it must be true that 
    # people[actor]["birth"] > minYear

    
    explored = set()
    
    while True:
        if frontier.empty():
            raise Exception("These two actors are not connected")
            return None
        
        node = frontier.remove()
        
        explored.add(node.state)
        
        
        if node.state==target:
            movies=[]
            stars=[]
            while node.parent is not None:
                movies.append(node.action)
                stars.append(node.state)
                node = node.parent
            movies.reverse()
            stars.reverse()
            solution = [(movies[i], stars[i]) for i in range(len(movies))]
            return solution
        
        
        for movie_id, person_id in neighbors_for_person(node.state):
            if not frontier.contains_state(person_id) and person_id not in explored:
                child = Node(state=person_id, parent=node, action=movie_id)
                frontier.add(child)
    
    raise NotImplementedError


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors

def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"
    '''LEAVE THIS ALONE
       Amend to take in input for testing'''

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Source name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Target name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


if __name__ == "__main__":
    main()
