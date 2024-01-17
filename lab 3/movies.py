movies = [
{
"name": "Usual Suspects", 
"imdb": 7.0,
"category": "Thriller"
},
{
"name": "Hitman",
"imdb": 6.3,
"category": "Action"
},
{
"name": "Dark Knight",
"imdb": 9.0,
"category": "Adventure"
},
{
"name": "The Help",
"imdb": 8.0,
"category": "Drama"
},
{
"name": "The Choice",
"imdb": 6.2,
"category": "Romance"
},
{
"name": "Colonia",
"imdb": 7.4,
"category": "Romance"
},
{
"name": "Love",
"imdb": 6.0,
"category": "Romance"
},
{
"name": "Bride Wars",
"imdb": 5.4,
"category": "Romance"
},
{
"name": "AlphaJet",
"imdb": 3.2,
"category": "War"
},
{
"name": "Ringing Crime",
"imdb": 4.0,
"category": "Crime"
},
{
"name": "Joking muck",
"imdb": 7.2,
"category": "Comedy"
},
{
"name": "What is the name",
"imdb": 9.2,
"category": "Suspense"
},
{
"name": "Detective",
"imdb": 7.0,
"category": "Suspense"
},
{
"name": "Exam",
"imdb": 4.2,
"category": "Thriller"
},
{
"name": "We Two",
"imdb": 7.2,
"category": "Romance"
}
]

def hight_score(movs):
    listof = []
    for x in movs:
        if x["imdb"] > 5.5:
            listof.append(f"{x["name"]}")
    return "\n".join(listof)

def listof_hight_score(movs):
    listof = []
    for x in movs:
        if x["imdb"] > 5.5:
            listof.append(f"{x['name']}, {x['imdb']}, {x['category']}")
    return "\n".join(listof)

def find_all_from_category(movs, category):
    listof = []
    for x in movs:
        if x["category"] == category:
            listof.append(f"{x["name"]}")
    return "\n".join(listof)

def avg_rating(movs):
    rating = 0
    for x in movs:
        rating+=x["imdb"]
    return rating/len(movs)

def avg_rating_from_category(movs, category):
    rating = 0
    i=0
    for x in movs:
        if x["category"] == category:
            rating+=x["imdb"]
            i+=1
    return rating/i if i > 0 else 0 # add checking for dividing to zero to avoid errors

print(hight_score(movies))
print(listof_hight_score(movies))
print(find_all_from_category(movies, "Suspense"))
print(avg_rating(movies))
print(avg_rating_from_category(movies, "Suspense"))