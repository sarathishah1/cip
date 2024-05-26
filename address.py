from typing import Dict, Any
from geopy.geocoders import Nominatim
from shapely import Point
import pickle

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
ISRAEL = 'ישראל'


class Address:
    def __init__(self, building_num: int, street: str, city: str, country: str = ISRAEL):
        self.building_num = building_num
        self.street = street
        self.city = city
        self.country = country
        self.geometry: Point = None
        self.area_id: int = None
        self.area_data = None

    def _get_address_point(self) -> Point:
        """
        takes an Israeli address and queries the free Nominatim geocoding API to get it's location.
        spelling should be precise.
        """
        coder = Nominatim(user_agent=UA)

        addr = self.street + ' ' + str(self.building_num)
        full_addr = addr + ', ' + self.city + ', ' + self.country

        res = coder.geocode(full_addr)
        if res:
            p = Point(res.longitude, res.latitude)
            self.geometry = p
            return p

        else:
            raise ValueError('Address geocoding failed')

    def _point_to_area_id(self) -> int:
        with open('data/geodata_pickle', 'rb') as f:
            gdf = pickle.load(f)

        area = gdf[gdf.contains(self.geometry)]
        if not area.empty:
            self.area_data = {k: list(v.values())[0] for k, v in area.to_dict().items()}
            self.area_id = self.area_data['YISHUV_STAT_2022']
            return self.area_id

        raise ValueError('No area found for the point')

    def get_area_id(self) -> int:
        self._get_address_point()
        return self._point_to_area_id()
