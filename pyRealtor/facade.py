from geo import GeoLocationService
from realtorFactory import RealtorFactory

class HousesFacade:

    def search_houses(
        self,
        search_area: str,
        country: str = None,
        state: str = None,
        listing_type: str = 'for_sale',
        use_proxy: bool = False,
        price_from: int = None,
        sorted_col_name: str = None,
        sorted_col_asc: bool = True,
        **kwargs
    ) -> list:
        geo_service_obj = GeoLocationService()

        if country is None:
            country = geo_service_obj.get_country(city=search_area, state=state)

        if country.lower().strip() != "canada":
            raise ValueError(f"Only Canada is currently supported, however received {country}")

        realtor_service_obj = RealtorFactory().get_realtor(country=country)

        geo_result_json = geo_service_obj.search_geo_location(
            city=search_area,
            province=state,
            country=country
        )

        display_address = geo_result_json["name"]
        geo_service_obj.set_display_physical_location(display_address)
        realtor_service_obj.set_transaction_type(listing_type)

        geo_service_obj.set_geo_location_boundry(geo_result_json)

        try:
            realtor_service_obj.set_geo_coordinate_boundry(geo_service_obj)
        except Exception:
            raise ValueError(f"Area: {search_area} in Country: {country} does not fit geographic requirements")

        if price_from is not None:
            realtor_service_obj.set_min_amount(
                new_amount=int(price_from),
                col_name=sorted_col_name
            )

        if sorted_col_name is not None:
            temp_col_name = 'listing_price' if sorted_col_name == 'Price' else sorted_col_name
            realtor_service_obj.set_sort_method(by=temp_col_name, ascending_order=sorted_col_asc)

        if 'open_house_date' in kwargs:
            realtor_service_obj.set_open_house_only(kwargs['open_house_date'])

        return realtor_service_obj.search_houses(use_proxy)
    
if __name__ == "__main__":
    import json
    listings = HousesFacade().search_houses(search_area="Toronto")
    print(f"Found {len(listings)} listings")
    print(json.dumps(listings[:2], indent=2))
