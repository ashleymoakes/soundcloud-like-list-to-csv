import soundcloud
import urllib.request
import json
import requests

clientID = "YOUR_CLIENT_ID_HERE"
client = soundcloud.Client(client_id=clientID)
api_base = "https://api.soundcloud.com"


def get_user_info(username):
    user = client.get('/resolve', url='http://soundcloud.com/{}/'.format(username))
    user_info = urllib.request.urlopen("{}/users/{}.json?consumer_key={}".format(api_base, user.id, clientID)).read()
    user_info_data = json.loads(user_info.decode())
    number_of_likes = user_info_data['public_favorites_count']
    username = user_info_data['username']
    return username, number_of_likes, user


user_information = get_user_info(input("Please enter your username: "))
user_name = user_information[0]
number_of_user_likes = user_information[1]
userID = user_information[2]

csv_file = open("{} like list.csv".format(user_name), "w", encoding='UTF-8')
csv_file.write("Track Title, Track URL\n")  # Writes headers to CSV file

offset_number = 0
while offset_number < number_of_user_likes:
    try:
        track_fetch = urllib.request.urlopen(
            "{}/users/{}/favorites.json?client_id={}&offset={}&limit1".format(api_base, userID.id,
                                                                              clientID, offset_number)).read()
        track_data = json.loads(track_fetch.decode())
        track_title = track_data[0]["title"].replace(",", "")  # Removes commas as causes issues with .csv files
        csv_file.write("{},{}\n".format(track_title, track_data[0]["permalink_url"]))
        offset_number += 1
        print("{} of {} ({}%)".format(offset_number, number_of_user_likes,
                                      round(float(100 / number_of_user_likes * offset_number), 2)))
    except IndexError:
        print("There is an issue with Soundcloud, please try again")
    except requests.HTTPError:
        print("There is an issue with Soundcloud, please try again")
    except requests.ConnectionError:
        print("Check your internet connection")