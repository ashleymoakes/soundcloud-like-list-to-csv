import soundcloud
import urllib.request
import json
import requests

clientID = "YOUR_CLIENT_ID_HERE"
client = soundcloud.Client(client_id=clientID)

username = input("Please enter your Soundcloud username: ")
user = client.get('/resolve', url='http://soundcloud.com/{}/'.format(username))
user_info = urllib.request.urlopen("https://api.soundcloud.com/users/{}.json?consumer_key={}".format(user.id,
                                                                                                     clientID)).read()
user_info_data = json.loads(user_info.decode())
number_of_likes = user_info_data['public_favorites_count']
user_name = user_info_data['username']
print("You have liked a total of {} tracks.".format(number_of_likes))

csv_file = open("{} like list.csv".format(user_name), "w", encoding='UTF-8')
csv_file.write("Track Title,Track URL\n")  # Writes headers to CSV file

offset_number = 0
complete = False
while number_of_likes > 0 and complete is False:
    if offset_number < number_of_likes:
        try:
            track_fetch = urllib.request.urlopen("http://api.soundcloud.com/users/{}/"
                                                 "favorites.json?client_id={}&offset="
                                                 "{}&limit1".format(user.id, clientID, offset_number)).read()
            track_data = json.loads(track_fetch.decode())
            if "," in track_data[0]["title"]:
                track_title = track_data[0]["title"].replace(",",
                                                             "")  # Removes commas as causes issues with .csv files
            else:
                track_title = track_data[0]["title"]
            csv_file.write("{},{}\n".format(track_title, track_data[0]["permalink_url"]))
            offset_number += 1
            print("{} of {} ({}%)".format(offset_number, number_of_likes,
                                          round(float(100 / number_of_likes * offset_number), 2)))
        except IndexError:
            print("There is an issue with Soundcloud, please try again")
        except requests.HTTPError:
            print("There is an issue with Soundcloud, please try again")
        except requests.ConnectionError:
            print("Check your internet connection")
    else:
        complete = True

print("Finished")
