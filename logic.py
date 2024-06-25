import sqlite3
from config import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import cartopy.crs as ccrs


class DB_Map():
    def __init__(self, database):
        self.database = database
    def create_user_table(self):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS users_cities (
                                user_id INTEGER,
                                city_id TEXT,
                                FOREIGN KEY(city_id) REFERENCES cities(id)
                            )''')
            conn.commit()

    def add_city(self,user_id, city_name ):
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM cities WHERE city=?", (city_name,))
            city_data = cursor.fetchone()
            if city_data:
                city_id = city_data[0]  
                conn.execute('INSERT INTO users_cities VALUES (?, ?)', (user_id, city_id))
                conn.commit()
                return 1
            else:
                return 0

            
    def select_cities(self, user_id):
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT cities.city 
                            FROM users_cities  
                            JOIN cities ON users_cities.city_id = cities.id
                            WHERE users_cities.user_id = ?''', (user_id,))

            cities = [row[0] for row in cursor.fetchall()]
            return cities


    def get_coordinates(self, city_name):
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT lat, lng
                            FROM cities  
                            WHERE city = ?''', (city_name,))
            coordinates = cursor.fetchone()
            return coordinates

    def create_grapf(self, path, cities, user):
        ax = plt.axes(projection=ccrs.PlateCarree())
        ax.stock_img()
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            result1 = cur.execute("SELECT color FROM marker WHERE user = ?", [user])
            usrcolor = ""
            for row in result1:
                usrcolor += " ".join(row)
            result2 = cur.execute("SELECT point FROM marker WHERE user = ?", [user])
            usrmarker = ""
            for row in result2:
                usrmarker += " ".join(row)
            for city in cities:
                coord = self.get_coordinates(city_name=city)
                if not coord:
                    return
                
                lon, lat = coord
                plt.plot([lat], [lon], color=usrcolor, linewidth=1, marker=usrmarker, transform=ccrs.Geodetic())
                plt.text(lat + 3, lon + 12, city, horizontalalignment='left', transform=ccrs.Geodetic())
            
            plt.savefig(path)
        
    def draw_distance(self, city1, city2):
        pass
    def add_color_marker(self, name, color):
        conn = sqlite3.connect(self.database)

        with conn:
            cur = conn.cursor()
            result = cur.execute("SELECT user FROM marker")
            users = ""
            for row in result:
                users += " ".join(row) + "\n"
            if name in users:
                cur.execute("UPDATE marker SET color = ? WHERE user = ?", (color, name))
            else:
                cur.execute("INSERT INTO marker (user, color) VALUES (?, ?)", (name, color))
    def add_point_marker(self, name, point):
        conn = sqlite3.connect(self.database)

        with conn:
            cur = conn.cursor()
            result = cur.execute("SELECT user FROM marker")
            users = ""
            for row in result:
                users += " ".join(row) + "\n"
            if name in users:
                cur.execute("UPDATE marker SET point = ? WHERE user = ?", (point, name))
            else:
                cur.execute("INSERT INTO marker (user, point) VALUES (?, ?)", (name, point))
if __name__=="__main__":
    
    m = DB_Map(DB)
    m.create_user_table()
    