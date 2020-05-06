import httplib2
import json
import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

foursquare_client_id = "FZH3MW1T4HUXI1RDS4NX51HXZI3IYWBHS5WR2EAAQ52LXIN2"
foursquare_client_secret = "4VS5XAHEEMIK5WA4X1M34JMDCZOCRV2ZBISHKHXUB1ITUSDZ"

def findARestaurant(mealtype,location):
    googleapikey = "AIzaSyAIEmOssTsiIMvlZshUq94ZaRimWhCOm1w"
    locationString = location.replace(" " , "+")
    url = ('https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s'%(locationString , googleapikey))
    h = httplib2.Http()
    result = json.loads(h.request(url,'GET')[1])
    latitude = result['results'][0]['geometry']['location']['lat']
    longitude = result['results'][0]['geometry']['location']['lng']
    addr = str(latitude) + ","+str(longitude)
    uri = ('https://api.foursquare.com/v2/venues/search?client_id=%s&client_secret=%s&v=20130815&ll=%s&query=%s'%(foursquare_client_id, foursquare_client_secret,addr,mealtype))
    print uri
    resultloc = json.loads(h.request(uri,'GET')[1])
    if resultloc ['response']['venues'] :
        restaurant = resultloc['response']['venues'][0]
        venue_id=restaurant['id']
        restaurant_name = restaurant['name']
        restaurant_address = restaurant['location']['formattedAddress']
        address = ""
        for i in restaurant_address:
            address += i + " "
        restaurant_address = address
        url = ('https://api.foursquare.com/v2/venues/%s/photos?client_id=%s&v=20150603&client_secret=%s' % ((venue_id,foursquare_client_id,foursquare_client_secret)))
        resultloc = json.loads(h.request(url, 'GET')[1])
        if resultloc['response']['photos']['items']:
            firstpic = resultloc['response']['photos']['items'][0]
            prefix = firstpic['prefix']
            suffix = firstpic['suffix']
            imageURL = prefix + "300x300" + suffix
        else:
            imageURL = "http://pixabay.com/get/8926af5eb597ca51ca4c/1433440765/cheeseburger-34314_1280.png?direct"
        restaurantInfo = {'name':restaurant_name, 'address':restaurant_address, 'image':imageURL}
        print "Restaurant Name: %s" % restaurantInfo['name']
        print "Restaurant Address: %s" % restaurantInfo['address']
        print "Image: %s \n" % restaurantInfo['image']
        return restaurantInfo
    else:
        print "No Restaurants Found for %s" % location
        return "No Restaurants Found"
if __name__ == '__main__':
    findARestaurant("Pizza", "Tokyo, Japan")
    findARestaurant("Tacos", "Jakarta, Indonesia")
