from realtorCa import RealtorCa


class RealtorFactory:

    def get_realtor(self, country: str):

        country = country.lower().strip()

        if country != 'canada':
            raise ValueError(f"Only Canada is currently supported, however received {country}")

        realtor_service_obj = RealtorCa()

        return realtor_service_obj