from realtorCa import RealtorCa
from realtorCom import RealtorCom
from housingCom import HousingCom


class RealtorFactory:

    def get_realtor(self, country: str, config: str = None):

        country = country.lower()

        if country == 'canada':
            realtor_service_obj = RealtorCa()
        elif country == 'united states':
            realtor_service_obj = RealtorCom()
        elif country == 'india':
            realtor_service_obj = HousingCom()
        else:
            raise ValueError(f"Expected countries are United States, Canada, or India, however received {country}")

        return realtor_service_obj